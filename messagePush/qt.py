import json
import queue
import sys
import threading
import time
import traceback
from multiprocessing import Process

import requests
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QAbstractItemView
from flask import Flask, request
from qtconsole.qt import QtCore

from lock import Wlock, acquire
from logger import logger

try:
    from dialog import Ui_Dialog
except:
    from .dialog import Ui_Dialog

_web_message_list = []
_web_message_list_lock = Wlock()


class WwInviteQt(QWidget):
    _pid = 0

    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.slm_message = QStringListModel()

        self.init_ui()

        self.message_queue = queue.Queue(maxsize=1000)
        t = threading.Thread(
            target=self.get_add_message_from_queue, name="work", daemon=True
        )
        t.start()

        t = threading.Thread(
            target=self.training_rotation, name="work", daemon=True
        )
        t.start()

    def init_ui(self):
        self.setWindowOpacity(0.5)  # 设置窗口透明度
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        # self.setWindowFlags(Qt.CustomizeWindowHint)

        self.ui.list_view_message.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.list_view_message.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QApplication.processEvents()

        self.show()  # 显示

    def training_rotation(self):
        interval = 0
        while True:
            try:
                interval = 1
                if len(_web_message_list) == 0:
                    continue
                with acquire(_web_message_list_lock):
                    value = _web_message_list.pop(0)
                self.add_new_message(value)
                interval = 0.2
            except:
                traceback.print_exc()
            finally:
                time.sleep(interval)

    def add_new_message(self, message):
        self.message_queue.put(message)

    def get_add_message_from_queue(self):
        while True:
            message = self.message_queue.get()
            self._add_new_message_to_windows(message)
            time.sleep(1)

    def _add_new_message_to_windows(self, message: (str, int, float, dict, tuple, list, set)):
        logger.info("wile add new message: {} (type is {})".format(message, type(message)))
        msg = ""
        if isinstance(message, str):
            msg = message
        elif isinstance(message, (int, float)):
            msg = str(message)
        elif isinstance(message, dict):
            msg = message.get("message") if "message" in message else json.dumps(message)
        elif isinstance(message, (tuple, list, set)):
            msg = " ".join(message)

        show = self.slm_message.stringList()
        if len(show) > 9:
            show = show[-9:]

        show.append(msg)
        self.slm_message.setStringList(show)
        self.ui.list_view_message.setModel(self.slm_message)


web_app = Flask(__name__)
web_app.logger = logger


@web_app.route("/push", methods=["POST"])
def push():
    data = request.get_json()
    value = {}
    if "message" in data.keys():
        value["message"] = data.get("message")

    with acquire(_web_message_list_lock):
        _web_message_list.append(value)
    return "OK"


@web_app.before_first_request
def before_request():
    if request.path == "/favicon.ico":
        return

    method = request.method

    # 获取请求参数
    request_message = ""
    if method == "GET":
        request_message = request.args.to_dict()
    elif method == "POST":
        if request.json is not None:
            request_message = request.json
        elif request.form is not None:
            request_message = request.form

    # 获取请求用户的真实ip地址
    real_ip = request.remote_addr
    if request.headers.get("X-Forwarded-For") is not None:
        real_ip = request.headers.get("X-Forwarded-For")

    logger.info(
        "Path: {}  Method: {} RemoteAddr: {} headers: {} request_message: {}  ".format(
            request.path,
            request.method,
            real_ip,
            request.headers.to_wsgi_list(),
            request_message
            # , request.__dict__
        )
    )


def main_web():
    web_app.run(host="0.0.0.0", port=1800)


if __name__ == '__main__':
    # web_process = Process(target=main_web, name="WebServer", daemon=True)  # 实例化进程对象
    # web_process.start()

    t = threading.Thread(
        target=main_web, name="web", daemon=True
    )
    t.start()

    ui_app = QApplication(sys.argv)
    ex = WwInviteQt()
    sys.exit(ui_app.exec_())
