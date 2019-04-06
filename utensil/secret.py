import rsa
import chardet


class Secret:
    def __init__(self, path_public='public.pem', path_private='private.pem'):
        self.path_public = path_public
        self.path_private = path_private


    def generate_key(self):  # 生成公钥与私钥
        # 生成密钥
        (pubkey, privkey) = rsa.newkeys(1024)

        # 保存密钥
        with open(self.path_public, 'w+') as f:
            f.write(pubkey.save_pkcs1().decode('utf-8'))

        with open(self.path_private, 'w+') as f:
            f.write(privkey.save_pkcs1().decode("utf-8"))

    def __import_key(self):  # 导入公钥与私钥
        with open(self.path_public, 'r') as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

        with open(self.path_private, 'r') as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

        return (pubkey, privkey)

    def pubkey_encryption(self, message):  # 公钥加密
        pubkey, privkey = self.__import_key()
        crypto = rsa.encrypt(message.encode(), pubkey)
        return crypto


    def privkey_decrypt(self, crypto):  # 私钥解密
        try:
            pubkey, privkey = self.__import_key()
            message = rsa.decrypt(crypto, privkey).decode()
            return message
        except:
            return None

    def privkey_encryption(self, message):  # 私钥签名
        try:
            pubkey, privkey = self.__import_key()
            signature = rsa.sign(message.encode(), privkey, 'SHA-256')
            return signature
        except:
            return None

    def pubkey_decrypt(self, message, signature):  # 公钥验证
        try:
            pubkey, privkey = self.__import_key()
            if rsa.verify(message.encode(), signature, pubkey) == 'SHA-256':
                return True
            else:
                return False
        except:
            return None

if __name__ == '__main__':
    temp = Secret()
