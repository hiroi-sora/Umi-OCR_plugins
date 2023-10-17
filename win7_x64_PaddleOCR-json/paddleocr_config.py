import os
import psutil
from i18n import trLoad, tr

trLoad("")

# 模块配置路径
MODELS_CONFIGS = "/models/configs.txt"


# 动态获取模型库列表
def _getlanguageList():
    """configs.txt 格式示例：
    config_chinese.txt 简体中文
    config_en.txt English
    """
    optionsList = []
    configsPath = os.path.dirname(os.path.abspath(__file__)) + MODELS_CONFIGS
    try:
        with open(configsPath, "r", encoding="utf-8") as file:
            content = file.read()
            lines = content.split("\n")
            for l in lines:
                parts = l.split(" ", 1)
                optionsList.append([f"models/{parts[0]}", parts[1]])
        return optionsList
    except FileNotFoundError:
        print("[Error] PPOCR配置文件configs不存在，请检查文件路径是否正确。", configsPath)
    except IOError:
        print("[Error] PPOCR配置文件configs无法打开或读取。")
    return []


_LanguageList = _getlanguageList()


# 获取最佳线程数
def _getThreads():
    try:
        phyCore = psutil.cpu_count(logical=False)  # 物理核心数
        lgiCore = psutil.cpu_count(logical=True)  # 逻辑核心数
        if (
            not isinstance(phyCore, int)
            or not isinstance(lgiCore, int)
            or lgiCore < phyCore
        ):
            raise ValueError("核心数计算异常")
        # 物理核数=逻辑核数，返回逻辑核数
        if phyCore * 2 == lgiCore or phyCore == lgiCore:
            return lgiCore
        # 大小核处理器，返回大核线程数
        big = lgiCore - phyCore
        return big * 2
    except Exception as e:
        print("[Warning] 无法获取CPU核心数！", e)
        return 4


_threads = _getThreads()

globalOptions = {
    "title": tr("PaddleOCR（本地）"),
    "type": "group",
    "enable_mkldnn": {
        "title": tr("启用MKL-DNN加速"),
        "default": True,
        "toolTip": tr("使用MKL-DNN数学库提高神经网络的计算速度。能大幅加快OCR识别速度，但也会增加内存占用。"),
    },
    "cpu_threads": {
        "title": tr("线程数"),
        "default": _threads,
        "min": 1,
        "isInt": True,
    },
    "ram_max": {
        "title": tr("内存占用限制"),
        "default": -1,
        "min": -1,
        "unit": "MB",
        "isInt": True,
        "advanced": True,
        "toolTip": tr("值>0时启用。引擎内存占用超过该值时，执行内存清理。"),
    },
    "ram_time": {
        "title": tr("内存闲时清理"),
        "default": 30,
        "min": -1,
        "unit": tr("秒"),
        "isInt": True,
        "advanced": True,
        "toolTip": tr("值>0时启用。引擎空闲时间超过该值时，执行内存清理。"),
    },
}

localOptions = {
    "title": tr("文字识别（PaddleOCR）"),
    "type": "group",
    "language": {
        "title": tr("语言/模型库"),
        "optionsList": _LanguageList,
    },
    "cls": {
        "title": tr("纠正文本方向"),
        "default": False,
        "toolTip": tr("启用方向分类，识别倾斜或倒置的文本。可能降低识别速度。"),
    },
    "limit_side_len": {
        "title": tr("限制图像边长"),
        "optionsList": [
            [960, "960 " + tr("（默认）")],
            [2880, "2880"],
            [4320, "4320"],
            [999999, tr("无限制")],
        ],
        "toolTip": tr("将边长大于该值的图片进行压缩，可以提高识别速度。可能降低识别精度。"),
        "advanced": True,  # 高级选项
    },
}
