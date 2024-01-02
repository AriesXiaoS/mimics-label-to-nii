
from common import signalBus
import traceback

def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            # 在这里执行原始函数
            return func(*args, **kwargs)
        except Exception as e:
            # 在这里处理异常
            tb = traceback.format_exc()
            signalBus.alertInfo.emit({
                'title': '错误',
                'content': tb,
                'duration': -1,
                'type': 'error',
            })
    return wrapper


















