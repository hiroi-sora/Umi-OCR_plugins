from . import WechatOCR_api
from . import WechatOCR_config

# 插件信息
PluginInfo = {
    # 插件组别
    "group": "ocr",
    # 全局配置
    "global_options": WechatOCR_config.globalOptions,
    # 局部配置
    "local_options": WechatOCR_config.localOptions,
    # 接口类
    "api_class": WechatOCR_api.Api,
}