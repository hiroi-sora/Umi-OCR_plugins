# 调用 PaddleOCR-json.exe 的 Python Api
# 项目主页：
# https://github.com/hiroi-sora/PaddleOCR-json

from call_func import CallFunc

from .paddleocr import PPOCR_pipe

import os
import psutil  # 进程检查

# exe路径
ExePath = os.path.dirname(os.path.abspath(__file__)) + "/PaddleOCR-json.exe"
# exe启动参数映射表。将配置项映射到启动参数
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

    # 更新启动参数，将data的值写入target
    def _updateExeConfigs(self, target, data):
        for c in ExeConfigs:
            if c[1] in data:
                target[c[0]] = data[c[1]]

    # 启动引擎。返回： "" 成功，"[Error] xxx" 失败
    def start(self, argd):
        # 加载局部参数
        tempConfigs = self.exeConfigs.copy()
        self._updateExeConfigs(tempConfigs, argd)
        # 若引擎已启动，且局部参数与传入参数一致，则无需重启
        if not self.api == None:
            if set(tempConfigs.items()) == set(self.exeConfigs.items()):
                return ""
            # 若引擎已启动但需要更改参数，则停止旧引擎
            self.stop()
        # 启动新引擎
        self.exeConfigs = tempConfigs
        # 启动引擎
        try:
            self.api = PPOCR_pipe(ExePath, tempConfigs)
        except Exception as e:
            self.api = None
            return f"[Error] OCR init fail. Argd: {tempConfigs}"
        return ""

    def stop(self):  # 停止引擎
        if self.api == None:
            return
        self.api.exit()
        self.api = None

    def runPath(self, imgPath: str):  # 路径识图
        self.__runBefore()
        res = self.api.run(imgPath)
        self.__ramClear()
        return res

    def runBytes(self, imageBytes):  # 字节流
        self.__runBefore()
        res = self.api.runBytes(imageBytes)
        self.__ramClear()
        return res

    def runBase64(self, imageBase64):  # base64字符串
        self.__runBefore()
        res = self.api.runBase64(imageBase64)
        self.__ramClear()
        return res

    def __runBefore(self):
        CallFunc.delayStop(self.ramInfo["timerID"])  # 停止ram清理计时器

    def _restart(self):  # 重启引擎
        self.stop()
        # 启动引擎
        try:
            self.api = PPOCR_pipe(ExePath, self.exeConfigs)
            print("重启引擎")
        except Exception as e:
            self.api = None
            print(f"[Error]重启引擎失败: {e}")

    def __ramClear(self):  # 内存清理
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
