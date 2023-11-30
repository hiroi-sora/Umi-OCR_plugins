from . import p2t_api
from . import p2t_config

PluginInfo = {
    "group": "ocr",  # 固定写法，定义插件组
    "global_options": p2t_config.globalOptions,  # 全局配置字典
    "local_options": p2t_config.localOptions,  # 局部配置字典
    "api_class": p2t_api.Api,  # 接口类
}
