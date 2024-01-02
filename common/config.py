import os
from PySide6.QtCore import *
from qfluentwidgets import *

import ctypes.wintypes

## 应用名字
APP_NAME = "mimics标注转Nifti"
## 应用版本
APP_VERSION = "0.0.1"
APPDATA = os.getenv('APPDATA')
APP_FOLDER = os.path.join(APPDATA, APP_NAME)
os.makedirs(APP_FOLDER, exist_ok=True)
CONFIG_PATH = os.path.join(APP_FOLDER, 'config.json')


class Config():
    def __init__(self, path):
        super().__init__()
        self.file = path
        self.cfg = dict()
        self.load()

    def get(self, key, default = None):
        return self.cfg.get(key, default)
    
    def set(self, key, value):
        self.cfg[key] = value
        self.save()
    
    def save(self):
        with open(self.file, 'w', encoding='utf8') as f:
            json.dump(self.cfg, f, indent=4, ensure_ascii=False )
    
    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf8') as f:
                self.cfg = json.load(f)
        else:
            self.cfg = dict()
    
    def initOneCfg(self, name, value, reset = False):
        if not reset:
            val = self.get(name)
            if val is None:
                self.set(name, value)
                val = value
        else:
            self.set(name, value)
            val = value
        return val

cfg = Config(CONFIG_PATH)

########################
## 用户可以修改的config

def getDocPath(pathID=5):
    '''path=5: My Documents'''
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, pathID, None, 0, buf)
    return buf.value

DOC_PATH = getDocPath()
DOC_APP_FOLDER = os.path.join(DOC_PATH, APP_NAME)
os.makedirs(DOC_APP_FOLDER, exist_ok=True)
USER_CONFIG_PATH = os.path.join(DOC_APP_FOLDER, 'config.json')

User_cfg = Config(USER_CONFIG_PATH)


'''
默认的label颜色
'''
Label_color_map = [ # 从1开始 
    # itk-snap的默认设置
    [ 1, 0, 0 ], # 1
    [ 0, 1, 0 ], # 2
    [ 0, 0, 1 ], # 3
    [ 1, 1, 0 ], # 4
    [ 0, 1, 1 ], # 5
    [ 1, 0, 1 ], # 6
    [ 1, 239/255, 213/255 ], # 7
    [ 0, 0, 205/255 ], # 8
    [ 205/255, 133/255, 63/255 ], # 9
]
Label_names = {
    1 : 'LV',
    2 : 'RV',
    3 : 'LA',
    4 : 'RA',
    5 : 'Myo',
    6 : 'Ao',
    7 : 'PA'
}

Addition_keyboard = { # https://blog.csdn.net/humanking7/article/details/80700233
    81 : 11, # Q
    87 : 12, # W
    69 : 13, # E
    82 : 14, # R
    84 : 15, # T
    89 : 16, # Y
    85 : 17, # U
    73 : 18, # I
    79 : 19, # O
    80 : 20, # P
}

User_cfg.initOneCfg('label_names', Label_names, reset = False)
User_cfg.initOneCfg('label_color_map', Label_color_map, reset = False)
User_cfg.initOneCfg('addition_keyboard', Addition_keyboard, reset = False)








