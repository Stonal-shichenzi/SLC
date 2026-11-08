import requests as web
import re, json
from . import wbi

class BilibiliUserInfo():
    def __init__(self, uid: int) -> None:
        self.data = web.get("https://api.bilibili.com/x/space/acc/info?mid={}".format(uid)).json()
        # if self.data
        # 还没做完