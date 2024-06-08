from . import PPOCR_umi
from . import PPOCR_config

# 插件信息
PluginInfo = {
    # 插件组别
    "group": "ocr",
    # 全局配置
    "global_options": PPOCR_config.globalOptions,
    # 局部配置
    "local_options": PPOCR_config.localOptions,
    # 接口类
    "api_class": PPOCR_umi.Api,
}
