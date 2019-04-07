import sys
sys.path.append('../')
from log import logger

from user_authentication import UserAuthentication
from websocket_server import WebsocketServer
from conf import *
import json
import string


PrivateList = []  # 私人用户的列表
PrivateMessage = []

ProtecteList = []  # 拥有部分权限的用户列表
ProtecteMessage = []

PublicList = []  # 公共订阅
PublicMessage = []

verifiedList = []  # 公共订阅列表
messsageList = []

def send_message_to_private(message):  # 给所有的私人用户推送消息
	for client in PrivateList:
		server.send_message(client, json.dumps(message))

def send_message_to_protecte(message):  # 给所有的朋友推送消息
	for client in ProtecteList:
		server.send_message(client, json.dumps(message))

def send_message_to_public(message):  # 给所有的公用订阅推送消息
	for client in PublicList:
		server.send_message(client, json.dumps(message))

def send_message(level='public'):  # 推送消息

	if level == 'private':
		if PrivateList.__len__() > 0 :  # 如果存在私人的客户端，则往私人消息中推送信息
			if PrivateMessage.__len__() > 0:  # 如果存在私人的消息队列
				while PrivateMessage.__len__() != 0:  # 推送消息直到没有未推送的消息位置
					message = PrivateMessage.pop(0)
					send_message_to_private(message)

	elif level == 'protecte':
		if ProtecteList.__len__() > 0 or PrivateList.__len__() > 0:   # 如果存在朋友的客户端，则往朋友消息中推送信息
			if ProtecteMessage.__len__() > 0 or PrivateMessage.__len__() > 0:  # 如果存在朋友的客户端，则往朋友消息中推送信息
				while ProtecteMessage.__len__() != 0:  # 推送消息直到没有未推送的消息位置
					message = ProtecteMessage.pop(0)
					send_message_to_private(message)
					send_message_to_protecte(message)

	elif level == 'public':
		if PublicList.__len__() > 0 or ProtecteList.__len__() > 0 or PrivateList.__len__() > 0:   # 如果存在公用订阅的客户端，则往公用订阅消息中推送信息
			if PublicMessage.__len__() > 0 or PrivateMessage.__len__() > 0 or ProtecteMessage.__len__() > 0:  # 如果存在公用订阅的客户端，则往公用订阅消息中推送信息
				while PublicMessage.__len__() != 0:  # 推送消息直到没有未推送的消息位置
					message = PublicMessage.pop(0)
					send_message_to_private(message)
					send_message_to_protecte(message)
					send_message_to_public(message)








# websocket相关代码
def new_client(client, server):  # 建立一个新连接
	pass

def client_left(client, server):  # 关闭一个连接
	if client['id'] in verifiedList:
		verifiedList.remove(client["id"])
		logger.info("用户断开连接(id: {})".format(client['id']))


def message_received(client, server, message):  # 接受消息
	try:
		message = json.loads(message)
		if message["type"] == "message":  # 新的消息
			eval(string.capwords(message['level']) + 'Message').append(message["info"])  # 将消息发送给响应的权限队列
			send_message(message['level'])

		elif message["type"] == "subscription":  # 新的用户订阅
			'''
			- 验证用户身份
			'''
			# print(message["info"])
			user_auth = UserAuthentication()

			if message['info']["username"] == 'private':  # 私人的订阅(用户的微信等敏感信息)
				if user_auth.rsa(message['info']['password']):  # 对进行私钥的验证
					PrivateList.append(client)
					logger.info("加入新的私人推送客户端(id: {})".format(client['id']))
					server.send_message(client, json.dumps({"message": "连接建立成功"}))
					send_message('private')  # 推送历史消息

			elif message['info']['username'] == 'protecte':  # 拥有部分权限的订阅用户
				if message['info']['password'] == PUBLICID:
					ProtecteList.append(client)
					logger.info("加入新的朋友推送客户端(id: {})".format(client['id']))
					server.send_message(client, json.dumps({"message": "连接建立成功"}))
					send_message('protecte')  # 推送历史消息

			else:
				PublicList.append(client)
				logger.info("加入新的公共订阅推送客户端(id: {})".format(client['id']))
				server.send_message(client, json.dumps({"message": "连接建立成功"}))
				send_message()  # 推送历史消息
	except:
			pass



server = WebsocketServer(port=PORT, host=HOST)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()