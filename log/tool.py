import sys
sys.path.append('../')
sys.path.append('../../')
import uuid as uu

def uuid():  #  获取uuid
    return uu.uuid4().hex
