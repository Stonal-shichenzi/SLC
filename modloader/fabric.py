import requests as web
import re, os, time, json, logging

class FabricLibrary():
    def __init__(self, library_json: dict) -> None:
        self.library_name: str = library_json["name"]
        if ("net.minecraft:launchwrapper:" in self.library_name) and ("url" not in library_json):
            version = re.findall(r"(?<=net\.minecraft:launchwrapper:)[\d\.]+", self.library_name)
            self.library_url = "https://libraries.minecraft.net/net/minecraft/launchwrapper/{0}/launchwrapper-{0}.jar".format(version)
        else:
            group_id, artifact_id, version = self.library_name.split(":")
            self.library_url = "https://maven.fabricmc.net/{0}/{1}/{2}/{1}-{2}.jar".format(group_id.replace(".", "/"), artifact_id, version)
        self.library_size = library_json.get("size", 1024)
        self.library_hash = library_json.get("sha1", "affb794d4f958432ad23770bf62d5bb32c52cef9")        # missingno
class FabricLoaderVersion():
    class __loader():
        def __init__(self, loader_mapping: dict) -> None:
            self.version_name: str = loader_mapping["version"]
            self.version_separated = self.version_name.split(loader_mapping["separator"])
            self.__stable: bool = loader_mapping["stable"]
            self.build_version: int = loader_mapping["build"]
            self.maven_version: int = loader_mapping["maven"]
            self.url = "https://maven.fabricmc.net/net/fabricmc/fabric-loader/{0}/fabric-loader-{0}.jar".format(self.version_name)
        def is_stable(self) -> bool:
            return self.__stable
    class __intermediary():
        def __init__(self, loader_mapping: dict):
            self.maven_version: int = loader_mapping["maven"]
            self.__stable: bool = loader_mapping["stable"]
            self.version_name: str = loader_mapping["version"]
            self.url = "https://maven.fabricmc.net/net/fabricmc/intermediary/{0}/intermediary-{0}.jar".format(self.version_name)
        def is_stable(self) -> bool:
            return self.__stable
    def __init__(self, version_mapping: dict) -> None:
        self.loader = self.__loader(version_mapping["loader"])
        self.intermediary = self.__intermediary(version_mapping["intermediary"])
        self.json_meta_version: int = version_mapping["launcherMeta"]["version"]
        self.min_java_version: int = dict(version_mapping["launcherMeta"]).get("min_java_version", 0)
        self.main_class: str = version_mapping["launcherMeta"]["mainClass"] if isinstance(version_mapping["launcherMeta"]["mainClass"], str) else version_mapping["launcherMeta"]["mainClass"]["client"]
        self.main_class_server: str = self.main_class if isinstance(version_mapping["launcherMeta"]["mainClass"], str) else version_mapping["launcherMeta"]["mainClass"]["server"]
        self.libraries = [
            FabricLibrary(lib)
            for section in version_mapping["launcherMeta"]["libraries"].values()
            for lib in section
        ]

def get_fabric_loader_versions(minecraft_version: str):
    version_array = list()
    cache_filename = "modloader_temp/fabric/version_{}.json".format(time.strftime("%Y%j", time.localtime()))
    if (len(os.listdir("modloader_temp/fabric")) > 0) and (os.path.isfile(cache_filename)):
        with open(cache_filename, mode="r", encoding="utf-8") as cache_file:
            version_array: list = json.load(cache_file)
    else:
        version_array: list = web.get("https://meta.fabricmc.net/v2/versions/loader/{}/".format(minecraft_version)).json()
        with open(cache_filename, mode="w", encoding="utf-8") as cache_file:
            cache_file.write(json.dumps(version_array, ensure_ascii=False, indent=4))
    version_array_class = [FabricLoaderVersion(i) for i in version_array]
    return version_array_class
def download_fabric_modloader(fabric_version: FabricLoaderVersion, minecraft_version_diectory: str, logger: logging.Logger = None):
    for library in fabric_version.libraries:
        if logger is not None:
            logger.info("Downloading {}".format(library.library_name))
        file_byte_data = web.get(library.library_url, timeout=5).content
        group_id, artifact_id, library_version = library.library_name.split(":")
        os.makedirs(".minecraft/libraries/{0}/{1}/{2}".format(group_id.replace(".", "/"), artifact_id, library_version), exist_ok=True)
        with open(".minecraft/libraries/{0}/{1}/{2}/{1}-{2}.jar".format(group_id.replace(".", "/"), artifact_id, library_version), mode="wb") as library_file:
            library_file.write(file_byte_data)
    os.rename("{0}/{1}.json".format(minecraft_version_diectory, os.path.basename(minecraft_version_diectory)), "{0}/{1}.vanilla.jsonc".format(minecraft_version_diectory, os.path.basename(minecraft_version_diectory)))
    with open("{0}/{1}.vanilla.jsonc".format(minecraft_version_diectory, os.path.basename(minecraft_version_diectory)), mode="r", encoding="utf-8") as vanilla_version_json:
        vanilla_version_json_content: dict = json.load(vanilla_version_json)
        vanilla_version_json_content["mainClass"] = fabric_version.main_class
        for library in fabric_version.libraries:
            group_id, artifact_id, library_version = library.library_name.split(":")
            vanilla_version_json_content["libraries"].append({
                "downloads": {
                    "artifact": {
                        "path": "{0}/{1}/{2}/{1}-{2}.jar".format(group_id.replace(".", "/"), artifact_id, library_version),
                        "sha1": library.library_hash,
                        "size": library.library_size,
                        "url": library.library_url
                    }
                },
                "name": library.library_name
            })
        # 补上 fabric-loader 本体
        vanilla_version_json_content["libraries"].append({
            "downloads": {"artifact": {
                "path": "net/fabricmc/fabric-loader/{0}/fabric-loader-{0}.jar".format(fabric_version.loader.version_name),
                "url": fabric_version.loader.url,
                "sha1": "affb794d4f958432ad23770bf62d5bb32c52cef9",
                "size": 1024
            }},
            "name": "net.fabricmc:fabric-loader:{}".format(fabric_version.loader.version_name)
        })
        # 补上 intermediary
        vanilla_version_json_content["libraries"].append({
            "downloads": {"artifact": {
                "path": "net/fabricmc/intermediary/{0}/intermediary-{0}.jar".format(fabric_version.intermediary.version_name),
                "url": fabric_version.intermediary.url,
                "sha1": "affb794d4f958432ad23770bf62d5bb32c52cef9",
                "size": 1024
            }},
            "name": "net.fabricmc:intermediary:{}".format(fabric_version.intermediary.version_name)
        })
        with open("{0}/{1}.json".format(minecraft_version_diectory, os.path.basename(minecraft_version_diectory)), mode="w", encoding="utf-8") as modded_version_json:
            modded_version_json.write(json.dumps(vanilla_version_json_content, indent=4))