import os
import sys
sys.path.append("../")
from log.conf import *


if len(sys.argv) == 0:
    name = 'common'
else:
    name = sys.argv[0].split('/')[-1]
    index = name.rfind('.')
    if index != -1:
        name = name[:index]
# print(name)


LOGCONFIG={
    'name': 'crawl',
    'debug': Log_Debug,
    'log_path': 'E:/LazyCrawling/logs/{}.log'.format(os.path.split(name)[1]),
}

path_log = LOGCONFIG["log_path"]

# path_log = os.path.join(os.path.abspath(os.curdir), LOGCONFIG["log_path"]).replace("\\", "/")
path_log = os.path.split(path_log)[0]

if os.path.exists(path_log):
    pass
else:
    os.mkdir(path_log)



