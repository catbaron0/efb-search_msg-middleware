# coding: utf-8
import logging
import os
from typing import Any, Dict, Optional, List, Iterator
from .db import DatabaseManager

from ehforwarderbot import EFBMiddleware, EFBChat, EFBMsg, MsgType, coordinator
from ehforwarderbot.utils import get_config_path
from . import __version__ as version

from dateutil.parser import parse as parse_dt
import yaml


class SearchMessageMiddleware(EFBMiddleware):
    """
    EFB Middleware - MessageBlockerMiddleware
    Add and manage filters to block some messages.

    Author: Catbaron <https://github.com/catbaron>
    """
    middleware_id = "catbaron.search_msg"
    middleware_name = "Search Message Middleware"
    __version__ = version.__version__
    logger: logging.Logger = logging.getLogger(
        "plugins.%s.SearchMessageMiddleware" % middleware_id
        )

    def __init__(self, instance_id=None):
        super().__init__()
        self.config: Dict[str: str] = self.load_config()
        self.master: str = self.config.get('master', 'blueset.telegram')
        self.command: str = self.config.get("command", '\\sr')
        self.max_num: int = int(self.config.get('max_num', 0))
        self.db: DatabaseManager = None
        self.label: str = '>>Search Results<<'

    def reply_msg(self, message: EFBMsg, text) -> EFBMsg:
        msg: EFBMsg = EFBMsg()
        msg.chat = message.chat
        msg.author = message.author
        msg.author.module_id = self.middleware_id
        msg.author.module_name = self.middleware_name
        msg.author.chat_name = 'Search Message'
        msg.author.module_id = self.middleware_id
        msg.author.module_name = self.middleware_name
        msg.deliver_to = coordinator.master
        msg.type = MsgType.Text
        msg.uid = message.uid
        msg.text = text
        return msg

    def load_config(self) -> Optional[Dict]:
        config_path: str = get_config_path(self.middleware_id)
        if not os.path.exists(config_path):
            self.logger.info('The configure file does not exist!')
            return
        with open(config_path, 'r') as f:
            d = yaml.load(f)
            if not d:
                self.self.logger.info('Load configure file failed!')
                return
            return d

    @staticmethod
    def sent_by_master(message: EFBMsg) -> bool:
        author: EFBChat = message.author
        try:
            if author.module_id == 'blueset.telegram':
                return True
            else:
                return False
        except Exception:
            return False

    def process_message(self, message: EFBMsg) -> Optional[EFBMsg]:
        """
        Process a message with middleware
        Returns:
            Optional[:obj:`.EFBMsg`]: Processed message or None if discarded.
        """
        if not self.sent_by_master(message):
            return message

        chat, target = message.chat, message.target
        msg_text: str = message.text.strip()

        if msg_text.startswith(self.command):
            if not self.db:
                self.db = DatabaseManager(self.master)

            filters: Dict[str: Any] = dict()
            # add filters for select records from db
            filters['chat'] = f'{chat.module_id} {chat.chat_uid}'

            args: List[str] = msg_text.split()[1:]
            for arg in args:
                arg = arg.strip()
                if arg.startswith('from:'):
                    # from datetime
                    try:
                        from_dt = parse_dt(arg[5:])
                        filters['from'] = from_dt
                    except Exception as e:
                        reply_text = f'Failed to parse the from_datetime: {e}'
                        return self.reply_msg(message, reply_text)
                elif arg.startswith('to:'):
                    # from datetime
                    try:
                        from_dt = parse_dt(arg[3:])
                        filters['to'] = from_dt
                    except Exception as e:
                        reply_text = f'Failed to parse the to_datetime: {e}'
                        return self.reply_msg(message, reply_text)
                else:
                    # key word
                    filters['key'] = arg
            if target:
                # match an author
                filters['author'] = target.author.chat_uid if \
                    not target.author.is_self else None
            records: Iterator = self.db.select(filters, self.max_num)
            records_str: List[str] = [self.label,]
            for record in records:
                dt = record.time
                au = record.slave_member_display_name
                txt = record.text
                if txt.startswith(self.label):
                    continue
                records_str.append(
                    f'{str(dt).split(".")[0]}\n'
                    f'{au}:\n'
                    f'{txt}\n')
                reply_text = '\n'.join(records_str)
                if len(reply_text) > 1000:
                    too_long = '\nThe search results are too long!'
                    reply_text = reply_text[:1000] + '\n...' + too_long
            return self.reply_msg(message, reply_text)
        return message
