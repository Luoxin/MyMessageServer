import sys
sys.path.append("../")

import time
from .commonlog import logger
from log.tool import uuid

def logpush(mid,gid=uuid(),msg='null'):
    def logwapper(fun):
        def _logwapper(*agrs,**kwargs):
            start_time = time.time()*1000
            val= fun(*agrs,**kwargs)
            end_time = time.time()*1000
            consum_time = int(end_time-start_time)
            logger.push(mid=mid, gid=gid, consum_time=consum_time, msg=msg)
            return val
        return _logwapper
    return logwapper


