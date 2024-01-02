

class GlobalVar():
    def __init__(self) -> None:
        self.global_dict = {}

    def set(self, key, value):
        """ 定义一个全局变量 """
        self.global_dict[key] = value
    
    def get(self, key, defValue=None):
        """
        获得一个全局变量,不存在则返回默认值
        """
        return self.global_dict.get(key, defValue)

globalVar = GlobalVar()








