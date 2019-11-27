import sys

sys.path.append("../")
from utensil import logger

from .user_authentication import UserAuthentication
from websocket_server import WebsocketServer
from .conf import *
import json
import string


# 消息相关的代码

MessageCache = {
    "private": {"userlist": [], "message": []},
    "protecte": {"userlist": [], "message": []},
    "public": {"userlist": [], "message": []},
}

PrivateList = []  # 私人用户的列表
PrivateMessage = []

ProtecteList = []  # 拥有部分权限的用户列表
ProtecteMessage = []

PublicList = []  # 公共订阅
PublicMessage = []

verifiedList = []  # 公共订阅列表
messsageList = []


def send_message_to_private(message):  # 给所有的私人用户推送消息
    broken = []
    for client in PrivateList:
        try:
            server.send_message(client, json.dumps(message))
        except:
            broken.append(client)
    for client in broken:
        PrivateList.remove(client)


def send_message_to_protecte(message):  # 给所有的朋友推送消息
    broken = []
    for client in ProtecteList:
        try:
            server.send_message(client, json.dumps(message))
        except:
            broken.append(client)
    for client in broken:
        ProtecteList.remove(client)


def send_message_to_public(message):  # 给所有的公用订阅推送消息
    broken = []
    for client in PublicList:
        try:
            server.send_message(client, json.dumps(message))
        except:
            broken.append(client)
    for client in broken:
        PublicList.remove(client)


def send_message(level="public"):  # 推送消息

    logger.debug(level)
    logger.debug(PrivateMessage)
    logger.debug(ProtecteMessage)
    logger.debug(PublicMessage)
    if level in ["private", "protecte", "public"]:  # 个人接受所有消息
        if PrivateList.__len__() > 0:  # 如果存在私人的客户端，则往私人消息中推送信息
            logger.debug("发送新消息给private")
            while PrivateMessage.__len__() != 0:  # 推送消息直到没有未推送的消息位置
                message = PrivateMessage.pop(0)
                send_message_to_private(message)

    if level in ["protecte", "public"]:  # 朋友接受部分消息
        if ProtecteList.__len__() > 0:  # 如果存在朋友的客户端，则往朋友消息中推送信息
            logger.debug("发送新消息给protecte")
            while ProtecteMessage.__len__() != 0:  # 推送消息直到没有未推送的消息位置
                message = ProtecteMessage.pop(0)
                send_message_to_protecte(message)

    if level in ["public"]:  # 公共接受公共消息
        if PublicList.__len__() > 0:  # 如果存在公用订阅的客户端，则往公用订阅消息中推送信息
            logger.debug("发送新消息给public")
            while PublicMessage.__len__() != 0:  # 推送消息直到没有未推送的消息位置
                message = PublicMessage.pop(0)
                send_message_to_public(message)


def new_message(
    message, level="public",
):  # 得到新的消息
    """
	如果长度过大，则清理内存
	:param level:
	:param message:
	:return:
	"""
    if level in ["private", "protecte", "public"]:  # 个人接受所有消息
        if PrivateMessage.__len__() > 200:
            logger.debug("private消息队列已满")
            PrivateMessage.pop(0)
        PrivateMessage.append(message)

    if level in ["protecte", "public"]:  # 朋友接受部分消息
        if PrivateMessage.__len__() > 100:
            logger.debug("protecte消息队列已满")
            ProtecteMessage.pop(0)
        ProtecteMessage.append(message)

    if level in ["public"]:  # 公共接受公共消息
        if PrivateMessage.__len__() > 50:
            logger.debug("public消息队列已满")
            PublicMessage.pop(0)
        PublicMessage.append(message)

    logger.debug("接收到新的消息  {}".format(message))
    send_message(level)


# websocket相关代码
def new_client(client, server):  # 建立一个新连接
    pass


def client_left(client, server):  # 关闭一个连接
    if client["id"] in PrivateList:
        PrivateList.remove(client["id"])
        logger.info(
            "私人断开连接(id: {}, 当前用户: {})".format(
                client["id"], [client_i["id"] for client_i in PrivateList]
            )
        )

    elif client["id"] in ProtecteList:
        ProtecteList.remove(client["id"])
        logger.info("朋友断开连接(id: {})".format(client["id"]))
    elif client["id"] in PublicList:
        PublicList.remove(client["id"])
        logger.info("公共订阅断开连接(id: {})".format(client["id"]))


def message_received(client, server, message):  # 接受消息
    try:
        message = json.loads(message)
        if message["type"] == "message":  # 新的消息
            new_message(message["info"], level=message["level"])

        elif message["type"] == "subscription":  # 新的用户订阅
            """
			- 验证用户身份
			"""
            if message["info"]["username"] == "private":  # 私人的订阅(用户的微信等敏感信息)
                user_auth = UserAuthentication()
                if user_auth.rsa(message["info"]["password"]):  # 对进行私钥的验证
                    MessageCache["private"]["userlist"].append(client)
                    logger.info(
                        "加入新的私人推送客户端(id: {},当前用户: {}, 积累的的消息已有 {})".format(
                            client["id"],
                            [client_i["id"] for client_i in PrivateList],
                            PrivateMessage.__len__(),
                        )
                    )
                    server.send_message(client, json.dumps({"message": "连接建立成功"}))
                    send_message("private")  # 推送历史消息

            elif message["info"]["username"] == "protecte":  # 拥有部分权限的订阅用户
                if message["info"]["password"] == PUBLICID:
                    ProtecteList.append(client)
                    logger.info("加入新的朋友推送客户端(id: {})".format(client["id"]))
                    server.send_message(client, json.dumps({"message": "连接建立成功"}))
                    send_message("protecte")  # 推送历史消息

            else:
                PublicList.append(client)
                logger.info("加入新的公共订阅推送客户端(id: {})".format(client["id"]))
                server.send_message(client, json.dumps({"message": "连接建立成功"}))
                send_message()  # 推送历史消息
    except:
        pass


server = WebsocketServer(port=PORT, host=HOST)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
