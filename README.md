# SearchMessage: A middleware for EFB 

## Notice

**Middleware ID**: `catbaron.search_msg`

**SearchMessage** is a middleware for EFB, to search message from the chat history.

Usually, you may have trouble to search messages with **Chinses** key words in Telegram clients,
thus here is the middleware could help you out.

Be aware that this is a very early develop version. Please let me know if you found any problem.

You need to use **MessageBlocker** on top of [EFB](https://ehforwarderbot.readthedocs.io). Please check the document and install EFB first.

## Dependense

* Python >=3.6
* EFB >=2.0.0
* peewee
* PyYaml
* python-dateutil

## Install

* Install
```
git clone https://github.com/catbaron0/efb-search_msg-middleware
cd efb-search_msg-middleware
Python setup.py install # You may need su permission here
```
* Register to EFB
Following [this document](https://ehforwarderbot.readthedocs.io/en/latest/getting-started.html) to edit the config file. The config file by default is `~/.ehforwarderbot/profiles/default`. It should look like:
```
master_channel: foo.demo_master
slave_channels:
- foo.demo_slave
- bar.dummy
middlewares:
- foo.other_middlewares
- catbaron.search_msg
```

You only need to add the last line to your config file.

* Config the middleware

The config file by default is `$HOME/.ehforwarderbot/profiles/default/catbaron.search_msg/config.yaml`.
Please create the config file if thers is not one.  Edit it as:

```
# The name of master channel
master: 'blueset.telegram'

# The max number of message the middleware would show you. 
# Set it to 0 for no limitation.
max_num: 15
```

* Restart EFB.

![](./example.png)

## How to use
### The command: 
`\sr [key_word] [from:datetime] [to:datetime]`
* `key_word`: text without whitespace characters
* `datetime`: Datetime string, such as `1989-6`, `2008-8-8 12:0`. Note that `from:` and `to:` are necessary and there should be no space in this argument. Messages of last 15 days will be searched by default.


### Usage
1. Sent command to a chat
   * There should be at least one of the three arguments
2. Reply the command to an message
   * Search message sent by the author of the replied message
   * Some times the author is saved as `None` in the database, so it's not always reliable. 
3. To locate the message in Telegram, you can:
   * Search the full message in Telegram
   * Search some segment of message splitted by non-chinese characters.
   * For instance, say you have a message `这是一条被空格分开  的消息`, to locate this message, you coulde search the entire message, `这是一条被空格分开` or `的消息` in Telegram.