# 调用 RapidOCR-json.exe 的 Python Api
# 项目主页：
# https://github.com/hiroi-sora/RapidOCR-json

import os
from .rapidocr import Rapid_pipe
from .rapidocr_config import LangDict

# exe路径
ExePath = os.path.dirname(os.path.abspath(__file__)) + "/RapidOCR-json.exe"


class Api:  # 公开接口
    def __init__(self, globalArgd):
        # 测试路径是否存在
        if not os.path.exists(ExePath):
            raise ValueError(f'[Error] Exe path "{ExePath}" does not exist.')
        # 初始化参数
        self.api = None  # api对象
        self.exeConfigs = {  # exe启动参数字典
            "models": "models",
            "ensureAscii": 1,
            "det": None,
            "cls": None,
            "rec": None,
            "keys": None,
            "doAngle": 0,
            "mostAngle": 0,
            "maxSideLen": None,
            "numThread": globalArgd["numThread"],
        }

    def start(self, argd):  # 启动引擎。返回： "" 成功，"[Error] xxx" 失败
        # 加载局部参数
        tempConfigs = self.exeConfigs.copy()
        try:
            lang = LangDict[argd["language"]]
            tempConfigs.update(lang)
            if argd["angle"]:
                tempConfigs["doAngle"] = tempConfigs["mostAngle"] = 1
            else:
                tempConfigs["doAngle"] = tempConfigs["mostAngle"] = 0
            tempConfigs["maxSideLen"] = argd["maxSideLen"]
        except Exception as e:
            self.api = None
            return f"[Error] OCR start fail. Argd: {argd}\n{e}"

        # 若引擎已启动，且局部参数与传入参数一致，则无需重启
        if not self.api == None:
            if set(tempConfigs.items()) == set(self.exeConfigs.items()):
                return ""
            # 若引擎已启动但需要更改参数，则停止旧引擎
            self.stop()
        # 启动新引擎
        self.exeConfigs = tempConfigs
        try:
            self.api = Rapid_pipe(ExePath, tempConfigs)
        except Exception as e:
            self.api = None
            return f"[Error] OCR init fail. Argd: {tempConfigs}\n{e}"
        return ""

    def stop(self):  # 停止引擎
        if self.api == None:
            return
        self.api.exit()
        self.api = None

    def runPath(self, imgPath: str):  # 路径识图
        res = self.api.run(imgPath)
        return res

    def runBytes(self, imageBytes):  # 字节流
        res = self.api.runBytes(imageBytes)
        return res

    def runBase64(self, imageBase64):  # base64字符串
        res = self.api.runBase64(imageBase64)
        return res
