import logging
import logging.handlers

# from log.commonhandlers import SSLSMTPHandler
import socket

import sys
sys.path.append('../')



class Logger(logging.Logger):

    _instance = None
    _first = True
    # 什么时间什么级别在哪个模块的哪个文件的哪个方法 哪个行号做了什么事情
    formatter = logging.Formatter('pid:%(process)d  level:%(levelname)s  ts:%(asctime)s  filename:%(filename)s  method:%(funcName)s  lineno:%(lineno)d  msg:%(message)s')
    # formatter = logging.Formatter('%(process)d\t%(levelname)s\t%(asctime)s\t%(filename)s\t%(funcName)s\t%(lineno)d\t%(message)s')

    def __init__(self,name='logger',debug=False,log_path=None,toaddrs=[],level = logging.INFO):
        '''
        :param name: 日志管理器的名字
        '''
        # if self._first:
        #     self._first = False
        self._start = None
        self._end = None

        self.__initconf(debug, name, level)
        self.__inithandler(debug, log_path, toaddrs)



    def __initconf(self, debug, name, level):
        logging.Logger.__init__(self,name, logging.DEBUG if debug else level)


    def __inithandler(self, debug, log_path,toaddres):
        self.__init_loghandler(debug, log_path)
        # self.__init_emailhandler(debug, toaddres)
        pass

    def __init_loghandler(self, debug, log_path):
        if debug:
            handler = logging.StreamHandler(sys.stdout)
        else:
            handler = logging.FileHandler(filename=log_path)
        handler.setFormatter(self.formatter)
        self.addHandler(handler)


    # def __init_emailhandler(self,debug,toaddres):
    #     if not debug:
    #         handler = SSLSMTPHandler(("smtp.exmail.qq.com", 465), 'dev@bishijie.com',
    #                                               toaddres,
    #                                                "报警日志",
    #                                                credentials=('dev@bishijie.com', 'Bishijie123'),timeout=60
    #                                                )
    #
    #         handler.setLevel(logging.ERROR)
    #         handler.setFormatter(self.formatter)
    #         self.addHandler(handler)


from log.settings import LOGCONFIG as settings

class PushLogger(logging.Logger):
    hostname = None
    _instance = None
    _first = True
    # 什么时间什么级别在哪个模块的哪个文件的哪个方法 哪个行号做了什么事情
    # formatter = logging.Formatter('pid=%(process)d\tlevel=%(levelname)s\tts=%(asctime)s\tfilename=%(filename)s\tmethod=%(funcName)s\tlineno=%(lineno)d\t%(message)s')
    formatter = logging.Formatter('')
    _logger = Logger(name=settings['name'], debug=settings['debug'], log_path=settings['log_path'],)

    def __init__(self,name='logger_push',debug=False,log_path=None,toaddrs=[], level=logging.INFO):
        '''
        :param name: 日志管理器的名字
        '''
        # if self._first:
        #     self._first = False
        self._start=None
        self._end=None
        self.isdebug = debug
        self.__initconf(debug, name, level)
        self.__inithandler(debug, log_path, toaddrs)



    def __initconf(self, debug, name, level):
        logging.Logger.__init__(self,name, logging.DEBUG if debug else level)

    def __inithandler(self, debug, log_path,toaddres):
        self.__init_loghandler(debug, log_path)
        # self.__init_emailhandler(debug,toaddres)
        pass

    def __init_loghandler(self, debug, log_path):
        if debug:
            handler = logging.StreamHandler(sys.stdout)
        else:
            handler = logging.FileHandler(filename=log_path)
        handler.setFormatter(self.formatter)
        self.addHandler(handler)

    def __to_string(self,*args,**kwargs):

        _msg = []
        for m in args:
            _msg.append('{}'.format(m))
        return '\t'.join(_msg)

    def info(self, *msg):
        self._logger._log(logging.INFO, self.__to_string(*msg), None)

    def error(self, *msg):
        self._logger._log(logging.ERROR, self.__to_string(*msg), None)

    # def warn(self, *msg):
    #     self._logger._log(logging.WARN, self.__to_string(*msg), None)

    def warning(self, *msg):
        self._logger._log(logging.WARNING, self.__to_string(*msg), None)

    def critical(self, *msg):
        self._logger._log(logging.CRITICAL, self.__to_string(*msg), None)

    def debug(self, *msg):
        if self.isdebug:
            self._logger._log(logging.DEBUG, self.__to_string(*msg), None)


    def get_sevhost(self):
        # 获取本机电脑名
        if not self.hostname:
             self.hostname = socket.gethostname()
        # 获取本机ip
        # myaddr = socket.gethostbyname(myname)

        return self.hostname

    # def push(self, mid,gid=uuid(),consum_time=0,msg='null'):
    #     '''
    #     :param msg: 要打印的消息
    #     :param mid: 模块的id
    #     :return:
    #     '''
    #     _msg = [
    #         # '{}'.format(int(time.time()*1000)),#ts
    #         # '{}'.format('REPORTTAG'),#identifier
    #         # '{}'.format(self.get_sevhost()),#sevhost
    #         '{}'.format(msg),#data
    #     ]
    #     self._log(logging.INFO, '\t'.join(_msg), None)


logger = PushLogger(name=settings['name'], debug=settings['debug'], log_path=settings['log_path'])


if __name__ == '__main__':

    # logger.push(mid=1,consum_time=10,gid='content',msg='asd')
    logger.p(mid='asd',name='张三',age=10)