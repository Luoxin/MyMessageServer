import json
import re
import socket
import traceback
import uuid as uu

from utensil import logger


class Instrument:
    @staticmethod
    def is_json(data: (bytes, str)) -> bool:
        if isinstance(data, bytes):
            data = data.decode()
        if isinstance(data, str):
            try:
                json.loads(data)
                return True
            except:
                logger.error(traceback.format_exc())
                return False
        return False

    @staticmethod
    def encode_to_utf8(data: str != "") -> str:
        # chardet.detect(data.encode()).get("encoding")
        return data.encode().decode("utf-8")

    @staticmethod
    def uuid() -> str:
        """
            获取uuid
        :return: uuid
        """
        return uu.uuid4().hex

    @staticmethod
    def get_extra_net_ip() -> str:  # 获取本机ip
        extra_net_ip = "127.0.0.1"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('223.5.5.5', 80))
            extra_net_ip = s.getsockname()[0]
            s.close()
        except:
            logger.error(traceback.format_exc())

        return extra_net_ip

    @staticmethod
    def is_url(url):  # 判断是否为一个标准的url格式
        pattern_url = re.compile(r'((http)/(https)|(ws)/(wss)/(ftp)/(ssh)/(sftp)):\/\/[^\s]*')
        if pattern_url.search(url):
            return True
        else:
            return False