import pygame, logging, json, os, time, launcher_data, minecraft_operator, threading, pyperclip, download_files, random, math, icon_drawer, io, subprocess, traceback, sys, ctypes, tempfile
import requests as web
from standard_service import colour
from PIL import Image, ImageFont
from changing_variable_type import pillow_to_pygame
from minecraft_operator import mc_color
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import *
from easygui import fileopenbox, filesavebox

logging._levelToName = {
    logging.CRITICAL: "FATAL",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARN",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
    logging.NOTSET: "NOTSET"
}

def override(file: io.TextIOWrapper, value: str):
    file.truncate(0)
    file.seek(0)
    return file.write(value)
def is_all_ascii(string: str) -> bool:
    for i in string:
        if ord(i) > 127:
            return False
    return True
def build_uuid() -> str:
    return "00534c43-{0}-4fff-bfff-{1}".format(eval("+".join(["hex(random.randint(0, 15))[2]"] * 4)), eval("+".join(["hex(random.randint(0, 15))[2]"] * 12)))
def get_config(key: str, default = None, logger_recording = True):
    config = open("config/launcher.json", mode="r", encoding="utf-8")
    config.seek(0)
    config_data = json.load(config)
    if logger_recording:
        logger.info("Loaded configure: {}".format(config_data))
    config.close()
    if key in config_data:
        if logger_recording:
            logger.info("Key for {0} -> \"{1}\"".format(key, config_data[key]))
        return config_data[key]
    else:
        if logger_recording:
            logger.info("Key for {0} -> undefined".format(key))
        # return minecraft_operator.config.basic_config[key]
        return default
def set_config(key: str, value, logger_recording = True):
    global logger
    config = open("config/launcher.json", mode="r+", encoding="utf-8")
    config.seek(0)
    # if logger_recording:
    #     logger.debug("Configure: {}".format(config.read()))
    config.seek(0)
    original_config_data: dict = json.loads(config.read())
    config_data = original_config_data.copy()
    config_data[key] = value
    config_string = json.dumps(config_data, ensure_ascii=False, indent=4)
    # if logger_recording:
    #     logger.debug("New configure: {}".format(config_string))
    byte_sum = override(config, config_string)
    if logger_recording:
        logger.info("Changed configure: {0} -> {1}".format(original_config_data, config_data))
    if logger_recording:
        logger.debug("Written: {}".format(byte_sum))
    config.close()
def get_game_config(key: str, default = None, logger_recording = True):
    game_config = open("config/game.json", mode="r", encoding="utf-8")
    game_config.seek(0)
    game_config_data = json.load(game_config)
    if logger_recording:
        logger.info("Loaded configure: {}".format(game_config_data))
    game_config.close()
    if key in game_config_data:
        if logger_recording:
            logger.info("Key for {0} -> \"{1}\"".format(key, game_config_data[key]))
        return game_config_data[key]
    else:
        if logger_recording:
            logger.info("Key for {0} -> undefined".format(key))
        # return minecraft_operator.config.basic_config[key]
        return default
def set_game_config(key: str, value, logger_recording = True):
    global logger
    game_config = open("config/game.json", mode="r+", encoding="utf-8")
    game_config.seek(0)
    # if logger_recording:
    #     logger.debug("Configure: {}".format(game_config.read()))
    game_config.seek(0)
    game_original_config_data: dict = json.loads(game_config.read())
    game_config_data = game_original_config_data.copy()
    game_config_data[key] = value
    game_config_string = json.dumps(game_config_data, ensure_ascii=False, indent=4)
    # if logger_recording:
    #     logger.debug("New configure: {}".format(game_config_string))
    byte_sum = override(game_config, game_config_string)
    if logger_recording:
        logger.info("Changed configure: {0} -> {1}".format(game_original_config_data, game_config_data))
    if logger_recording:
        logger.debug("Written: {}".format(byte_sum))
    game_config.close()
def get_account_config(logger_recording = True) -> list:
    account_config = open("config/account.json", mode="r", encoding="utf-8")
    account_config.seek(0)
    account_config_data = json.load(account_config)
    if logger_recording:
        logger.info("Loaded configure: {}".format(account_config_data))
    account_config.close()
    return account_config_data
def set_account_config(index: int, value, logger_recording = True):
    global logger
    account_config = open("config/account.json", mode="r+", encoding="utf-8")
    account_config.seek(0)
    # if logger_recording:
    #     logger.debug("Configure: {}".format(account_config.read()))
    account_config.seek(0)
    account_original_config_data: list = json.loads(account_config.read())
    account_config_data = account_original_config_data.copy()
    account_config_data[index] = value
    account_config_string = json.dumps(account_config_data, ensure_ascii=False, indent=4)
    # if logger_recording:
    #     logger.debug("New configure: {}".format(account_config_string))
    byte_sum = override(account_config, account_config_string)
    if logger_recording:
        logger.info("Changed configure: {0} -> {1}".format(account_original_config_data, account_config_data))
    if logger_recording:
        logger.debug("Written: {}".format(byte_sum))
    account_config.close()
def append_account_config(value, logger_recording = True):
    global logger
    account_config = open("config/account.json", mode="r+", encoding="utf-8")
    account_config.seek(0)
    # if logger_recording:
    #     logger.debug("Configure: {}".format(account_config.read()))
    account_config.seek(0)
    account_original_config_data: list = json.loads(account_config.read())
    account_config_data = account_original_config_data.copy()
    account_config_data.append(value)
    account_config_string = json.dumps(account_config_data, ensure_ascii=False, indent=4)
    # if logger_recording:
    #     logger.debug("New configure: {}".format(account_config_string))
    byte_sum = override(account_config, account_config_string)
    if logger_recording:
        logger.info("Changed configure: {0} -> {1}".format(account_original_config_data, account_config_data))
    if logger_recording:
        logger.debug("Written: {}".format(byte_sum))
    account_config.close()
def remove_account_config(index: int, logger_recording = True):
    global logger
    account_config = open("config/account.json", mode="r+", encoding="utf-8")
    account_config.seek(0)
    # if logger_recording:
    #     logger.debug("Configure: {}".format(account_config.read()))
    account_config.seek(0)
    account_original_config_data: list = json.loads(account_config.read())
    account_config_data = account_original_config_data.copy()
    del account_config_data[index]
    account_config_string = json.dumps(account_config_data, ensure_ascii=False, indent=4)
    # if logger_recording:
    #     logger.debug("New configure: {}".format(account_config_string))
    byte_sum = override(account_config, account_config_string)
    if logger_recording:
        logger.info("Changed configure: {0} -> {1}".format(account_original_config_data, account_config_data))
    if logger_recording:
        logger.debug("Written: {}".format(byte_sum))
    account_config.close()
def get_account_enabled(logger_recording = True):
    global logger
    account_config = open("config/account.json", mode="r", encoding="utf-8")
    account_config.seek(0)
    result_data = dict()
    if logger_recording:
        logger.debug("Configure: {}".format(account_config.read()))
    for i in json.load(account_config):
        if bool(i["enabled"]):
            if i["type"] in result_data:
                if logger_recording:
                    logger.warning("Multiple enabled account of \"{}\"".format(i["type"]))
            else:
                result_data[i["type"]] = i
    return result_data
def string_remove_index(string: str, index: int) -> str:
    # 正数、负数都适用
    return string[0:index] + string[index + 1:]
def string_insert_index(string: str, index: int, character: str) -> str:
    # 正数、负数都适用
    return string[0:index] + character + string[index:]
def truncate_string(string: str, size: int, overback = "...") -> str:
    return string[0:size] + overback if size < len(string) else string
def random_boolean() -> bool:
    return bool(random.randint(0, 1))
def get_version_array():
    global logger, version_array
    try:
        version_array = web.get("https://piston-meta.mojang.com/mc/game/version_manifest.json").json()
    except:
        logger.error("Falied to load the version array")
        version_array = {"versions": [{"id": "无法打开版本列表"}]}
def position_in_rect(position: tuple, left: int, top: int, width: int, height: int):
    return position[0] >= left and position[0] < left + width and position[1] >= top and position[1] < top + height
def inputting(event):
    global input_text, inputting_text_cursor_location
    key_value: int = event.key
    key_name = pygame.key.name(key_value)
    if key_value == pygame.K_RETURN or key_value == pygame.K_KP_ENTER:
        logger.info("Input \"{}\"".format(input_text))
        options["input_form"] = 0
        input_text = ""
    elif key_value == pygame.K_BACKSPACE:
        if inputting_text_cursor_location > 0:
            input_text = string_remove_index(input_text, inputting_text_cursor_location - 1)
            inputting_text_cursor_location -= 1
    elif key_value == pygame.K_DELETE:
        if inputting_text_cursor_location < len(input_text):
            input_text = string_remove_index(input_text, inputting_text_cursor_location)
    elif key_value == pygame.K_INSERT:
        input_text = string_insert_index(input_text, inputting_text_cursor_location, pyperclip.paste())
        inputting_text_cursor_location += len(pyperclip.paste())
    elif key_value == pygame.K_SPACE or key_value == pygame.K_TAB:
        input_text = string_insert_index(input_text, inputting_text_cursor_location, " ")
        inputting_text_cursor_location += 1
    elif key_value == pygame.K_ESCAPE:
        options["input_form"] = 0
    elif key_value == pygame.K_LEFT and inputting_text_cursor_location > 0:
        inputting_text_cursor_location -= 1
    elif key_value == pygame.K_RIGHT and inputting_text_cursor_location < len(input_text):
        inputting_text_cursor_location += 1
    elif key_value == pygame.K_UP or key_value == pygame.K_HOME:
        inputting_text_cursor_location = 0
    elif key_value == pygame.K_DOWN or key_value == pygame.K_END:
        inputting_text_cursor_location = len(input_text)
    else:
        input_text = string_insert_index(input_text, inputting_text_cursor_location, event.unicode)
        inputting_text_cursor_location += 1
def get_forms(key: str) -> str:
    global forms
    if key in forms:
        return forms[key]
    else:
        return str()
def should_render_display_page(page_number: int) -> bool:
    global options, choosing_page, PAGE_OF_THINKING
    return (choosing_page == PAGE_OF_THINKING and options["thinking_page"] == page_number) or choosing_page == page_number
# region
# def download_minecraft_file_json_method():
#     global choosing_version_url
#     choosing_version_json_data = web.get(choosing_version_url).json()
#     choosing_version_jar_data = web.get(choosing_version_json_data["downloads"]["client"]).content
#     version_name = get_forms("version_name")
#     if not os.path.isdir(version_name):
#         os.mkdir(version_name)
#         choosing_version_json_data_file = open("{0}/{0}.json".format(version_name), mode="w")
#         choosing_version_json_data_file.write(json.dumps(choosing_version_json_data, indent=4))
#         choosing_version_json_data_file.close()
#         choosing_version_jar_data_file = open("{0}/{0}.jar".format(version_name), mode="wb")
#         choosing_version_jar_data_file.write(choosing_version_jar_data)
#         choosing_version_jar_data_file.close()
# endregion
def is_valiable_dir_name(dirname: str) -> bool:
    if dirname == "":
        return False
    if "*" in dirname:
        return False
    if "/" in dirname:
        return False
    if "\\" in dirname:
        return False
    if "?" in dirname:
        return False
    if ":" in dirname:
        return False
    if "<" in dirname:
        return False
    if ">" in dirname:
        return False
    if "\"" in dirname:
        return False
    if "|" in dirname:
        return False
    if dirname[-1] == ".":
        return False
    if dirname[-1] == " ":
        return False
    if dirname.lower() == "con":
        return False
    if dirname.lower() == "prn":
        return False
    if dirname.lower() == "aux":
        return False
    if dirname.lower() == "nul":
        return False
    if len(dirname) == 4:
        if (dirname[0:3].lower() == "com" or dirname[0:3].lower() == "lpt") and dirname[3].isdigit():
            return False
    if os.path.isdir(dirname):
        return False
    return True
def calculate_text_width(text: str, font_size: int, font_path: str) -> int:
    font = ImageFont.truetype(font_path, font_size)
    return int(font.getlength())
def get_command_output(command: str) -> str:
    os.system("{} > temp/command_output.txt".format(command))
    with open("temp/command_output.txt", mode="r") as file:
        result = file.read()
    return result
def add_menu(menu_name: str, id_num: int, chinese_font_choosing = True) -> None:
    global screen, font_data, chinese_character_font_data, position, position_in_rect, choosing_page, display_cursor_type
    if choosing_page == id_num:
        pygame.draw.rect(screen, colour.MediumSlateBlue, pygame.Rect(0, 35 * id_num + 35, 200, 35))
        font_choosing = chinese_character_font_data if chinese_font_choosing else font_data
        screen.blit(font_choosing.render(menu_name, True, colour.Black), (41, 35 * id_num + 42))
    else:
        font_choosing = chinese_character_font_data if chinese_font_choosing else font_data
        if position_in_rect(position, 0, 35 * id_num + 35, 200, 35):
            display_cursor_type = pygame.SYSTEM_CURSOR_HAND
            pygame.draw.rect(screen, colour.MediumSlateBlue, pygame.Rect(0, 35 * id_num + 35, 200, 35))
        screen.blit(font_choosing.render(menu_name, True, colour.White), (41, 35 * id_num + 42))
def find_version_in_array(version_array: list, version_name = str) -> dict:
    for i in version_array:
        if i["id"] == version_name:
            return i
    return dict()
def blit_inputting_text(form_name: str, position_x: int, position_y: int, valiable_condition = True, forced_using_chinese_font = True):
    global chinese_character_font_data, font_data, screen, string_insert_index, get_forms, inputting_text_cursor_location, options
    if form_name == "game_version_name":
        form_id = 1
    elif form_name == "player_name":
        form_id = 2
    if forced_using_chinese_font:
        text_render = chinese_character_font_data.render(string_insert_index(get_forms(form_name), inputting_text_cursor_location, "|") if (options["input_form"] == form_id and time.time() % 1 < 0.5) else get_forms(form_name), True, colour.Black if valiable_condition else colour.Red)
    else:
        text_render = font_data.render(string_insert_index(get_forms(form_name), inputting_text_cursor_location, "|") if (options["input_form"] == form_id and time.time() % 1 < 0.5) else get_forms(form_name), True, colour.Black if valiable_condition else colour.Red)
    screen.blit(text_render, (position_x, position_y))
# region
# def add_menu_squared(menu_name: str, id_num: int, chinese_font_choosing = True) -> None:
#     global screen, font_data, chinese_character_font_data, position, position_in_rect, choosing_page
#     if choosing_page == id_num:
#         pygame.draw.rect(screen, colour.Turquoise, pygame.Rect(-40 * id_num + 1240, 760, 40, 40))
#         font_choosing = chinese_character_font_data if chinese_font_choosing else font_data
#         screen.blit(font_choosing.render(menu_name, True, colour.Black), (1220 - 40 * id_num - 8 * len(menu_name), 772))
#     else:
#         font_choosing = chinese_character_font_data if chinese_font_choosing else font_data
#         if position_in_rect(position, -40 * id_num + 1240, 760, 40, 40):
#             pygame.draw.rect(screen, colour.Turquoise, pygame.Rect(-40 * id_num + 1240, 760, 40, 40))
#         screen.blit(font_choosing.render(menu_name, True, colour.Black), (1220 - 40 * id_num - 8 * len(menu_name), 772))
# def download_file(url: str, output_dir: str):
#     if not os.path.isdir(output_dir):
#         global logger
#         os.mkdir(output_dir)
#         logger.warning("Folder not found! Created {}".format(output_dir))
#     local_filename = os.path.join(output_dir, url.split("/")[-1])
#     response = web.get(url, stream=True)
#     with open(local_filename, 'wb') as file:
#         for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                 file.write(chunk)
#     return local_filename
# def download_files_concurrently(urls: list, output_dir: str, max_workers = 5):
#     os.makedirs(output_dir, exist_ok=True)
#     with ThreadPoolExecutor(max_workers) as executor:
#         futures = [executor.submit(download_file, url, output_dir) for url in urls]
#         for future in as_completed(futures):
#             print("Downloaded: {}".format(future.result()))
# endregion
def download_version_manifest_main():
    global logger, running_download_version_manifest
    running_download_version_manifest = True
    # version_manifest_downloader = multi_downloader(url)
    version_manifest = web.get("https://piston-meta.mojang.com/mc/game/version_manifest.json").json()
    version_manifest_string = json.dumps(version_manifest, ensure_ascii=False, indent=4)
    with open("temp/version_manifest_{}.json".format(time.strftime("%Y%j%H", time.localtime())), mode="w", encoding="utf-8") as file:
        file.write(version_manifest_string)
def download_version_manifest_callback(future):
    global recent_download_version_manifest_temporary, ran_download_version_manifest, logger
    recent_download_version_manifest_temporary = time.time()
    logger.info("Downloaded temp/version_manifest.json")
    ran_download_version_manifest = True
def download_version_manifest():
    download_version_manifest_main()
    download_version_manifest_callback()
# def current_thread_initializer():
#     threading.current_thread().daemon = True
def download_new_game_version_main(game_version: dict, version_name: str):
    global downloading_game_version
    downloading_game_version += 1
    if is_valiable_dir_name(version_name):
        try:
            os.mkdir(".minecraft/versions/" + version_name)
            version_json = web.get(game_version["url"]).json()
            version_json_string = json.dumps(version_json, ensure_ascii=False, indent=4)
            with open(".minecraft/versions/{0}/{0}.json".format(version_name), mode="w", encoding="utf-8") as file:
                file.write(version_json_string)
            version_jar = web.get(version_json["downloads"]["client"]["url"]).content
            with open(".minecraft/versions/{0}/{0}.jar".format(version_name), mode="wb") as file:
                file.write(version_jar)
        except Exception as error:
            logger.error("An error happened:\n{}".format(error))
    logger.info("Config game version")
    set_game_config(version_name, {"completed": False, "colour": colour.Black})
    set_config("choosing_version", version_name)
def download_new_game_version_callback(future):
    global logger, downloading_game_version
    logger.info("Downloaded game version")
    downloading_game_version -= 1
def download_new_game_version():
    download_new_game_version_main()
    download_new_game_version_callback(None)
def build_resource_necessary_main():
    global building_necessary_resource, building_resource_config_version_name
    building_necessary_resource = True
    minecraft_operator.launch.build_minecraft_libraries(building_resource_config_version_name, logger, True)
    minecraft_operator.launch.built_asset_files(building_resource_config_version_name, logger, True)
def build_resource_necessary_callback(future):
    global building_necessary_resource
    building_necessary_resource = False
def build_resource_necessary():
    build_resource_necessary_main()
    build_resource_necessary_callback(None)
def launch_minecraft_main():
    global version_name, minecraft_process, logger, building_necessary_resource, version_name
    building_necessary_resource = True
    minecraft_operator.launch.build_minecraft_libraries(version_name, logger, False)
    minecraft_operator.launch.built_asset_files(version_name, logger, False)
    building_necessary_resource = False
    try:
        set_game_config(version_name, {"completed": True, "colour": get_game_config(version_name)["colour"]})
        argument_array = minecraft_operator.launch.build_launch_bash_array(version_name, logger)
        if isinstance(argument_array, list):
            argument_value = minecraft_operator.launch.build_launch_bash_string(version_name, logger)
            logger.info("Ready to launch minecraft: {0}\nArgument array: {1}".format(version_name, argument_array))
            logger.debug("Argument string: {}".format(argument_value))
            minecraft_process = subprocess.Popen(argument_array, creationflags=subprocess.CREATE_NO_WINDOW, cwd=".")
            logger.info("Minecraft launched")
    except Exception as error:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        last_frame = traceback.extract_tb(exception_traceback)[-1]
        logger.error("An error happened at line {0} of {1}: type {2}, content: {3}".format(last_frame.lineno, os.path.basename(last_frame.filename), exception_type.__name__, error))

if not os.path.isdir(".minecraft"):
    os.mkdir(".minecraft")
if not os.path.isdir(".minecraft/versions"):
    os.mkdir(".minecraft/versions")

if not os.path.isdir("temp"):
    os.mkdir("temp")

if not os.path.isdir("logs"):
    os.mkdir("logs")
logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] [%(name)s/%(levelname)s] %(message)s", datefmt="%H:%M:%S", filename="logs/{}.log".format(time.strftime("%Y%j", time.localtime())), filemode="a")
logger = logging.getLogger("main")
logger.info("Beginning!")

if not os.path.isdir("icons"):
    os.mkdir("icons")
if not os.path.isfile("icons/icon.png"):
    icon = open("icons/icon.png", mode="wb")
    icon.write(launcher_data.icon)
    icon.close()
if not os.path.isfile("icons/icon.ico"):
    icon = open("icons/icon.ico", mode="wb")
    icon.write(launcher_data.icon_ico_file)
    icon.close()

if not os.path.isdir("config"):
    os.mkdir("config")
if not os.path.isfile("config/launcher.json"):
    config = open("config/launcher.json", mode="w")
    config.write("{}")
    config.close()
if not os.path.isfile("config/game.json"):
    config = open("config/game.json", mode="w")
    config.write("{}")
    config.close()
if not os.path.isfile("config/account.json"):
    config = open("config/account.json", mode="w")
    config.write("[]")
    config.close()

options = {
    "choosing_resource_number": 0,
    "choosing_setting_number": 0,
    "choosing_version_pages_index": 0,
    "editing_account_config": 0,
    "input_form": 0,
    "opening_menu": False,
    "pages": [
        0
    ],
    "pages_index": 0,
    "thinking_page": 0
}
resource_display_array = [
    "首页",
    "官方",
    "加载器",
    "模组",
    "数据包",
    "资源包",
    "光影"
]
setting_display_array = [
    "启动",
    "程序",
    "账号",
    "实例"
]

PAGE_OF_VERSION_DOWNLOAD = -1
PAGE_OF_VERSION_CHOOSING = -2
PAGE_OF_THINKING = -65536
ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION = 26
ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION = 28
forms = {}
choosing_page = 0
# build_resource_necessary_calculating_thread = None
# choosing_page_detail = 0
# downloading_game_version = list()
chosen_game_version_in_download_page = dict()
running_download_version_manifest = False
minecraft_process = None
game_version_total_pages = 0
game_version_total = 0
inputting_text_cursor_location = 0
downloading_game_version = 0
building_necessary_resource = False
launching_game_step = 0                                                 # 0表示空闲，即没有进行启动操作
config_version_name = str()
building_resource_config_version_name = str()
pygame.init()
looping = True
large_font_data = pygame.font.SysFont(["Arial", "SimHei", "黑体", "微软雅黑", "Noto Sans SC"], 32)
font_data = pygame.font.SysFont(["Arial", "SimHei", "黑体", "微软雅黑", "Noto Sans SC"], 16)
chinese_character_font_data = pygame.font.SysFont(["SimHei", "黑体", "微软雅黑", "Noto Sans SC"], 16)
chinese_character_font_data_small = pygame.font.SysFont(["SimHei", "黑体", "微软雅黑", "Noto Sans SC"], 12)
chinese_character_font_data_tiny = pygame.font.SysFont(["SimHei", "黑体", "微软雅黑", "Noto Sans SC"], 8)
chinese_character_font_data_large = pygame.font.SysFont(["SimHei", "黑体", "微软雅黑", "Noto Sans SC"], 24)
chinese_character_font_data_huge = pygame.font.SysFont(["SimHei", "黑体", "微软雅黑", "Noto Sans SC"], 32)
title_value = "Plain Collection Launcher"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("stonal.stonals-launcher-collection.main.{}".format(minecraft_operator.config.basic_config["launcher_version"]))
text_title = font_data.render("Stonal's Laucher Collection", True, colour.White)
pygame.display.set_caption("Stonal's Laucher Collection")
screen = pygame.display.set_mode((1200, 800), pygame.NOFRAME | pygame.HWSURFACE | pygame.SHOWN)
icon = pillow_to_pygame(Image.open("icons/icon.png")).convert_alpha()
pygame.display.set_icon(icon)
# 加载图标
# hicon = win32gui.LoadImage(None, "icon.ico", win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE)
# hwnd = win32gui.GetForegroundWindow()
# win32gui.SetClassLong(hwnd, win32con.GCL_HICON, hicon)
# logger.info("Icon loaded: {}".format(icon.get_size()))
# while not icon:
#     logger.info("Icon loaded: {}".format(icon.get_size()))
#     icon = pillow_to_pygame(Image.open("icons/icon.ico")).convert_alpha()
# if sys.platform == "win32":
#     try:
#         # 获取窗口句柄
#         hwnd = pygame.display.get_wm_info()["window"]
#         user32 = ctypes.windll.user32
#         # 从外部 .ico 文件加载 (备选)
#         icon_handle = user32.LoadImageW(0, "./icons/icon.ico", 1, 0, 0, 0x10)
#         # 发送 WM_SETICON 消息
#         if icon_handle:
#             # ICON_SMALL = 0, WM_SETICON = 0x0080
#             user32.SendMessageW(hwnd, 0x0080, 0, icon_handle)
#             user32.SendMessageW(hwnd, 0x0080, 1, icon_handle)
#         else:
#             logger.warning("Failed to load icon: {}".format(e))
#     except Exception as e:
#         logger.error("Failed to set taskbar icon: {}".format(e))
screen.fill(colour.White)
recent_download_version_manifest_temporary: float = 0
ran_download_version_manifest = True
if len(os.listdir("temp")) > 1:
    recent_download_version_manifest_temporary_file_name = max(os.listdir("temp"))
    recent_download_version_manifest_temporary_time_number = recent_download_version_manifest_temporary_file_name[17:26]
    recent_download_version_manifest_temporary = time.mktime(time.strptime(recent_download_version_manifest_temporary_time_number, "%Y%j%H"))
# version_manifest_downloader: multi_downloader = None                  # 先声明后定义
# download_version_manifest()
thread_pool_executor = ThreadPoolExecutor(max_workers=8)
version_name = get_config("choosing_version", None)
try:
    while looping:
        screen.fill(colour.White)
        position = pygame.mouse.get_pos()
        display_cursor_type = pygame.SYSTEM_CURSOR_ARROW
        pygame.draw.rect(screen, colour.SlateBlue, pygame.Rect(0, 0, 1200, 35))
        choosing_menu = pygame.Surface((40, 35))
        choosing_menu.fill(colour.MediumSlateBlue)
        if position_in_rect(position, 0, 0, 40, 35):
            # 菜单高亮
            screen.blit(choosing_menu, (0, 0))
            display_cursor_type = pygame.SYSTEM_CURSOR_HAND
        if position_in_rect(position, 1080, 0, 40, 35):
            # 思索
            # screen.blit(choosing_menu, (1080, 0))
            pass
        if position_in_rect(position, 1120, 0, 40, 35):
            # 最小化
            screen.blit(choosing_menu, (1120, 0))
        if position_in_rect(position, 1160, 0, 40, 35):
            # 关闭
            screen.blit(choosing_menu, (1160, 0))
        # 四个方格 40×35
        pygame.draw.line(screen, colour.DarkSlateBlue, (12, 12), (28, 12))
        pygame.draw.line(screen, colour.DarkSlateBlue, (12, 18), (28, 18))
        pygame.draw.line(screen, colour.DarkSlateBlue, (12, 24), (28, 24))
        pygame.draw.line(screen, colour.DarkSlateBlue, (1132, 18), (1148, 18))
        pygame.draw.line(screen, colour.DarkSlateBlue, (1174, 12), (1186, 24))
        pygame.draw.line(screen, colour.DarkSlateBlue, (1174, 24), (1186, 12))
        # pygame.draw.line(screen, colour.DarkSlateBlue, (1090, 10), (1090, 20))
        # pygame.draw.line(screen, colour.DarkSlateBlue, (1100, 15), (1100, 25))
        # pygame.draw.line(screen, colour.DarkSlateBlue, (1110, 10), (1110, 20))
        # pygame.draw.line(screen, colour.DarkSlateBlue, (1090, 10), (1100, 15))
        # pygame.draw.line(screen, colour.DarkSlateBlue, (1090, 20), (1100, 25))
        # pygame.draw.line(screen, colour.DarkSlateBlue, (1110, 10), (1100, 15))
        # pygame.draw.line(screen, colour.DarkSlateBlue, (1110, 20), (1100, 25))
        # 菜单
        if options["opening_menu"]:
            pygame.draw.rect(screen, colour.DarkSlateBlue, pygame.Rect(0, 35, 200, 765))
            add_menu("Minecraft", 0, False)                                 # 正数显示，负数不显示
            add_menu("设置", 1)
            add_menu("资源", 2)
            add_menu("程序", 3)
            add_menu("视频", 4)
        # 标题
        screen.blit(text_title, (49, 9))
        # 各个标签
        if should_render_display_page(0):
            # Minecraft
            if options["opening_menu"]:
                if position_in_rect(position, 200, 760, 500, 40):
                    pygame.draw.rect(screen, colour.Turquoise, pygame.Rect(200, 760, 500, 40))
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                else:
                    pygame.draw.rect(screen, colour.DarkTurquoise, pygame.Rect(200, 760, 500, 40))
                if position_in_rect(position, 700, 760, 500, 40):
                    pygame.draw.rect(screen, colour.MediumSlateBlue, pygame.Rect(700, 760, 500, 40))
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                else:
                    pygame.draw.rect(screen, colour.SlateBlue, pygame.Rect(700, 760, 500, 40))
                screen.blit(chinese_character_font_data.render("启动游戏", True, colour.White), (212, 772))
                screen.blit(chinese_character_font_data.render("版本选择", True, colour.White), (712, 772))
            else:
                if position_in_rect(position, 0, 760, 600, 40):
                    pygame.draw.rect(screen, colour.Turquoise, pygame.Rect(0, 760, 600, 40))
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                else:
                    pygame.draw.rect(screen, colour.DarkTurquoise, pygame.Rect(0, 760, 600, 40))
                if position_in_rect(position, 600, 760, 600, 40):
                    pygame.draw.rect(screen, colour.MediumSlateBlue, pygame.Rect(600, 760, 600, 40))
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                else:
                    pygame.draw.rect(screen, colour.SlateBlue, pygame.Rect(600, 760, 600, 40))
                screen.blit(chinese_character_font_data.render("启动游戏", True, colour.White), (12, 772))
                screen.blit(chinese_character_font_data.render("版本选择", True, colour.White), (612, 772))
            screen.blit(chinese_character_font_data.render("账号", True, colour.Black), (int(options["opening_menu"]) * 200 + 10, 52))
            if position_in_rect(position, int(options["opening_menu"]) * 200 + 50, 45, 1140 - int(options["opening_menu"]) * 200, 30):
                display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(int(options["opening_menu"]) * 200 + 50, 45, 1140 - int(options["opening_menu"]) * 200, 30))
            pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(int(options["opening_menu"]) * 200 + 50, 45, 1140 - int(options["opening_menu"]) * 200, 30), 1)
            screen.blit(chinese_character_font_data.render("账号设置", True, colour.Black), (int(options["opening_menu"]) * 100 + 588, 52))
            # add_menu_squared("下载", 0)
            if downloading_game_version > 0:
                screen.blit(chinese_character_font_data.render("有{}个版本正在下载中".format(downloading_game_version), True, colour.Black), (int(options["opening_menu"]) * 200 + 7, 714))
            if building_necessary_resource:
                screen.blit(chinese_character_font_data.render("正在补全文件...", True, colour.Black), (int(options["opening_menu"]) * 200 + 7, 691 if downloading_game_version > 0 else 714))
                # region
                # # 如果计算线程未启动或已完成，则重新启动（每帧获取最新进度）
                # if build_resource_necessary_calculating_thread is None or build_resource_necessary_calculating_thread.done():
                #     build_resource_necessary_calculating_thread = thread_pool_executor.submit(minecraft_operator.launch.build_resource_necessary_calculating, building_resource_config_version_name)
                # # 若线程已完成，取出结果并显示
                # if build_resource_necessary_calculating_thread.done():
                #     try:
                #         gotten = build_resource_necessary_calculating_thread.result()
                #         # gotten 是四元组：(已下载库数, 总库数, 已下载资源数, 总资源数)
                #         libs_done, libs_total, assets_done, assets_total = gotten
                #         libs_str = "{0}/{1}".format(libs_done, libs_total) if libs_total > 0 else "N/A"
                #         assets_str = "{0}/{1}".format(assets_done, assets_total) if assets_total > 0 else "N/A"
                #         downloading_resource_tip = "补全文件中：依赖模块 {0}，资源文件 {1}".format(libs_str, assets_str)
                #         screen.blit(chinese_character_font_data.render(downloading_resource_tip, True, colour.Black), (int(options["opening_menu"]) * 200 + 7, 691 if downloading_game_version > 0 else 714))
                #     except Exception as err:
                #         logger.error("Failed to get the process: {}".format(err))
                # else:
                #     screen.blit(chinese_character_font_data.render("正在补全文件...", True, colour.Black), (int(options["opening_menu"]) * 200 + 7, 691 if downloading_game_version > 0 else 714))
                # endregion
            if choosing_page != PAGE_OF_THINKING:
                HOMEPAGE_Y_BEGIN = 75
                screen.blit(font_data.render("Minecraft: Java Edition / MC-276156", True, colour.Black), (int(options["opening_menu"]) * 200 + 7, HOMEPAGE_Y_BEGIN + 7))
                screen.blit(font_data.render("minecraft java should sign up for free not needed for buy this mean hell to cracked players", True, colour.Black), (int(options["opening_menu"]) * 200 + 7, HOMEPAGE_Y_BEGIN + 37))
                screen.blit(chinese_character_font_data.render("译：Java版Minecraft应当免费而不是付费注册，这对疯狂的玩家来说就是地狱", True, colour.Black), (int(options["opening_menu"]) * 200 + 7, HOMEPAGE_Y_BEGIN + 67))
            if len(os.listdir("temp")) > 1:
                screen.blit(chinese_character_font_data.render("选择的版本：{}".format(get_config("choosing_version", max(os.listdir(".minecraft/versions")), False)), True, colour.Black), (int(options["opening_menu"]) * 200 + 7, 737))
        if choosing_page == 1:
            # 设置
            opening = int(options["opening_menu"]) * 200
            pygame.draw.rect(screen, colour.DarkTurquoise, pygame.Rect(opening, 35, 1200 - opening, 35))
            for i in range(len(setting_display_array)):
                if position_in_rect(position, opening + 100 * i, 35, 100, 35) or i == options["choosing_setting_number"]:
                    pygame.draw.rect(screen, colour.Turquoise, pygame.Rect(opening + 100 * i, 35, 100, 35))
                if position_in_rect(position, opening + 100 * i, 35, 100, 35):
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                screen.blit(chinese_character_font_data.render(setting_display_array[i], True, colour.Black if options["choosing_setting_number"] == i else colour.White), (opening + 100 * i + 9, 44))
            if options["choosing_setting_number"] == 0:
                pass
            elif options["choosing_setting_number"] == 1:
                screen.blit(chinese_character_font_data.render("Java程序", True, colour.Black), (opening + 10, 87))
                if position_in_rect(position, 1160, 80, 30, 30):
                    pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(1160, 80, 30, 30))
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(opening + 90, 80, 1070 - opening, 30), 1)
                icon_drawer.draw_icon_folder(screen, colour.Gainsboro, 1165, 85)
                # get_command_output("java --version").split()[1]
            elif options["choosing_setting_number"] == 2:
                opening = int(options["opening_menu"]) * 200
                pygame.draw.rect(screen, colour.LawnGreen if position_in_rect(position, opening, 70, 30, 30) else colour.LimeGreen, pygame.Rect(opening, 70, 30, 30))
                pygame.draw.rect(screen, colour.White, pygame.Rect(opening + 5, 75, 20, 20), 1)
                pygame.draw.rect(screen, colour.White, pygame.Rect(opening + 10, 84, 10, 2))
                pygame.draw.rect(screen, colour.White, pygame.Rect(opening + 14, 80, 2, 10))
                pygame.draw.rect(screen, colour.LawnGreen if position_in_rect(position, opening + 30, 70, 30, 30) else colour.LimeGreen, pygame.Rect(opening + 30, 70, 30, 30))
                pygame.draw.ellipse(screen, colour.White, pygame.Rect(opening + 35, 75, 20, 20), 1)
                pygame.draw.rect(screen, colour.White, pygame.Rect(opening + 40, 84, 10, 2))
                pygame.draw.rect(screen, colour.White, pygame.Rect(opening + 44, 80, 2, 10))
                pygame.draw.rect(screen, colour.LawnGreen if position_in_rect(position, opening + 60, 70, 30, 30) else colour.LimeGreen, pygame.Rect(opening + 60, 70, 30, 30))
                pygame.draw.rect(screen, colour.White, pygame.Rect(opening + 65, 80, 20, 15), 1)
                pygame.draw.line(screen, colour.White, (opening + 67, 75), (opening + 72, 80))
                pygame.draw.line(screen, colour.White, (opening + 82, 75), (opening + 77, 80))
                pygame.draw.line(screen, colour.White, (opening + 69, 84), (opening + 69, 90))
                pygame.draw.line(screen, colour.White, (opening + 80, 84), (opening + 80, 90))
                pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(opening + 90, 70, 1110 - opening, 30))
                pygame.draw.rect(screen, colour.DarkOrange, pygame.Rect(opening, 100, 90, 400))
                if position_in_rect(position, opening, 70, 30, 30):
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                    pygame.draw.rect(screen, colour.Orange, pygame.Rect(opening, 100, 30, 400))
                    screen.blit(chinese_character_font_data.render("Minecraft离线账号", True, colour.Black), (opening + 97, 77))
                if position_in_rect(position, opening + 30, 70, 30, 30):
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                    pygame.draw.rect(screen, colour.Orange, pygame.Rect(opening + 30, 100, 30, 400))
                    screen.blit(chinese_character_font_data.render("Minecraft正版账号", True, colour.Black), (opening + 97, 77))
                if position_in_rect(position, opening + 60, 70, 30, 30):
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                    pygame.draw.rect(screen, colour.Orange, pygame.Rect(opening + 60, 100, 30, 400))
                    screen.blit(chinese_character_font_data.render("哔哩哔哩账号", True, colour.Black), (opening + 97, 77))
                pygame.draw.rect(screen, colour.Turquoise, pygame.Rect(opening, 500, 1200 - opening, 30))
                account_type_number = ["minecraft_legacy", "microsoft_account", "bilibili_account"]
                for i in range(len(get_account_config(False))):
                    account = get_account_config(False)[i]
                    if "type" not in account or "enabled" not in account:
                        logger.warning("An invalid account \"{}\", which was ignored".format(account))
                        continue
                    if account["type"] in account_type_number:
                        display_location_x = account_type_number.index(account["type"]) * 30 + opening
                        display_location_y = i * 30 + 100
                        display_location_rect = pygame.Rect(display_location_x, display_location_y, 30, 30)
                        if options["editing_account_config"] == i + 1:
                            display_location_chosen = colour.Red
                        else:
                            display_location_chosen = colour.OrangeRed
                        pygame.draw.rect(screen, display_location_chosen, display_location_rect)
                        if account["enabled"]:
                            display_location_enabled = pygame.Rect(display_location_x + 5, display_location_y + 5, 20, 20)
                            pygame.draw.rect(screen, colour.White, display_location_enabled)
                        if position_in_rect(position, 1170, display_location_y, 30, 30):
                            display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                        pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(1170, display_location_y, 30, 30))
                        pygame.draw.rect(screen, colour.Silver, pygame.Rect(1174, display_location_y + 14, 2, 2))
                        pygame.draw.rect(screen, colour.Silver, pygame.Rect(1184, display_location_y + 14, 2, 2))
                        pygame.draw.rect(screen, colour.Silver, pygame.Rect(1194, display_location_y + 14, 2, 2))
                        if account["type"] == account_type_number[0]:
                            user_name_surface = chinese_character_font_data.render(account["user"], True, colour.Black)
                            screen.blit(user_name_surface, (opening + 97, display_location_y + 7))
                    else:
                        logger.warning("An invalid account type \"{}\", which was ignored".format(account["type"]))
                if options["editing_account_config"] == 0:
                    screen.blit(chinese_character_font_data.render("点击账号右侧的按钮进行设置", True, colour.Black), (opening + 7, 537))
                else:
                    editing_account = get_account_config(False)[options["editing_account_config"] - 1]
                    if editing_account["type"] == account_type_number[0]:
                        screen.blit(chinese_character_font_data.render("玩家名", True, colour.Black), (opening + 10, 547))
                        pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(opening + 70, 540, 1120 - opening, 30), 1)
                        blit_inputting_text("player_name", opening + 77, 547, get_forms("player_name").replace("_", "").isalnum(), False)
                        if position_in_rect(position, opening + 70, 540, 1120 - opening, 30):
                            display_cursor_type = pygame.SYSTEM_CURSOR_IBEAM
                        if position_in_rect(position, opening + 10, 580, 1180 - opening, 30):
                            display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                            pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(opening + 10, 580, 1180 - opening, 30))
                        pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(opening + 10, 580, 1180 - opening, 30), 1)
                        screen.blit(chinese_character_font_data.render("确认", True, colour.Black), (0.5 * opening + 584, 587))
                        if position_in_rect(position, opening + 10, 620, 1180 - opening, 30):
                            display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                            pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(opening + 10, 620, 1180 - opening, 30))
                        pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(opening + 10, 620, 1180 - opening, 30), 1)
                        screen.blit(chinese_character_font_data.render("选中", True, colour.Black), (0.5 * opening + 584, 627))
                        if position_in_rect(position, opening + 10, 660, 1180 - opening, 30):
                            display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                            pygame.draw.rect(screen, colour.Pink, pygame.Rect(opening + 10, 660, 1180 - opening, 30))
                            display_colour_delete = colour.DarkRed
                        else:
                            display_colour_delete = colour.Red
                        pygame.draw.rect(screen, colour.Red, pygame.Rect(opening + 10, 660, 1180 - opening, 30), 1)
                        screen.blit(chinese_character_font_data.render("删除", True, display_colour_delete), (0.5 * opening + 584, 667))
            elif options["choosing_setting_number"] == 3:
                opening = int(options["opening_menu"]) * 200
                if position_in_rect(position, opening + 10, 80, 200, 30):
                    display_cursor_type = pygame.SYSTEM_CURSOR_NO if building_necessary_resource else pygame.SYSTEM_CURSOR_HAND
                    pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(opening + 10, 80, 190, 30))
                pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(opening + 10, 80, 190, 30), 1)
                screen.blit(chinese_character_font_data.render("补全依赖库", True, colour.Black), (opening + 65, 87))
        if choosing_page == 2:
            # 资源
            opening = int(options["opening_menu"]) * 200
            pygame.draw.rect(screen, colour.DarkTurquoise, pygame.Rect(opening, 35, 1200 - opening, 35))
            for i in range(len(resource_display_array)):
                if position_in_rect(position, opening + 100 * i, 35, 100, 35) or i == options["choosing_resource_number"]:
                    pygame.draw.rect(screen, colour.Turquoise, pygame.Rect(opening + 100 * i, 35, 100, 35))
                if position_in_rect(position, opening + 100 * i, 35, 100, 35):
                    display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                screen.blit(chinese_character_font_data.render(resource_display_array[i], True, colour.Black if options["choosing_resource_number"] == i else colour.White), (opening + 100 * i + 9, 44))
            if time.time() - recent_download_version_manifest_temporary >= 3600 and not running_download_version_manifest:
                download_version_manifest_thread = thread_pool_executor.submit(download_version_manifest_main)
                download_version_manifest_thread.add_done_callback(download_version_manifest_callback)
            if options["choosing_resource_number"] == 0:
                if len(os.listdir("temp")) > 1:
                    recent_download_version_manifest_temporary_file_name = "temp/" + max(list(set(os.listdir("temp")).symmetric_difference({"command_output.txt"})))
                    recent_download_version_manifest_temporary_file_class = open(recent_download_version_manifest_temporary_file_name, encoding="utf-8", mode="r")
                    recent_download_version_manifest_content: dict = json.load(recent_download_version_manifest_temporary_file_class)
                    screen.blit(chinese_character_font_data.render("最新版本", True, colour.Black), (10 + int(options["opening_menu"]) * 200, 80))
                    if "release" in recent_download_version_manifest_content["latest"]:
                        if position_in_rect(position, int(options["opening_menu"]) * 200, 101, 1200 - int(options["opening_menu"]) * 200, 26):
                            display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                            pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(int(options["opening_menu"]) * 200, 101, 1200 - int(options["opening_menu"]) * 200, 26))
                        screen.blit(chinese_character_font_data.render("正式版  {}".format(recent_download_version_manifest_content["latest"]["release"]), True, colour.DimGray), (10 + int(options["opening_menu"]) * 200, 106))
                    if "snapshot" in recent_download_version_manifest_content["latest"]:
                        if position_in_rect(position, int(options["opening_menu"]) * 200, 127, 1200 - int(options["opening_menu"]) * 200, 26):
                            display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                            pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(int(options["opening_menu"]) * 200, 127, 1200 - int(options["opening_menu"]) * 200, 26))
                        screen.blit(chinese_character_font_data.render("测试版  {}".format(recent_download_version_manifest_content["latest"]["snapshot"]), True, colour.DimGray), (10 + int(options["opening_menu"]) * 200, 132))
                else:
                    screen.blit(chinese_character_font_data.render("加载中", True, colour.Black), (1142, 80))
            elif options["choosing_resource_number"] == 1:
                if len(os.listdir("temp")) > 1:
                    if ran_download_version_manifest:
                        if os.listdir("temp"):
                            ran_download_version_manifest = False               # 确保仅仅刚刚完成下载才加载，防止死循环未响应
                            recent_download_version_manifest_temporary_file_name = "temp/" + max(os.listdir("temp"))
                            recent_download_version_manifest_temporary_file_class = open(recent_download_version_manifest_temporary_file_name, encoding="utf-8", mode="r")
                            recent_download_version_manifest_content: dict = json.load(recent_download_version_manifest_temporary_file_class)
                            version_array = recent_download_version_manifest_content["versions"]
                    game_version_total_pages = math.ceil(len(version_array) / ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION)
                    game_version_total = len(version_array)
                    # 页数
                    pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(int(options["opening_menu"]) * 200 + 60, 70, 1140 - int(options["opening_menu"]) * 200, 30))
                    screen.blit(font_data.render("{0} / {1}".format(options["pages_index"] + 1, game_version_total_pages), True, colour.Black), (int(options["opening_menu"]) * 200 + 68, 77))
                    # 向前翻页
                    if position_in_rect(position, int(options["opening_menu"]) * 200, 70, 30, 30):
                        display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                        pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(int(options["opening_menu"]) * 200, 70, 30, 30))
                        pygame.draw.polygon(screen, colour.LightGray, ((int(options["opening_menu"]) * 200 + 25, 75), (int(options["opening_menu"]) * 200 + 25, 95), (int(options["opening_menu"]) * 200 + 5, 85)), 1)
                    else:
                        pygame.draw.rect(screen, colour.LightGray, pygame.Rect(int(options["opening_menu"]) * 200, 70, 30, 30))
                        pygame.draw.polygon(screen, colour.Silver, ((int(options["opening_menu"]) * 200 + 25, 75), (int(options["opening_menu"]) * 200 + 25, 95), (int(options["opening_menu"]) * 200 + 5, 85)), 1)
                    # 向后翻页
                    if position_in_rect(position, int(options["opening_menu"]) * 200 + 30, 70, 30, 30):
                        display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                        pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(int(options["opening_menu"]) * 200 + 30, 70, 30, 30))
                        pygame.draw.polygon(screen, colour.LightGray, ((int(options["opening_menu"]) * 200 + 35, 75), (int(options["opening_menu"]) * 200 + 35, 95), (int(options["opening_menu"]) * 200 + 55, 85)), 1)
                    else:
                        pygame.draw.rect(screen, colour.LightGray, pygame.Rect(int(options["opening_menu"]) * 200 + 30, 70, 30, 30))
                        pygame.draw.polygon(screen, colour.Silver, ((int(options["opening_menu"]) * 200 + 35, 75), (int(options["opening_menu"]) * 200 + 35, 95), (int(options["opening_menu"]) * 200 + 55, 85)), 1)
                    # 版本列表显示
                    for i in range(ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION if len(version_array) - options["pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION > ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION else len(version_array) - options["pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION):
                        j = font_data.render(version_array[options["pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION + i]["id"], True, colour.Green if version_array[options["pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION + i]["type"] == "release" else (colour.Maroon if version_array[options["pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION + i]["type"] == "snapshot" else colour.Black))
                        if position_in_rect(position, int(options["opening_menu"]) * 200, 26 * i + 100, 1200 - int(options["opening_menu"]) * 200, 26):
                            pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(int(options["opening_menu"]) * 200, 26 * i + 100, 1200 - int(options["opening_menu"]) * 200, 26))
                        screen.blit(j, (5 + int(options["opening_menu"]) * 200, 26 * i + 104))
                else:
                    screen.blit(chinese_character_font_data.render("加载中", True, colour.Black), (1142, 80))
        if choosing_page == PAGE_OF_VERSION_DOWNLOAD:
            # 版本下载页面
            opening = int(options["opening_menu"]) * 200
            screen.blit(chinese_character_font_data.render("版本名称", True, colour.Black), (opening + 10, 57))
            if position_in_rect(position, opening + 80, 50, 1110 - opening, 30):
                display_cursor_type = pygame.SYSTEM_CURSOR_IBEAM
            pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(opening + 80, 50, 1110 - opening, 30), 1)
            blit_inputting_text("game_version_name", opening + 87, 57, is_valiable_dir_name(get_forms("game_version_name")))
            if position_in_rect(position, opening + 10, 90, 1180 - opening, 30):
                display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(opening + 10, 90, 1180 - opening, 30))
            pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(opening + 10, 90, 1180 - opening, 30), 1)
            screen.blit(chinese_character_font_data.render("下载版本", True, colour.Black), (int(options["opening_menu"]) * 100 + 568, 97))
        if choosing_page == PAGE_OF_VERSION_CHOOSING:
            # 版本选择页面
            opening = int(options["opening_menu"]) * 200
            # 页数
            pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(opening + 60, 35, 1140 - opening, 30))
            screen.blit(font_data.render("{0} / {1}".format(options["choosing_version_pages_index"] + 1, math.ceil(len(os.listdir(".minecraft/versions")) / ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION)), True, colour.Black), (opening + 68, 42))
            # 向前翻页
            if position_in_rect(position, int(options["opening_menu"]) * 200, 35, 30, 30):
                display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(int(options["opening_menu"]) * 200, 35, 30, 30))
                pygame.draw.polygon(screen, colour.LightGray, ((int(options["opening_menu"]) * 200 + 25, 40), (int(options["opening_menu"]) * 200 + 25, 60), (int(options["opening_menu"]) * 200 + 5, 50)), 1)
            else:
                pygame.draw.rect(screen, colour.LightGray, pygame.Rect(int(options["opening_menu"]) * 200, 35, 30, 30))
                pygame.draw.polygon(screen, colour.Silver, ((int(options["opening_menu"]) * 200 + 25, 40), (int(options["opening_menu"]) * 200 + 25, 60), (int(options["opening_menu"]) * 200 + 5, 50)), 1)
            # 向后翻页
            if position_in_rect(position, int(options["opening_menu"]) * 200 + 30, 35, 30, 30):
                display_cursor_type = pygame.SYSTEM_CURSOR_HAND
                pygame.draw.rect(screen, colour.Gainsboro, pygame.Rect(int(options["opening_menu"]) * 200 + 30, 35, 30, 30))
                pygame.draw.polygon(screen, colour.LightGray, ((int(options["opening_menu"]) * 200 + 35, 40), (int(options["opening_menu"]) * 200 + 35, 60), (int(options["opening_menu"]) * 200 + 55, 50)), 1)
            else:
                pygame.draw.rect(screen, colour.LightGray, pygame.Rect(int(options["opening_menu"]) * 200 + 30, 35, 30, 30))
                pygame.draw.polygon(screen, colour.Silver, ((int(options["opening_menu"]) * 200 + 35, 40), (int(options["opening_menu"]) * 200 + 35, 60), (int(options["opening_menu"]) * 200 + 55, 50)), 1)
            version_array = os.listdir(".minecraft/versions")
            for i in range(ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION if len(version_array) - options["choosing_version_pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION > ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION else len(version_array) - options["choosing_version_pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION):
                version_name = version_array[options["choosing_version_pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION + i]
                version_colour = tuple(get_game_config(version_name, {"colour": colour.Black}, False)["colour"])
                j = chinese_character_font_data.render(version_name, True, version_colour)
                if position_in_rect(position, opening, 26 * i + 65, 1200 - opening, 26):
                    pygame.draw.rect(screen, colour.WhiteSmoke, pygame.Rect(opening, 26 * i + 65, 1200 - opening, 26))
                screen.blit(j, (5 + int(options["opening_menu"]) * 200, 26 * i + 70))
        if choosing_page == PAGE_OF_THINKING:
            # 二阶思索
            if options["thinking_page"] == 0:
                HOMEPAGE_Y_BEGIN = 75
                screen.blit(chinese_character_font_data.render("左侧的菜单栏上每个选项都可在点击后跳转至具体页面" if options["opening_menu"] else "点击左上角后打开菜单", True, colour.Black), (int(options["opening_menu"]) * 200 + 7, HOMEPAGE_Y_BEGIN + 7))
            if options["thinking_page"] == PAGE_OF_THINKING:
                pygame.draw.line(screen, colour.Black, (1100, 35), (1100, 60))
                screen.blit(chinese_character_font_data.render("思索", True, colour.Black), (1084, 64))
                screen.blit(chinese_character_font_data.render("你现在正在干的事", True, colour.Black), (1036, 84))
        # 事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 退出启动器
                looping = False
            elif event.type == pygame.KEYDOWN:
                # logger.info("Pressed key")
                logger.info("Pressed key {0}, also known as {1}".format(event.key, pygame.key.name(event.key)))
                if options["input_form"] != 0:
                    inputting(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    logger.info("Left clicked at {}".format(position))
                    if position_in_rect(position, 0, 0, 40, 35):
                        # 菜单
                        logger.info("Clicked the menu")
                        options["opening_menu"] = not options["opening_menu"]
                    if position_in_rect(position, 1080, 0, 40, 35):
                        # 思索该页面
                        # logger.info("Clicked to think")
                        # options["thinking_page"] = choosing_page
                        # choosing_page = PAGE_OF_THINKING
                        pass
                    if position_in_rect(position, 1120, 0, 40, 35):
                        # 最小化启动器
                        logger.info("Clicked to iconify")
                        pygame.display.iconify()
                    if position_in_rect(position, 1160, 0, 40, 35):
                        # 退出启动器
                        logger.info("Clicked to close")
                        looping = False
                    # 菜单点击事件
                    if options["opening_menu"]:
                        for i in range(5):
                            if position_in_rect(position, 0, 35 * i + 35, 200, 35):
                                choosing_page = i
                                logger.info("Switched action to {}".format(i + 1))
                    if choosing_page == 0:
                        # Minecraft 页面交互逻辑
                        half_opening = options["opening_menu"] * 100
                        if position_in_rect(position, int(options["opening_menu"]) * 200 + 50, 45, 1140 - int(options["opening_menu"]) * 200, 30):
                            options["choosing_setting_number"] = 2
                            logger.info("Switching action minecraft to action setting")
                            choosing_page = 1
                            logger.info("Switched action to {0}.{1}".format(choosing_page + 1, options["choosing_setting_number"]))
                        if position_in_rect(position, half_opening + 600, 760, 600 - half_opening, 40):
                            choosing_page = PAGE_OF_VERSION_CHOOSING
                        if position_in_rect(position, half_opening * 2, 760, 600 - half_opening, 40):
                            launch_minecraft_thread = thread_pool_executor.submit(launch_minecraft_main)
                    elif choosing_page == 1:
                        # 设置 页面交互逻辑
                        for i in range(len(setting_display_array)):
                            if position_in_rect(position, int(options["opening_menu"]) * 200 + 100 * i, 35, 100, 35):
                                options["choosing_setting_number"] = i
                                logger.info("Switched action to {0}.{1}".format(choosing_page + 1, options["choosing_setting_number"]))
                        if options["choosing_setting_number"] == 0:
                            pass
                        elif options["choosing_setting_number"] == 1:
                            if position_in_rect(position, 1160, 80, 30, 30):
                                java_exe_file: str = fileopenbox("选择Java程序文件", "Stonal's Launcher Collection", "*", [["java.exe", "Java程序"]], False)
                                logger.info("Chosen java executor \"{}\"".format(java_exe_file))
                                if java_exe_file is not None:
                                    java_exe_file = java_exe_file.replace("\\", "/")
                                    java_exe_file_array: dict = get_config("java_executor_files", dict())
                                    if java_exe_file not in java_exe_file_array.keys():
                                        java_exe_file_array[java_exe_file] = int(get_command_output("\"{}\" --version".format(java_exe_file.replace("/java.exe", "/javaw.exe"))).split()[1].split(".")[0])
                                        set_config("java_executor_files", java_exe_file_array)
                        elif options["choosing_setting_number"] == 2:
                            if position_in_rect(position, opening, 70, 30, 30):
                                append_account_config({"type": "minecraft_legacy", "user": "Player", "game_uuid": build_uuid(), "enabled": False})
                                forms["player_name"] = "Player"
                                options["editing_account_config"] = len(get_account_config())
                            for i in range(len(get_account_config(False))):
                                if position_in_rect(position, 1170, i * 30 + 100, 30, 30):
                                    logger.info("Chosen account {} to configure".format(i + 1))
                                    options["editing_account_config"] = i + 1
                                    forms["player_name"] = get_account_config()[i]["user"]
                            if options["editing_account_config"] != 0:
                                if get_account_config(False)[options["editing_account_config"] - 1]["type"] == "minecraft_legacy":
                                    if position_in_rect(position, opening + 70, 540, 1120 - opening, 30):
                                        input_text = get_forms("player_name")
                                        inputting_text_cursor_location = len(get_forms("player_name"))
                                        options["input_form"] = 2
                                    if position_in_rect(position, opening + 10, 580, 1180 - opening, 30):
                                        edited_account_config = get_account_config(False)[options["editing_account_config"] - 1]
                                        edited_account_config["user"] = get_forms("player_name")
                                        set_account_config(options["editing_account_config"] - 1, edited_account_config)
                                        options["editing_account_config"] = 0
                                        input_text = str()
                                        forms["player_name"] = str()
                                    elif position_in_rect(position, opening + 10, 620, 1180 - opening, 30):
                                        account_array_size = len(get_account_config())
                                        for i in range(account_array_size):
                                            disabled_account_config = get_account_config(False)[i]
                                            disabled_account_config["enabled"] = False
                                            set_account_config(i, disabled_account_config)
                                        edited_account_config = get_account_config(False)[options["editing_account_config"] - 1]
                                        edited_account_config["enabled"] = True
                                        set_account_config(options["editing_account_config"] - 1, edited_account_config)
                                    elif position_in_rect(position, opening + 10, 660, 1180 - opening, 30):
                                        remove_account_config(options["editing_account_config"] - 1)
                                        options["editing_account_config"] = 0
                        elif options["choosing_setting_number"] == 3:
                            if position_in_rect(position, opening + 10, 80, 200, 30) and not building_necessary_resource:
                                building_resource_config_version_name = get_config("choosing_version")
                                build_resource_necessary_thread = thread_pool_executor.submit(build_resource_necessary_main)
                                build_resource_necessary_thread.add_done_callback(build_resource_necessary_callback)
                                build_resource_necessary_calculating_thread = thread_pool_executor.submit(minecraft_operator.launch.build_resource_necessary_calculating, building_resource_config_version_name)
                    elif choosing_page == 2:
                        # 资源 页面交互逻辑
                        for i in range(len(resource_display_array)):
                            if position_in_rect(position, int(options["opening_menu"]) * 200 + 100 * i, 35, 100, 35):
                                options["choosing_resource_number"] = i
                                logger.info("Switched action to {0}.{1}".format(choosing_page + 1, options["choosing_setting_number"]))
                        if options["choosing_resource_number"] == 0:
                            if len(os.listdir("temp")) > 1:
                                recent_download_version_manifest_temporary_file_name = "temp/" + max(list(set(os.listdir("temp")).symmetric_difference({"command_output.txt"})))
                                recent_download_version_manifest_temporary_file_class = open(recent_download_version_manifest_temporary_file_name, encoding="utf-8", mode="r")
                                recent_download_version_manifest_content: dict = json.load(recent_download_version_manifest_temporary_file_class)
                                if "release" in recent_download_version_manifest_content["latest"] and position_in_rect(position, int(options["opening_menu"]) * 200, 101, 1200 - int(options["opening_menu"]) * 200, 26):
                                    if "snapshot" in recent_download_version_manifest_content["latest"]:
                                        chosen_game_version_in_download_page = find_version_in_array(recent_download_version_manifest_content["versions"], recent_download_version_manifest_content["latest"]["release"])
                                    else:
                                        chosen_game_version_in_download_page = recent_download_version_manifest_content["versions"][0]
                                    forms["game_version_name"] = chosen_game_version_in_download_page["id"]
                                    input_text = get_forms("game_version_name")
                                    inputting_text_cursor_location = len(get_forms("game_version_name"))
                                    choosing_page = -1
                                    logger.info("Switched to page of downloading versions")
                                if "snapshot" in recent_download_version_manifest_content["latest"] and position_in_rect(position, int(options["opening_menu"]) * 200, 127, 1200 - int(options["opening_menu"]) * 200, 26):
                                    chosen_game_version_in_download_page = recent_download_version_manifest_content["versions"][0]
                                    forms["game_version_name"] = chosen_game_version_in_download_page["id"]
                                    input_text = get_forms("game_version_name")
                                    inputting_text_cursor_location = len(get_forms("game_version_name"))
                                    choosing_page = -1
                                    logger.info("Switched to page of downloading versions")
                        if options["choosing_resource_number"] == 1:
                            if len(os.listdir("temp")) > 1:
                                if position_in_rect(position, int(options["opening_menu"]) * 200, 70, 30, 30):
                                    options["pages_index"] -= 1
                                    options["pages_index"] %= game_version_total_pages
                                if position_in_rect(position, int(options["opening_menu"]) * 200 + 30, 70, 30, 30):
                                    options["pages_index"] += 1
                                    options["pages_index"] %= game_version_total_pages
                                for i in range(ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION if game_version_total - options["pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION > ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION else game_version_total - options["pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION):
                                    if position_in_rect(position, int(options["opening_menu"]) * 200, 26 * i + 100, 1200 - int(options["opening_menu"]) * 200, 26):
                                        # 下载对应版本
                                        recent_download_version_manifest_temporary_file_name = "temp/" + max(os.listdir("temp"))
                                        recent_download_version_manifest_temporary_file_class = open(recent_download_version_manifest_temporary_file_name, encoding="utf-8", mode="r")
                                        recent_download_version_manifest_content: dict = json.load(recent_download_version_manifest_temporary_file_class)
                                        chosen_game_version_in_download_page = recent_download_version_manifest_content["versions"][options["pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_DOWNLOAD_VERSION + i]
                                        forms["game_version_name"] = chosen_game_version_in_download_page["id"]
                                        input_text = get_forms("game_version_name")
                                        inputting_text_cursor_location = len(get_forms("game_version_name"))
                                        choosing_page = -1
                                        logger.info("Switched to page of downloading versions")
                    elif choosing_page == PAGE_OF_VERSION_DOWNLOAD:
                        # 版本下载页面交互逻辑
                        opening = int(options["opening_menu"]) * 200
                        if position_in_rect(position, opening + 80, 50, 1110 - opening, 30):
                            options["input_form"] = 1
                        else:
                            options["input_form"] = 0
                        if position_in_rect(position, opening + 10, 90, 1180 - opening, 30):
                            if is_valiable_dir_name(get_forms("game_version_name")):
                                download_new_game_version_thread = thread_pool_executor.submit(download_new_game_version_main, chosen_game_version_in_download_page, get_forms("game_version_name"))
                                download_new_game_version_thread.add_done_callback(download_new_game_version_callback)
                                choosing_page = 0
                    elif choosing_page == PAGE_OF_VERSION_CHOOSING:
                        # 版本选择页面交互逻辑
                        opening = int(options["opening_menu"]) * 200
                        if position_in_rect(position, int(options["opening_menu"]) * 200, 70, 30, 30):
                            options["choosing_version_pages_index"] -= 1
                            options["choosing_version_pages_index"] %= math.ceil(len(os.listdir(".minecraft/versions")) / ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION)
                        if position_in_rect(position, int(options["opening_menu"]) * 200 + 30, 70, 30, 30):
                            options["choosing_version_pages_index"] += 1
                            options["choosing_version_pages_index"] %= math.ceil(len(os.listdir(".minecraft/versions")) / ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION)
                        for i in range(ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION if len(version_array) - options["choosing_version_pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION > ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION else len(version_array) - options["choosing_version_pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION):
                            if position_in_rect(position, opening, 26 * i + 65, 1200 - opening, 26):
                                # 选择对应版本
                                set_config("choosing_version", os.listdir(".minecraft/versions")[i])
                                choosing_page = 0
                                logger.info("Switched action to {}".format(choosing_page + 1))
                                break
                elif event.button == 2:
                    logger.info("Middle clicked at {}".format(position))
                elif event.button == 3:
                    logger.info("Right clicked at {}".format(position))
                    if choosing_page == PAGE_OF_VERSION_CHOOSING:
                        # 版本选择页面交互逻辑 右键
                        opening = int(options["opening_menu"]) * 200
                        if position_in_rect(position, int(options["opening_menu"]) * 200, 70, 30, 30):
                            options["choosing_version_pages_index"] -= 1
                            options["choosing_version_pages_index"] %= math.ceil(len(os.listdir(".minecraft/versions")) / ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION)
                        if position_in_rect(position, int(options["opening_menu"]) * 200 + 30, 70, 30, 30):
                            options["choosing_version_pages_index"] += 1
                            options["choosing_version_pages_index"] %= math.ceil(len(os.listdir(".minecraft/versions")) / ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION)
                        for i in range(ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION if len(version_array) - options["choosing_version_pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION > ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION else len(version_array) - options["choosing_version_pages_index"] * ELEMENT_NUMBER_OF_ONE_PAGE_IN_CHOOSING_VERSION):
                            if position_in_rect(position, opening, 26 * i + 65, 1200 - opening, 26):
                                # 设置对应版本
                                config_version_name = os.listdir(".minecraft/versions")[i]
                                choosing_page = 1
                                options["choosing_setting_number"] = 3
                                logger.info("Switched action to {}".format(choosing_page + 1, options["choosing_setting_number"]))
                                break
                elif event.button == 4:
                    logger.info("Middle rolled at {} (up)".format(position))
                elif event.button == 5:
                    logger.info("Middle rolled at {} (down)".format(position))
        # 输入逻辑
        if options["input_form"] == 1:
            forms["game_version_name"] = input_text
        elif options["input_form"] == 2:
            forms["player_name"] = input_text
        pygame.mouse.set_cursor(display_cursor_type)
        pygame.display.flip()
except Exception as error:
    exception_type, exception_value, exception_traceback = sys.exc_info()
    last_frame = traceback.extract_tb(exception_traceback)[-1]
    logger.critical("An error happened at line {0} of {1}: type {2}, content: {3}".format(last_frame.lineno, os.path.basename(last_frame.filename), exception_type.__name__, error))
    logger.critical("Stopping with quite a serious error")
finally:
    pygame.quit()
    logger.info("Stopping!")
    # region
    # Stonla's Launcher Collection
    # .-------------.  .--.             .-------------.
    # |  .----------'  |  |             |  .----------'
    # |  |             |  |             |  |
    # |  '----------.  |  |             |  |
    # '----------.  |  |  |             |  |
    #            |  |  |  |             |  |
    # .----------'  |  |  '----------.  |  '----------.
    # '-------------'  '-------------'  '-------------'
    # 作者 石辰子
    # 审核 石印社软件审核室
    # Author:                                                           Stonal
    # Checker:                                                          Stonal's Printing Press
    #                                                                   Software Checking Room
    # endregion
    thread_pool_executor.shutdown(True)
    logger.info("End of stopping!")
# pyinstaller --onefile --windowed --icon=slc.ico main.pyw