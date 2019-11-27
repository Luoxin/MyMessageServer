import sys
sys.path.append('../')
sys.path.append('../../')

from utensil import logger

import time
from urllib.parse import urljoin
from .download_html import DownLoaderHtml
from .analyze_html import AnalyzeHtml
from .conf_RSS import *
import json
from websocket import create_connection


def send_messagr(message):
    try:
        ws = create_connection("ws://{}:{}".format(SERVERHOST, SERVERPORT))
        ws.send(json.dumps(message))
        ws.close()
    except:
        pass

class Controller:
    def __init__(self):
        self.backup = set()
        self.current = set()


    def update_list(self, id):  # 更新新的列表
        self.current.add(id)

        if id in self.backup:
            return False
        else:
            return True

    def update_index(self):  # 更新索引位置
        del self.backup
        self.backup = self.current
        self.current = set()


class RSS:
    def __init__(self):
        self.download = DownLoaderHtml()  # 下载模块
        self.analyze = AnalyzeHtml()  # 解析模块

        self.controller = {}
        for key, __ in RSSLIST.items():
            self.controller[key] = Controller()

        while True:
            logger.info("一次新的消息获取推送")
            self.dispatch()  # 总体调度
            time.sleep(30)

    def dispatch(self):
        for key, value in RSSLIST.items():
            try:
                rss_message = self.get_data(value["base_url"], value['url_routing'], value['analyze_rule'])
                if rss_message:
                    for message in rss_message:
                        if self.controller[key].update_list(message["id"]):
                            temp = message
                            temp["消息来源"] = key
                            message_send = {
                                'type': "message",
                                'level': 'protecte',
                                "info": temp
                            }
                            send_messagr(message_send)  # 获取到消息后发送到服务端并停止30秒
                            time.sleep(30)
                            # print(message)
                            # break

            finally:
                logger.info("{} 的新消息推送完毕".format(key))
                self.controller[key].update_index()


    def get_data(self, base_url, url_routing, analyze_rule):
        try:
            url = urljoin(base_url, url_routing)
            xml_content = self.download.download_html(url)
            analyze_rule["reorganization"] = list(analyze_rule.keys())

            status, result = self.analyze.parse_xpath_xml(xml_content, analyze_rule)
            if status:
                return result["reorganization"][0]
            else:
                return False
        except:
            return False







if __name__ == '__main__':
    # Controller()
    RSS()