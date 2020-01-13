import json
import random
import traceback
import sys
import threading
import time

import queue

import requests
from PyQt5.QtCore import Qt, QEvent, QStringListModel
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QWidget
from flask import Flask, request
from qtconsole.qt import QtCore

from logger import logger

try:
    from dialog import Ui_Dialog
except:
    from .dialog import Ui_Dialog


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
        self.setWindowOpacity(0.3)  # 设置窗口透明度
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        # self.setWindowFlags(Qt.CustomizeWindowHint)
        self.show()  # 显示

    def training_rotation(self):
        while True:
            try:
                message = requests.post("http://127.0.0.1:1800/push").text
                self.add_new_message(message)
            except (requests.exceptions.ConnectionError):
                pass
            except:
                traceback.print_exc()
            finally:
                time.sleep(1)

    def add_new_message(self, message):
        self.message_queue.put(message)

    def get_add_message_from_queue(self):
        while True:
            message = self.message_queue.get()
            self._add_new_message_to_windows(message)
            time.sleep(1)

    def _add_new_message_to_windows(self, message: (str, int, float, dict, tuple, list, set)):
        logger.info("wile add new message: {}".format(message))
        if isinstance(message, str):
            pass
        elif isinstance(message, (int, float)):
            message = str(message)
        elif isinstance(message, dict):
            message = json.dumps(message)
        elif isinstance(message, (tuple, list, set)):
            message = " ".join(message)

        show = self.slm_message.stringList()
        if len(show) > 9:
            show = show[-9:]

        show.append(message)
        self.slm_message.setStringList(show)
        self.ui.list_view_message.setModel(self.slm_message)


if __name__ == "__main__":
    ui_app = QApplication(sys.argv)
    ex = WwInviteQt()
    sys.exit(ui_app.exec_())
