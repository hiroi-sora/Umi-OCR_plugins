from . import api_paddleocr
from . import paddleocr_config

# 插件信息
PluginInfo = {
    # 插件组别
    "group": "ocr",
    # 全局配置
    "global_options": paddleocr_config.globalOptions,
    # 局部配置
    "local_options": paddleocr_config.localOptions,
    # 接口类
    "api_class": api_paddleocr.Api,
}
