import requests as __web
class download:
    def __init__(self, url: str, filename: str) -> None:
        response = __web.get(url, stream=True)
        # total默认-1
        self.total_size = int(response.headers.get("content-length", -1))
        block_size = 1024
        with open(filename, "wb") as f:
            for data in response.iter_content(block_size):
                f.write(data)
                self.download_size = len(data)
    def __del__(self):
        del self.total_size
        del self.download_size
    def kb_total_size(self):
        return "{} KB".format(self.total_size % 1024)
    def kb_total_size(self):
        return "{} KB".format(self.download_size % 1024)
    def mb_total_size(self):
        return "{} MB".format(self.total_size % 1024 ** 2)
    def mb_total_size(self):
        return "{} MB".format(self.download_size % 1024 ** 2)
    def gb_total_size(self):
        return "{} GB".format(self.total_size % 1024 ** 3)
    def gb_total_size(self):
        return "{} GB".format(self.download_size % 1024 ** 3)
# class multi_downloader:
#     def __init__(self, urls: List[Tuple[str, str]], max_workers: int = 4, chunk_size: int = 8192):
#         # 多线程下载器
#         # 属性 urls: 列表，元素为 (url, filename) 的元组。
#         # 属性 max_workers: 最大并发线程数。
#         # 属性 chunk_size: 每次写入磁盘的字节大小。
#         self.urls = urls
#         self.max_workers = max_workers
#         self.chunk_size = chunk_size
#         # 内部状态变量
#         self.__downloaded_size = 0
#         self.__total_size = 0
#         self.__lock = Lock()            # 线程锁，确保并发更新变量时的安全性
#         # 初始化时计算总大小
#         self.__calculate_total_size()
#     @property                           # 将方法伪装成属性，防止篡改 _downloaded_size
#     def downloaded_size(self) -> int:
#         # 已下载大小（字节）
#         return self.__downloaded_size
#     @property
#     def total_size(self) -> int:
#         # 总大小（字节）
#         return self.__total_size
#     def __calculate_total_size(self):
#         # 通过 HEAD 请求获取所有文件的总大小
#         for url, _ in self.urls:
#             try:
#                 resp = requests.head(url, timeout=10)
#                 content_length = resp.headers.get('Content-Length')
#                 if content_length:
#                     self.__total_size += int(content_length)
#             except Exception:
#                 pass                    # 如果无法获取大小，则保持为 0
#     def __download_single(self, url: str, filename: str):
#         # 下载单个文件并更新已下载大小
#         try:
#             response = requests.get(url, stream=True, timeout=30)
#             response.raise_for_status()
#             with open(filename, 'wb') as f:
#                 for chunk in response.iter_content(chunk_size=self.chunk_size):
#                     if chunk:
#                         f.write(chunk)
#                         # 线程安全地更新已下载大小
#                         with self.__lock:
#                             self.__downloaded_size += len(chunk)
#         except Exception as e:
#             print(f"\n[错误] 下载 {url} 失败: {e}")
#     def start(self) -> dict:
#         # 启动多线程下载，返回下载结果字典
#         results = {}
#         with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
#             future_to_url = {
#                 executor.submit(self._download_single, url, name): name 
#                 for url, name in self.urls
#             }
#             for future in as_completed(future_to_url):
#                 filename = future_to_url[future]
#                 try:
#                     future.result()
#                     results[filename] = True
#                 except Exception as e:
#                     results[filename] = False
#         return results