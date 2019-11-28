import json
import traceback

from websocket import create_connection, WebSocketException

from conf.conf_WebSocket import SERVER_HOST, SERVER_PORT
from utensil import logger


def send_message(message):
    try:
        ws = create_connection("ws://{}:{}".format(SERVER_HOST, SERVER_PORT))
        ws.send(json.dumps(message))
        ws.close()
    except:
        logger.error(traceback.format_exc())


if __name__ == '__main__':
    send_message("hahaha")