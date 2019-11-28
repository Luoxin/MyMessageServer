from websocket_server import WebsocketServer

from utensil import logger


def new_client(client, server):
    logger.info("new client {}".format(client))
    server.send_message_to_all("Hey all, a new client has joined us")
    server.send_message(client, "success")


def set_fn_client_left(client, server):
    logger.warning("client has closed", client.get("id"))


def set_fn_message_received(client, server, message):
    pass

ws = WebsocketServer(1802, host="127.0.0.1")
ws.set_fn_new_client(new_client)
ws.set_fn_message_received(set_fn_message_received)
ws.set_fn_client_left(set_fn_client_left)
ws.run_forever()
