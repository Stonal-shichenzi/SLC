import requests as web
import re, json, time, os

def build_mixin_key(cache_folder_directory: str = None):
    # 日志记录：报错用 ERROR 等级
    MIXIN_KEY_ENC_TAB = [
        46, 47, 18,  2, 53,  8, 23, 32, 15, 50, 10, 31, 58,  3, 45, 35,
        27, 43,  5, 49, 33,  9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
      # 37, 48,  7, 16, 24, 55, 40, 61, 26, 17,  0,  1, 60, 51, 30,  4,
      # 22, 25, 54, 21, 56, 59,  6, 63, 57, 62, 11, 36, 20, 34, 44, 52
    ]
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0 SLCRequester/1.0.0"
    if cache_folder_directory is None:
        native: dict = web.get("https://api.bilibili.com/x/web-interface/nav", headers={"User-Agent": USER_AGENT}, timeout=5).json()
    else:
        cache_filename = "biliCacheNav_{}.json".format(time.strftime("%Y%j", time.localtime()))
        if cache_filename in os.listdir(cache_folder_directory):
            with open(cache_filename, mode="r", encoding="utf-8") as cache_file:
                native: dict = json.load(cache_file)
        else:
            native: dict = web.get("https://api.bilibili.com/x/web-interface/nav", headers={"User-Agent": USER_AGENT}, timeout=5).json()
            with open(cache_filename, mode="w", encoding="utf-8") as cache_file:
                cache_file.write(json.dumps(native, ensure_ascii=False, indent=4))
    try:
        img_url: str = native["data"]["wbi_img"]["img_url"]
        sub_url: str = native["data"]["wbi_img"]["sub_url"]
    except (KeyError, TypeError):
        raise ValueError("Invalid structure:\n{}".format(json.dumps(native, ensure_ascii=False, indent=4)))
    img_key = get_hash_from_url(img_url)
    sub_key = get_hash_from_url(sub_url)
    raw_wbi_key = img_key + sub_key
    mixin_key_full = str()
    for i in MIXIN_KEY_ENC_TAB:
        mixin_key_full += raw_wbi_key[i]
    # return mixin_key_full[:32]
    return mixin_key_full
def get_hash_from_url(url: str) -> str:
    local_hash = re.findall("(?<=/bfs/wbi/)([0-9a-f]{32})(?=\\.png)", url)
    if local_hash:
        return local_hash[0]
    else:
        raise ValueError("Invalid URL to check: {}".format(url))
def build_mixin_wrid(args: dict):
    unix_time = int(time.time())
    # 还没做完