# Umi-OCR 插件接口： PaddleOCR-json
# 项目主页：
# https://github.com/hiroi-sora/PaddleOCR-json

import os
import psutil  # 进程检查
from platform import system  # 平台检查
import threading  # 线程

from call_func import CallFunc
from .PPOCR_api import PPOCR_pipe

# 引擎可执行文件（入口）名称
# # TODO ：改为 Umi 内部的平台标志，无需自己获取标志
system_type = system()
ExeFile = ""
if system_type == "Windows":
    ExeFile = "PaddleOCR-json.exe"
elif system_type == "Linux":
    ExeFile = "run.sh"
else:
    raise NotImplementedError(f"[Error] PaddleOCR: Unsupported system: {system_type}")

# 引擎可执行文件路径
ExePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), ExeFile)
# 引擎可执行文件启动参数映射表。将配置项映射到启动参数
ExeConfigs = [
    ("enable_mkldnn", "enable_mkldnn"),  # mkl加速
    ("config_path", "language"),  # 配置文件路径
    ("cls", "cls"),  # 方向分类
    ("use_angle_cls", "cls"),  # 方向分类
    ("limit_side_len", "limit_side_len"),  # 长边压缩
    ("cpu_threads", "cpu_threads"),  # 线程数
]


class Api:  # 公开接口
    def __init__(self, globalArgd):
        # 测试路径是否存在
        if not os.path.exists(ExePath):
            raise ValueError(f'[Error] Exe path "{ExePath}" does not exist.')
        # 初始化参数
        self.api = None  # api对象
        self.exeConfigs = {}  # exe启动参数字典
        self._updateExeConfigs(self.exeConfigs, globalArgd)  # 更新启动参数字典
        # 内存清理参数
        self.ramInfo = {"max": -1, "time": -1, "timerID": ""}
        m = globalArgd["ram_max"]
        if isinstance(m, (int, float)):
            self.ramInfo["max"] = m
        m = globalArgd["ram_time"]
        if isinstance(m, (int, float)):
            self.ramInfo["time"] = m
        self.isInit = True
        self.lock = threading.Lock()  # 线程锁

    # 更新启动参数，将data的值写入target
    def _updateExeConfigs(self, target, data):
        for c in ExeConfigs:
            if c[1] in data:
                target[c[0]] = data[c[1]]

    # 启动引擎。返回： "" 成功，"[Error] xxx" 失败
    def start(self, argd):
        with self.lock:
            # 加载局部参数
            tempConfigs = self.exeConfigs.copy()
            self._updateExeConfigs(tempConfigs, argd)
            # 若引擎已启动，且局部参数与传入参数一致，则无需重启
            if self.api is not None and set(tempConfigs.items()) == set(
                self.exeConfigs.items()
            ):
                return ""
            # 记录参数
            self.exeConfigs = tempConfigs
            # 启动引擎
            try:
                self.stop()
                self.api = PPOCR_pipe(ExePath, argument=tempConfigs)
            except Exception as e:
                self.api = None
                return f"[Error] OCR init fail. Argd: {tempConfigs}\n{e}"
            return ""

    def stop(self):  # 停止引擎
        if self.api is None:
            return
        self.api.exit()
        self.api = None

    def runPath(self, imgPath: str):  # 路径识图
        self._runBefore()
        res = self.api.run(imgPath)
        self._ramClear()
        return res

    def runBytes(self, imageBytes):  # 字节流
        self._runBefore()
        res = self.api.runBytes(imageBytes)
        self._ramClear()
        return res

    def runBase64(self, imageBase64):  # base64字符串
        self._runBefore()
        res = self.api.runBase64(imageBase64)
        self._ramClear()
        return res

    def _runBefore(self):
        CallFunc.delayStop(self.ramInfo["timerID"])  # 停止ram清理计时器

    def _restart(self):  # 重启引擎
        with self.lock:
            try:
                self.stop()
                self.api = PPOCR_pipe(ExePath, argument=self.exeConfigs)
            except Exception as e:
                self.api = None
                print(f"[Error] OCR restart fail: {e}")

    def _ramClear(self):  # 内存清理
        if self.ramInfo["max"] > 0:
            pid = self.api.ret.pid
            rss = psutil.Process(pid).memory_info().rss
            rss /= 1048576
            if rss > self.ramInfo["max"]:
                self._restart()
        if self.ramInfo["time"] > 0:
            self.ramInfo["timerID"] = CallFunc.delay(
                self._restart, self.ramInfo["time"]
            )
