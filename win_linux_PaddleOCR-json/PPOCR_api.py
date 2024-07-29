# 调用 PaddleOCR-json.exe 的 Python Api
# 项目主页：
# https://github.com/hiroi-sora/PaddleOCR-json

import os
import socket  # 套接字
import atexit  # 退出处理
import subprocess  # 进程，管道
import re  # regex
from json import loads as jsonLoads, dumps as jsonDumps
from sys import platform as sysPlatform  # popen静默模式
from base64 import b64encode  # base64 编码


class PPOCR_pipe:  # 调用OCR（管道模式）
    def __init__(self, exePath: str, modelsPath: str = None, argument: dict = None):
        """初始化识别器（管道模式）。\n
        `exePath`: 识别器`PaddleOCR_json.exe`的路径。\n
        `modelsPath`: 识别库`models`文件夹的路径。若为None则默认识别库与识别器在同一目录下。\n
        `argument`: 启动参数，字典`{"键":值}`。参数说明见 https://github.com/hiroi-sora/PaddleOCR-json
        """
        # 私有成员变量
        self.__ENABLE_CLIPBOARD = False

        exePath = os.path.abspath(exePath)
        cwd = os.path.abspath(os.path.join(exePath, os.pardir))  # 获取exe父文件夹
        cmds = [exePath]
        # 处理启动参数
        if modelsPath is not None:
            if os.path.exists(modelsPath) and os.path.isdir(modelsPath):
                cmds += ["--models_path", os.path.abspath(modelsPath)]
            else:
                raise Exception(
                    f"Input modelsPath doesn't exits or isn't a directory. modelsPath: [{modelsPath}]"
                )
        if isinstance(argument, dict):
            for key, value in argument.items():
                # Popen() 要求输入list里所有的元素都是 str 或 bytes
                if isinstance(value, bool):
                    cmds += [f"--{key}={value}"]  # 布尔参数必须键和值连在一起
                elif isinstance(value, str):
                    cmds += [f"--{key}", value]
                else:
                    cmds += [f"--{key}", str(value)]
        # 设置子进程启用静默模式，不显示控制台窗口
        self.ret = None
        startupinfo = None
        if "win32" in str(sysPlatform).lower():
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = (
                subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
            )
            startupinfo.wShowWindow = subprocess.SW_HIDE
        self.ret = subprocess.Popen(  # 打开管道
            cmds,
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,  # 丢弃stderr的内容
            startupinfo=startupinfo,  # 开启静默模式
        )
        # 启动子进程
        while True:
            if not self.ret.poll() == None:  # 子进程已退出，初始化失败
                raise Exception(f"OCR init fail.")
            initStr = self.ret.stdout.readline().decode("utf-8", errors="ignore")
            if "OCR init completed." in initStr:  # 初始化成功
                break
            elif "OCR clipboard enbaled." in initStr:  # 检测到剪贴板已启用
                self.__ENABLE_CLIPBOARD = True
        atexit.register(self.exit)  # 注册程序终止时执行强制停止子进程

    def isClipboardEnabled(self) -> bool:
        return self.__ENABLE_CLIPBOARD

    def getRunningMode(self) -> str:
        # 默认管道模式只能运行在本地
        return "local"

    def runDict(self, writeDict: dict):
        """传入指令字典，发送给引擎进程。\n
        `writeDict`: 指令字典。\n
        `return`:  {"code": 识别码, "data": 内容列表或错误信息字符串}\n"""
        # 检查子进程
        if not self.ret:
            return {"code": 901, "data": f"引擎实例不存在。"}
        if not self.ret.poll() == None:
            return {"code": 902, "data": f"子进程已崩溃。"}
        # 输入信息
        writeStr = jsonDumps(writeDict, ensure_ascii=True, indent=None) + "\n"
        try:
            self.ret.stdin.write(writeStr.encode("utf-8"))
            self.ret.stdin.flush()
        except Exception as e:
            return {
                "code": 902,
                "data": f"向识别器进程传入指令失败，疑似子进程已崩溃。{e}",
            }
        # 获取返回值
        try:
            getStr = self.ret.stdout.readline().decode("utf-8", errors="ignore")
        except Exception as e:
            return {"code": 903, "data": f"读取识别器进程输出值失败。异常信息：[{e}]"}
        try:
            return jsonLoads(getStr)
        except Exception as e:
            return {
                "code": 904,
                "data": f"识别器输出值反序列化JSON失败。异常信息：[{e}]。原始内容：[{getStr}]",
            }

    def run(self, imgPath: str):
        """对一张本地图片进行文字识别。\n
        `exePath`: 图片路径。\n
        `return`:  {"code": 识别码, "data": 内容列表或错误信息字符串}\n"""
        writeDict = {"image_path": imgPath}
        return self.runDict(writeDict)

    def runClipboard(self):
        """立刻对剪贴板第一位的图片进行文字识别。\n
        `return`:  {"code": 识别码, "data": 内容列表或错误信息字符串}\n"""
        if self.__ENABLE_CLIPBOARD:
            return self.run("clipboard")
        else:
            raise Exception("剪贴板功能不存在或已禁用。")

    def runBase64(self, imageBase64: str):
        """对一张编码为base64字符串的图片进行文字识别。\n
        `imageBase64`: 图片base64字符串。\n
        `return`:  {"code": 识别码, "data": 内容列表或错误信息字符串}\n"""
        writeDict = {"image_base64": imageBase64}
        return self.runDict(writeDict)

    def runBytes(self, imageBytes):
        """对一张图片的字节流信息进行文字识别。\n
        `imageBytes`: 图片字节流。\n
        `return`:  {"code": 识别码, "data": 内容列表或错误信息字符串}\n"""
        imageBase64 = b64encode(imageBytes).decode("utf-8")
        return self.runBase64(imageBase64)

    def exit(self):
        """关闭引擎子进程"""
        if hasattr(self, "ret"):
            if not self.ret:
                return
            try:
                self.ret.kill()  # 关闭子进程
            except Exception as e:
                print(f"[Error] ret.kill() {e}")
        self.ret = None
        atexit.unregister(self.exit)  # 移除退出处理
        print("###  PPOCR引擎子进程关闭！")

    @staticmethod
    def printResult(res: dict):
        """用于调试，格式化打印识别结果。\n
        `res`: OCR识别结果。"""

        # 识别成功
        if res["code"] == 100:
            index = 1
            for line in res["data"]:
                print(
                    f"{index}-置信度：{round(line['score'], 2)}，文本：{line['text']}"
                )
                index += 1
        elif res["code"] == 100:
            print("图片中未识别出文字。")
        else:
            print(f"图片识别失败。错误码：{res['code']}，错误信息：{res['data']}")

    def __del__(self):
        self.exit()
