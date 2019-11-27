# 用户身份验证与归类
import os
import sys

sys.path.append("../")

from utensil import logger
from .conf import *
from utensil.secret import Secret


class UserAuthentication:
    def __init__(self):
        pass

    def rsa(self, privkey):  # 利用rsa算法对私钥进行验证
        try:
            count = 0
            while True:  # 获取临时存储的地址(防止多用户同时)
                path = "./temp_{}.pem".format(count)
                if os.path.exists(path):
                    continue
                else:
                    del count
                    break

            with open(path, "w+") as f:  # 因为编码的问题将私钥临时存储为一个临时的私钥文件
                f.write(privkey)

            secret = Secret(path_public="../utensil/public.pem", path_private=path)
            return secret.pubkey_decrypt(privkey, secret.privkey_encryption(privkey))
        except:
            return False
        finally:
            os.remove(path)  # 删除临时存储的私钥


if __name__ == "__main__":
    UserAuthentication()
