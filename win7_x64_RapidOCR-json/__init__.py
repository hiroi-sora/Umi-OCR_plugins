from . import api_rapidocr
from . import rapidocr_config

# 插件信息
PluginInfo = {
    # 插件组别
    "group": "ocr",
    # 全局配置
    "global_options": rapidocr_config.globalOptions,
    # 局部配置
    "local_options": rapidocr_config.localOptions,
    # 接口类
    "api_class": api_rapidocr.Api,
}
