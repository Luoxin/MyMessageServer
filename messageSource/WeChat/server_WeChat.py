import sys
sys.path.append('../')
sys.path.append('../../')


import time
import json

from log import logger

import itchat
from itchat.content import *
from conf import *
from websocket import create_connection

def send_messagr(message):  # 将消息推送给消息推送
    ws = create_connection("ws://{}:{}".format(SERVERHOST, SERVERPORT))
    ws.send(json.dumps(message))
    ws.close()


# 自动回复

# 无法处理的消息
VideoReply = '''检测到您发送的是媒体文件(非文字)，如若有急事，人工转换成文字再发送。{}'''.format(LITTLETAIL)

# 新好友
NewFriend = '''Nice to meet you!{}'''.format(LITTLETAIL)

# 无趣的在
Ignore_zai = '''不在，有事说事，我会把消息推送给小主人的。{}'''.format(LITTLETAIL)

# 爱你

# 时间戳转换为时间
def ts_to_datatime(ts):
    tl = time.localtime(float(ts))
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", tl)
    return format_time





# 机器人部分
itchat.auto_login(hotReload=True, enableCmdQR=False)
logger.info("用户已登录")
# 获取自己的id
my_info = itchat.search_friends()
my_UserName = my_info["UserName"]


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    try:
        if msg["FromUserName"] != my_UserName:
            messgae = msg.text
            if messgae in ["在", "在不在", "在？", "在不在？", "在吗", "在吗？", "在嘛", "在么", "在嘛?", "在么?"]:
                msg.user.send(Ignore_zai)
            elif ("爱你" in messgae) or ("喜欢你" in messgae):
                msg.user.send(Ignore_zai)
            else:
                messgae = {
                    "type": "message",
                    'level': 'private',
                    "info": {
                        "消息来源": "WeChat",
                        "昵称": msg.user["NickName"].replace("\"", "\\\"").replace("\\", "\\\\").replace("\'", "\\\'"),
                        "备注": msg.user["RemarkName"],
                        "消息": msg.text,
                        "Time": msg["CreateTime"]
                    }
                }
                send_messagr(messgae)
                logger.info("收到 {} 发送的消息".format(msg.user["RemarkName"]))
    except:
        pass

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def video_reply(msg):
    msg.user.send(VideoReply)


# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
# def download_files(msg):
#     if msg["FromUserName"] != my_UserName:
#         # msg.download(msg.fileName)
#         # typeSymbol = {
#         #     PICTURE: 'image',
#         #     VIDEO: 'voice', }.get(msg.type, 'fil')
#         # print("Received a {}.".format(typeSymbol), "{}({}) from:".format(typeSymbol, msg.fileName), msg.user["RemarkName"], "(time at {})".format(ts_to_datatime(msg["CreateTime"])))
#         msg.user.send(Ignore_zai)


@itchat.msg_register(FRIENDS)  # 自动加好友
def add_friend(msg):
    msg.user.verify()
    msg.user.send(NewFriend)


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg["FromUserName"] != my_UserName:
        if msg["Type"] == "Text":
            if "全体成员" in msg["Text"]:
                messgae = {
                    "type": "message",
                    'level': 'private',
                    "info": {
                        "消息来源": "WeChat(群聊通知)",
                        "昵称": msg["ActualNickName"].replace("\"", "\\\"").replace("\\", "\\\\").replace("\'", "\\\'"),
                        "消息": msg["Text"],
                        "Time": msg["CreateTime"]
                    }
                }
                send_messagr(messgae)

itchat.run(True)
