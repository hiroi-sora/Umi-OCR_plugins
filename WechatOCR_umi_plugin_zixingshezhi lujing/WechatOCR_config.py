from plugin_i18n import Translator

# UI翻译
tr = Translator(__file__, "i18n.csv")



globalOptions = {
    "title": tr("微信OCR(本地)-用户自行设置路径"),
    "type": "group",
    "wechat_ocr_dir": {
        "title": tr("WeChatOCR.exe的文件路径"),
        "toolTip": tr("WeChatOCR.exe的文件路径,不是微信的路径"),
        "default": "",
    },
    "wechat_dir": {
        "title": tr("微信的完整路径，有带版本号就填带版本号的路径"),
        "toolTip": tr("微信的完整路径，有带版本号就填带版本号的路径，例如：C:\Program Files (x86)\Tencent\WeChat\[3.9.8.25]"),
        "default": "",
    },    
}


localOptions = {
    "title": tr("微信OCR(本地)-用户自行设置路径"),
    "type": "group",
}