import logging as __logging

generated_minecraft_libraries_count = 0
generated_minecraft_asset_files_count = 0
def is_native_library(library_name: str) -> bool:
    library_description = library_name.split(":")
    return len(library_description) == 4 and library_description[-1].startswith("natives-")
def get_native_classifier(library_name: str) -> str:
    library_description = library_name.split(":")
    if len(library_description) == 4:
        return library_description[3]
    return str()
def version_greater_than(a, b) -> bool:
    import sys
    if isinstance(a, str):
        a_version_details = tuple(map(int, a.split(".")))
    else:
        a_version_details = (a.major, a.minor, a.build)
    if isinstance(b, str):
        b_version_details = tuple(map(int, b.split(".")))
    else:
        b_version_details = (b.major, b.minor, b.build)
    if a_version_details[0] > b_version_details[0]:
        return True
    if a_version_details[0] < b_version_details[0]:
        return False
    if a_version_details[1] > b_version_details[1]:
        return True
    if a_version_details[1] < b_version_details[1]:
        return False
    if a_version_details[2] > b_version_details[2]:
        return True
    if a_version_details[2] < b_version_details[2]:
        return False
    return False
def is_able_to_add_the_argument(rules: list, logger: __logging.Logger = None) -> bool:
    import sys, platform
    if not rules:
        return True
    for i in rules:
        if logger is not None:
            logger.debug("Rule -> {}".format(i))
        action: str = i["action"]
        if "os" in i:
            system: dict = i["os"]
            if "name" in system:
                if system["name"] == "windows" and action == "disallow":
                    return False
                if system["name"] != "windows" and action == "allow":
                    return False
            if "versionRange" in system:
                if "min" in system["versionRange"]:
                    if version_greater_than(system["versionRange"]["min"], sys.getwindowsversion()):
                        return False
                if "max" in system["versionRange"]:
                    if version_greater_than(sys.getwindowsversion(), system["versionRange"]["max"]):
                        return False
            arch = platform.machine().lower()
            # 统一架构命名
            if arch in ("amd64", "x86_64"):
                arch = "x64"
            elif arch in ("i386", "i686", "x86"):
                arch = "x86"
            elif arch.startswith("arm"):
                arch = "arm" if "64" not in arch else "arm64"
            if "arch" in system:
                if system["arch"] != arch:
                    return False
    return True
def get_system_arch():
    # 返回当前系统架构标识，与 Minecraft 版本 JSON 中的 arch 字段匹配
    import platform
    machine = platform.machine().lower()
    arch_map = {
        "amd64": "x64",
        "x86_64": "x64",
        "x64": "x64",
        "i386": "x86",
        "i686": "x86",
        "x86": "x86",
        "armv7l": "arm",
        "armv8l": "arm64",
        "aarch64": "arm64",
        "arm64": "arm64"
    }
    return arch_map.get(machine, machine)
def is_able_to_add_the_argument_game(rules: list) -> bool:
    if not rules:
        return True
    for i in rules:
        if not isinstance(i, dict):
            continue
        action: str = i["action"]
        if "features" in i:
            is_demo_user: bool = i["features"].get("is_demo_user", None)
            has_custom_resolution: bool = i["features"].get("has_custom_resolution", None)
            has_quick_plays_support: bool = i["features"].get("has_quick_plays_support", None)
            is_quick_play_singleplayer: bool = i["features"].get("is_quick_play_singleplayer", None)
            is_quick_play_multiplayer: bool = i["features"].get("is_quick_play_multiplayer", None)
            is_quick_play_realms: bool = i["features"].get("is_quick_play_realms", None)
            if is_demo_user is not None:
                if is_demo_user and action == "disallow":
                    return True
                if is_demo_user and action == "allow":
                    return False
            if has_custom_resolution is not None:
                if has_custom_resolution and action == "disallow":
                    return False
                if has_custom_resolution and action == "allow":
                    return True
            if has_quick_plays_support is not None:
                if has_quick_plays_support and action == "disallow":
                    return True
                if has_quick_plays_support and action == "allow":
                    return False
            if is_quick_play_singleplayer is not None:
                if is_quick_play_singleplayer and action == "disallow":
                    return True
                if is_quick_play_singleplayer and action == "allow":
                    return False
            if is_quick_play_multiplayer is not None:
                if is_quick_play_multiplayer and action == "disallow":
                    return True
                if is_quick_play_multiplayer and action == "allow":
                    return False
            if is_quick_play_realms is not None:
                if is_quick_play_realms and action == "disallow":
                    return True
                if is_quick_play_realms and action == "allow":
                    return False
    return True
def build_minecraft_libraries(choosing_version_folder_name: str, logger: __logging.Logger = None, forced_override=False):
    import os, json
    import requests as web
    global generated_minecraft_libraries_count
    generated_minecraft_libraries_count = 0
    version_json_path = f".minecraft/versions/{choosing_version_folder_name}/{choosing_version_folder_name}.json"
    with open(version_json_path, "r", encoding="utf-8") as f:
        version_json = json.load(f)
    natives_dir = f".minecraft/versions/{choosing_version_folder_name}/{choosing_version_folder_name}-natives"
    os.makedirs(natives_dir, exist_ok=True)
    for lib in version_json["libraries"]:
        # 检查平台规则
        should_apply = True
        if "rules" in lib:
            # 遍历所有规则，判断是否允许当前系统即Windows
            for rule in lib["rules"]:
                if rule.get("action") == "allow":
                    if "os" in rule and rule["os"].get("name") != "windows":
                        should_apply = False
                        break
                    if "arch" in rule and rule["arch"] != get_system_arch():
                        should_apply = False
                        break
                if rule.get("action") == "disallow":
                    if "os" in rule and rule["os"].get("name") == "windows":
                        should_apply = False
                        break
        invalid_arch = ["x64", "x86", "arm", "arm64"]
        invalid_arch.remove(get_system_arch())
        for i in invalid_arch:
            if i in lib["name"]:
                should_apply = False
                break
        if not should_apply:
            continue
        # 处理普通 artifact（新格式的核心）
        if "downloads" in lib and "artifact" in lib["downloads"]:
            artifact: dict = lib["downloads"]["artifact"]
            path: str = artifact["path"]
            url: str = artifact["url"]
            local_path = ".minecraft/libraries/" + path
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            if forced_override or not os.path.isfile(local_path):
                logger.debug("Downloading {0} -> {1}".format(url, local_path))
                response = web.get(url)
                response.raise_for_status()
                with open(local_path, "wb") as f:
                    f.write(response.content)
                generated_minecraft_libraries_count += 1
            else:
                logger.debug("Existing library: {}".format(lib["name"]))
            # 判断是否为 Native 库并解压
            # 规则：库名包含 "natives-" 或路径包含 "natives-"
            is_native = ("natives-" in lib.get("name", "") or "natives-" in path)
            if is_native:
                extract_java_library(local_path, natives_dir, logger)
                # 如需额外计数可在此增加，但已计入总库数
        # 兼容旧版 classifiers
        # 某些旧版本既可能有 artifact（通常无用）也有 classifiers
        if "downloads" in lib and "classifiers" in lib["downloads"]:
            classifiers: dict = lib["downloads"]["classifiers"]
            platform_key = None
            for key in classifiers.keys():
                if "windows" in key.lower():
                    platform_key = key
                    break
            if platform_key is not None:
                native_artifact: dict = classifiers[platform_key]
                native_path: str = native_artifact["path"]
                local_native_path: str = ".minecraft/libraries/" + native_path
                os.makedirs(os.path.dirname(local_native_path), exist_ok=True)
                if forced_override or not os.path.isfile(local_native_path):
                    logger.debug("Downloading native (legacy) {0} -> {1}".format(native_artifact["url"], local_native_path))
                    response = web.get(native_artifact["url"])
                    response.raise_for_status()
                    with open(local_native_path, "wb") as f:
                        f.write(response.content)
                extract_java_library(local_native_path, natives_dir, logger)
                # 旧版通常没有计入总数，此处也可增加
                generated_minecraft_libraries_count += 1
def built_asset_files(choosing_version_folder_name: str, logger: __logging.Logger = None, forced_override = False):
    import os, json
    import requests as web
    global generated_minecraft_asset_files_count
    generated_minecraft_asset_files_count = 0
    file = open(".minecraft/versions/{0}/{0}.json".format(choosing_version_folder_name), mode="r", encoding="utf-8")
    version_json: dict = json.load(file)
    file.close()
    if not os.path.isdir(".minecraft/assets"):
        os.mkdir(".minecraft/assets")
    if not os.path.isdir(".minecraft/assets/indexes"):
        os.mkdir(".minecraft/assets/indexes")
    if not os.path.isdir(".minecraft/assets/objects"):
        os.mkdir(".minecraft/assets/objects")
    index_file_name = ".minecraft/assets/indexes/{}.json".format(version_json["assetIndex"]["id"])
    if forced_override or not os.path.isfile(index_file_name):
        asset_index = web.get(version_json["assetIndex"]["url"]).json()
        with open(index_file_name, mode="w", encoding="utf-8") as index_file:
            index_file.write(json.dumps(asset_index, ensure_ascii=False, indent=4))
    else:
        with open(index_file_name, mode="r", encoding="utf-8") as index_file:
            asset_index = json.load(index_file)
        logger.debug("Existing asset index")
    for i in asset_index["objects"].keys():
        hash: str = asset_index["objects"][i]["hash"]
        if not os.path.isdir(".minecraft/assets/objects/" + hash[0:2]):
            os.mkdir(".minecraft/assets/objects/" + hash[0:2])
        if forced_override or not os.path.isfile(".minecraft/assets/objects/{0}/{1}".format(hash[0:2], hash)):
            asset_byte = web.get("https://resources.download.minecraft.net/{0}/{1}".format(hash[0:2], hash)).content
            with open(".minecraft/assets/objects/{0}/{1}".format(hash[0:2], hash), mode="wb") as asset_file:
                asset_file.write(asset_byte)
            logger.debug("Downloaded {}".format(hash))
            generated_minecraft_asset_files_count += 1
        else:
            logger.debug("Existing asset {}".format(hash))
def build_launch_bash_array(choosing_version_folder_name: str, logger: __logging.Logger = None) -> list:
    # 需要确保有可用的Java，否则返回~invalid: missing java
    # 需要确保有可用的账号，否则返回~invalid: missing account
    import os, json, math, psutil
    config = open("config/launcher.json", mode="r")
    config_data = json.load(config)
    account_config = open("config/account.json", mode="r")
    account_config_data = json.load(account_config)
    file = open(".minecraft/versions/{0}/{0}.json".format(choosing_version_folder_name), mode="r", encoding="utf-8")
    version_json: dict = json.load(file)
    account_config.close()
    config.close()
    file.close()
    java_executor_files: dict = config_data["java_executor_files"]
    account = dict()
    if version_json["javaVersion"]["majorVersion"] in java_executor_files.values():
        for i in java_executor_files.keys():
            if java_executor_files[i] == version_json["javaVersion"]["majorVersion"]:
                java_executor_files_most_suitable: str = i
                break
    else:
        java_executor_files_item = java_executor_files.items()
        java_executor_files_item_minus_suitable_java = list()
        for i in java_executor_files_item:
            minus_suitable_java: int = i[1] - version_json["javaVersion"]["majorVersion"]
            if minus_suitable_java > 0:
                java_executor_files_item_minus_suitable_java.append((i[0], minus_suitable_java))
        if not java_executor_files_item_minus_suitable_java:
            if logger is not None:
                logger.warning("Missing java executor")
            return "~invalid: missing java"
        min_value = (str(), math.inf)
        for i in java_executor_files_item_minus_suitable_java:
            if min_value[1] > i[1]:
                min_value[0] = i[0]
                min_value[1] = i[1]
        java_executor_files_most_suitable: str = min_value[0]
    launcher_command = [java_executor_files_most_suitable]
    if not account_config_data:
        return "~invalid: missing account"
    for i in account_config_data:
        if i["type"] in ("minecraft_legacy", "microsoft_account") and i["enabled"]:
            account = i
            break
    if not account:
        return "~invalid: missing account"
    launcher_command.append("-Dstderr.encoding=UTF-8")
    launcher_command.append("-Dstdout.encoding=UTF-8")
    launcher_command.append("-Dfile.encoding=COMPAT")
    launcher_command.append("-XX:+UseG1GC")
    launcher_command.append("-XX:-UseAdaptiveSizePolicy")
    launcher_command.append("-XX:-OmitStackTraceInFastThrow")
    launcher_command.append("-Djdk.lang.Process.allowAmbiguousCommands=true")
    launcher_command.append("-Dfml.ignoreInvalidMinecraftCertificates=True")
    launcher_command.append("-Dfml.ignorePatchDiscrepancies=True")
    launcher_command.append("-Dlog4j2.formatMsgNoLookups=true")
    if "minecraftArguments" in version_json and "arguments" not in version_json:
        version_json["arguments"] = version_json["minecraftArguments"]
    jvm_args = version_json["arguments"].get("default-user-jvm", []) + version_json["arguments"].get("jvm", [])
    total_memory_size_gb = psutil.virtual_memory().total / (1024 ** 3)
    if total_memory_size_gb >= 8:
        max_heap_size = min((total_memory_size_gb * 0.6), 6) * 1024
    elif total_memory_size_gb >= 4:
        max_heap_size = total_memory_size_gb * 512
    else:
        max_heap_size = max(total_memory_size_gb * 512, 1024)
    launcher_command.append("-Xmx{}M".format(int(max_heap_size)))
    launcher_command.append("-Xms{}M".format(int(max_heap_size * 0.7)))
    launcher_command.append("-Dorg.lwjgl.librarypath={}".format(os.path.abspath(".minecraft/versions/{0}/{0}-natives".format(choosing_version_folder_name))))
    launcher_command.append("-Dorg.lwjgl.util.DisableNativesExtraction=true")
    for i in jvm_args:
        if isinstance(i, str):
            game_argv: str = replace_argument_in_argument(i, choosing_version_folder_name, account, version_json, java_executor_files_most_suitable)
            if "-Xmx" in game_argv or "-Xms" in game_argv:
                continue
            launcher_command.append(game_argv)
        elif isinstance(i, dict):
            if i["value"] not in launcher_command and is_able_to_add_the_argument(dict(i).get("rules", False), logger):
                value = i["value"]
                if isinstance(value, str):
                    if "-Xmx" in value or "-Xms" in value:
                        continue
                    launcher_command.append(value)
                elif isinstance(value, list):
                    for j in value:
                        if "-Xmx" in j or "-Xms" in j:
                            continue
                        launcher_command.append(j)
    launcher_command.append("net.minecraft.client.main.Main")
    for i in version_json["arguments"]["game"]:
        if isinstance(i, str):
            game_argv: str = replace_argument_in_argument(i, choosing_version_folder_name, account, version_json, java_executor_files_most_suitable)
            launcher_command.append(game_argv)
        elif isinstance(i, dict):
            if isinstance(i["value"], str):
                if i["value"] not in launcher_command and is_able_to_add_the_argument_game(i.get("rules", False)):
                    game_argv: str = replace_argument_in_argument(i["value"], choosing_version_folder_name, account, version_json, java_executor_files_most_suitable)
                    launcher_command.append(game_argv)
            elif isinstance(i["value"], list):
                for j in i["value"]:
                    if j not in launcher_command and is_able_to_add_the_argument_game(i.get("rules", False)):
                        game_argv: str = replace_argument_in_argument(j, choosing_version_folder_name, account, version_json, java_executor_files_most_suitable)
                        launcher_command.append(game_argv)
    return launcher_command
def replace_argument_in_argument(game_argv: str, version_name: str, account: dict, version_json: dict, java_executor_file: str) -> str:
    from .config import basic_config
    import os
    game_argv = game_argv.replace("${auth_player_name}", account["user"])
    game_argv = game_argv.replace("${version_name}", version_name)
    game_argv = game_argv.replace("${game_directory}", ".minecraft/versions/{}".format(version_name))
    game_argv = game_argv.replace("${assets_root}", ".minecraft/assets")
    game_argv = game_argv.replace("${assets_index_name}", version_json["assetIndex"]["id"])
    game_argv = game_argv.replace("${auth_uuid}", account["game_uuid"])
    game_argv = game_argv.replace("${auth_access_token}", account["access_token"] if account["type"] == "microsoft_account" else "0")
    game_argv = game_argv.replace("${clientid}", "undefined")
    game_argv = game_argv.replace("${auth_xuid}", "undefined")
    game_argv = game_argv.replace("${version_type}", "Stonal's Launcher Collection")
    game_argv = game_argv.replace("${resolution_width}", "854")
    game_argv = game_argv.replace("${resolution_height}", "480")
    game_argv = game_argv.replace("${launcher_name}", "Stonal's Launcher Collection")
    game_argv = game_argv.replace("${launcher_version}", basic_config["launcher_version"])
    game_argv = game_argv.replace("${natives_directory}/java", "{0};{1}".format(os.path.abspath(".minecraft/versions/{0}/{0}-natives".format(version_name)), os.path.dirname(java_executor_file)))
    game_argv = game_argv.replace("${natives_directory}/jna", os.path.abspath(".minecraft/versions/{0}/{0}-natives".format(version_name)))
    game_argv = game_argv.replace("${natives_directory}/lwjgl", os.path.abspath(".minecraft/versions/{0}/{0}-natives".format(version_name)))
    game_argv = game_argv.replace("${natives_directory}/netty", os.path.abspath(".minecraft/versions/{0}/{0}-natives".format(version_name)))
    game_argv = game_argv.replace("${classpath}", "{0};{1}".format(os.path.abspath(".minecraft/versions/{0}/{0}.jar".format(version_name)), ";".join(get_all_library_class_path(version_json))))
    return game_argv
def build_launch_bash_string(choosing_version_folder_name: str, logger: __logging.Logger = None) -> str:
    array = build_launch_bash_array(choosing_version_folder_name, logger)
    LENGTH = len(array)
    for i in range(LENGTH):
        if " " in array[i]:
            array[i] = "\"{}\"".format(array[i])
    return " ".join(array)
def get_all_library_class_path(version_json: dict) -> list:
    import os
    library_path = list()
    for lib in version_json["libraries"]:
        library_directory = lib["downloads"]["artifact"]["path"]
        if "natives-" in lib["name"] or "natives-" in library_directory:
            continue
        library_path.append(os.path.abspath(".minecraft/libraries/{}".format(library_directory)))
    return library_path
def build_resource_necessary_calculating(version_name: str, logger: __logging.Logger = None) -> tuple:
    import json, os
    global generated_minecraft_asset_files_count, generated_minecraft_libraries_count
    result = [None] * 4
    version_json_file = open(".minecraft/versions/{0}/{0}.json".format(version_name), mode="r", encoding="utf-8")
    version_json: dict = json.load(version_json_file)
    version_json_file.close()
    index_file_name = ".minecraft/assets/indexes/{}.json".format(version_json["assetIndex"]["id"])
    if os.path.isfile(index_file_name):
        object_mapping_file = open(index_file_name, mode="r", encoding="utf-8")
        object_mapping_array: dict = json.load(object_mapping_file)["objects"]
        object_mapping_file.close()
        result[3] = len(object_mapping_array)
        result[2] = generated_minecraft_asset_files_count
    result[1] = len(version_json["libraries"])
    result[0] = generated_minecraft_libraries_count
    return tuple(result)
def extract_java_library(jar_path: str, target_dir: str, logger: __logging.Logger = None):
    # 提取 jar 中的所有 .dll 文件到 target_dir（不创建子目录）
    import zipfile, os
    os.makedirs(target_dir, exist_ok=True)
    with zipfile.ZipFile(jar_path, "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            # 只提取 .dll 文件
            if info.filename.lower().endswith(".dll"):
                # 获取文件名
                filename = os.path.basename(info.filename)
                target_path = os.path.join(target_dir, filename)
                # 解压
                with zf.open(info) as src, open(target_path, "wb") as dst:
                    dst.write(src.read())
                if logger is not None:
                    logger.debug("Extracted {0} to {1}".format(filename, target_path))
# def build_minecraft_libraries(choosing_version_folder_name: str, logger: __logging.Logger = None, forced_override=False):
#     import os, json, zipfile
#     import requests as web
#     global generated_minecraft_libraries_count
#     generated_minecraft_libraries_count = 0
#     version_json_path = ".minecraft/versions/{0}/{0}.json".format(choosing_version_folder_name)
#     with open(version_json_path, "r", encoding="utf-8") as f:
#         version_json: dict = json.load(f)
#     natives_dir = ".minecraft/versions/{0}/{0}-natives".format(choosing_version_folder_name)
#     os.makedirs(natives_dir, exist_ok=True)
#     for lib in version_json.get("libraries", []):
#         # 1. 处理普通artifact（通常是主JAR）
#         if "downloads" in lib and "artifact" in lib["downloads"]:
#             artifact = lib["downloads"]["artifact"]
#             path = artifact["path"]
#             url = artifact["url"]
#             local_path = ".minecraft/libraries/{}".format(path)
#             os.makedirs(os.path.dirname(local_path), exist_ok=True)
#             if forced_override or not os.path.isfile(local_path):
#                 logger.debug("Downloading {0} -> {1}".format(url, local_path))
#                 response = web.get(url)
#                 response.raise_for_status()
#                 with open(local_path, "wb") as f:
#                     f.write(response.content)
#                 generated_minecraft_libraries_count += 1
#         # 2. 处理native库
#         if "downloads" in lib and "classifiers" in lib["downloads"]:
#             logger.info("Library \"{}\" is a native library".format(lib["name"]))
#             classifiers: dict = lib["downloads"]["classifiers"]
#             # 查找 Windows 平台对应的 classifier key（如 "natives-windows" 或 "natives-windows-64"）
#             platform_key = None
#             for key in classifiers.keys():
#                 if "windows" in str(key).lower():
#                     platform_key = key
#                     break
#             if platform_key is None:
#                 # 没有 Windows 的 classifier，跳过（可能是 Linux/Mac）
#                 continue
#             native_artifact = classifiers[platform_key]
#             native_url = native_artifact["url"]
#             native_path = native_artifact["path"]
#             local_native_path = ".minecraft/libraries/{}".format(native_path)
#             os.makedirs(os.path.dirname(local_native_path), exist_ok=True)
#             # 下载 native jar（如果尚未下载）
#             if forced_override or not os.path.isfile(local_native_path):
#                 logger.debug("Downloading native {0} -> {1}".format(native_url, local_native_path))
#                 response = web.get(native_url)
#                 response.raise_for_status()
#                 with open(local_native_path, "wb") as f:
#                     f.write(response.content)
#             # 解压到 natives 目录（提取所有 .dll）
#             extract_java_library(local_native_path, natives_dir, logger)
#             generated_minecraft_libraries_count += 1                    # 计入总数（可选）
# def extract_java_library(library_name: str, jar_path: str, target_directory: str, store_ingore_list: str = None, logger: __logging.Logger = None) -> None:
#     import zipfile, os, json
#     os.makedirs(target_directory, exist_ok=True)
#     with zipfile.ZipFile(jar_path, "r") as zip_file_data:
#         for information in zip_file_data.infolist():
#             if information.is_dir() or os.path.splitext(information.filename)[1] != ".dll":
#                 continue
#             file_name = os.path.basename(information.filename)
#             folder_name = library_name.split(":")[0].split(".")[1]
#             output_directory = "{0}/{1}/{2}".format(target_directory, folder_name, file_name)
#             with zip_file_data.open(information) as source_file, open(output_directory, "wb") as target_file:
#                 target_file.write(source_file.read())
#             if logger is not None:
#                 logger.info("Extracted {0} from {1} of {2}".format(output_directory, information.filename, jar_path))
#     if store_ingore_list is not None:
#         try:
#             store_ingore_file = open(store_ingore_list, mode="r+", encoding="utf-8")
#             store_ingore_data: list = json.load(store_ingore_file)
#             store_ingore_data.append(jar_path)
#             store_ingore_file.truncate(0)
#             store_ingore_file.write(json.dumps(store_ingore_data, ensure_ascii=False, indent=4))
#             if logger is not None:
#                 logger.info("File {} will be ignored".format(jar_path))
#         except json.JSONDecodeError:
#             logger.error("Invalid store ingore list file {}".format(store_ingore_list))