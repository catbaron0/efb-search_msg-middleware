from peewee import Model
from peewee import SqliteDatabase
from peewee import TextField, DateTimeField
from ehforwarderbot import utils
import datetime
import os
import operator
from functools import reduce
from typing import List

# dependence
from dateutil.relativedelta import relativedelta as relative_dt
from peewee import Expression


class DatabaseManager:
    def __init__(self, master: str):
        # self.db = SqliteDatabase(str(base_path / 'ftdata.db'))
        base_path: str = utils.get_data_path(master)
        self.db: SqliteDatabase = SqliteDatabase(
            os.path.join(base_path, 'tgdata.db'))
        self.db.connect()

        class BaseModel(Model):
            class Meta:
                database = self.db

        class MsgLog(BaseModel):
            master_msg_id = TextField(unique=True, primary_key=True)
            master_msg_id_alt = TextField(null=True)
            slave_message_id = TextField()
            text = TextField()
            slave_origin_uid = TextField()
            slave_origin_display_name = TextField(null=True)
            slave_member_uid = TextField(null=True)
            slave_member_display_name = TextField(null=True)
            media_type = TextField(null=True)
            mime = TextField(null=True)
            file_id = TextField(null=True)
            msg_type = TextField()
            sent_to = TextField()
            time = DateTimeField(default=datetime.datetime.now, null=True)

        self.MsgLog = MsgLog

    def select(self, filters, limit):
        clauses: List[Expression] = list()

        # search messages in current chat
        clauses.append((self.MsgLog.slave_origin_uid == filters['chat']))

        # search messages after a datetime
        # search messages in last 15 days by default
        delt_dt = relative_dt(days=15)
        to_dt = datetime.datetime.now()
        from_dt = to_dt - delt_dt
        if 'from' in filters:
            from_dt = filters['from']
        if 'to' in filters:
            to_dt = filters['to']
        clauses.append((self.MsgLog.time >= from_dt))
        clauses.append((self.MsgLog.time <= to_dt))

        # search messages sent by an author
        if 'author' in filters:
            clauses.append((self.MsgLog.slave_member_uid == filters['author']))

        # search messages containing the text
        if 'key' in filters:
            clauses.append((self.MsgLog.text.contains(filters['key'])))

        return (self.MsgLog.select(
                        self.MsgLog.time,
                        self.MsgLog.slave_origin_display_name,
                        self.MsgLog.slave_member_display_name,
                        self.MsgLog.text)
                    .where(reduce(operator.and_, clauses))
                    .limit(limit)
                    .order_by(self.MsgLog.time))
