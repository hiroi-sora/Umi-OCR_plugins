from . import aba_ocr
from . import aba_ocr_config

# 插件信息
PluginInfo = {
    # 插件组别
    "group": "ocr",
    # 全局配置
    "global_options": aba_ocr_config.globalOptions,
    # 局部配置
    "local_options": aba_ocr_config.localOptions,
    # 接口类
    "api_class": aba_ocr.Api,
}
