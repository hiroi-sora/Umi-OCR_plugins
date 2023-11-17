import os
import psutil
from plugin_i18n import Translator

tr = Translator(__file__, "i18n.csv")

# 模块配置路径
MODELS_CONFIGS = "/models/configs.txt"
# 保存语言字典
LangDict = {}


# 动态获取模型库列表
def _getlanguageList():
    global LangDict
    """configs.txt 格式示例：
    简体中文(V4)
    ch_PP-OCRv4_det_infer.onnx
    ch_ppocr_mobile_v2.0_cls_infer.onnx
    rec_ch_PP-OCRv4_infer.onnx
    dict_chinese.txt

    """
    optionsList = []
    configsPath = os.path.dirname(os.path.abspath(__file__)) + MODELS_CONFIGS
    try:
        with open(configsPath, "r", encoding="utf-8") as file:
            content = file.read()
            parts = content.split("\n\n")
            for part in parts:
                items = part.split("\n")
                if len(items) == 5:
                    title, det, cls, rec, keys = items
                    LangDict[title] = {
                        "det": det,
                        "cls": cls,
                        "rec": rec,
                        "keys": keys,
                    }
                    optionsList.append([title, title])
        return optionsList
    except FileNotFoundError:
        print("[Error] RapidOCR配置文件configs不存在，请检查文件路径是否正确。", configsPath)
    except IOError:
        print("[Error] RapidOCR配置文件configs无法打开或读取。")
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
    "title": tr("RapidOCR（本地）"),
    "type": "group",
    "numThread": {
        "title": tr("线程数"),
        "default": _threads,
        "min": 1,
        "isInt": True,
    },
}

localOptions = {
    "title": tr("文字识别（RapidOCR）"),
    "type": "group",
    "language": {
        "title": tr("语言/模型库"),
        "optionsList": _LanguageList,
    },
    "angle": {
        "title": tr("纠正文本方向"),
        "default": False,
        "toolTip": tr("启用方向分类，识别倾斜或倒置的文本。可能降低识别速度。"),
    },
    "maxSideLen": {
        "title": tr("限制图像边长"),
        "optionsList": [
            [1024, "1024 " + tr("（默认）")],
            [2048, "2048"],
            [4096, "4096"],
            [999999, tr("无限制")],
        ],
        "toolTip": tr("将边长大于该值的图片进行压缩，可以提高识别速度。可能降低识别精度。"),
    },
}
