from plugin_i18n import Translator

# UI翻译
tr = Translator(__file__, "i18n.csv")

# 全局配置
globalOptions = {
    "title": tr("Mistral OCR"),
    "type": "group",
    "api_key": {
        "title": tr("API密钥"),
        "default": "",
        "toolTip": tr("Mistral API的密钥，用于访问OCR服务。"),
    },
    "model": {
        "title": tr("模型"),
        "default": "mistral-ocr-latest",
        "toolTip": tr("Mistral OCR使用的模型名称。"),
    },
    "timeout": {
        "title": tr("超时时间"),
        "isInt": True,
        "default": 30,
        "min": 5,
        "max": 120,
        "unit": tr("秒"),
        "toolTip": tr("API请求的超时时间。"),
    },
    "include_image_base64": {
        "title": tr("包含图像Base64"),
        "default": False,
        "toolTip": tr("是否在响应中包含图像的Base64编码。"),
        "advanced": True,
    },
}

# 局部配置
localOptions = {
    "title": tr("文字识别（Mistral OCR）"),
    "type": "group",
    "language": {
        "title": tr("语言"),
        "optionsList": [
            ["auto", tr("自动检测")],
            ["zh", tr("中文")],
            ["en", tr("英文")],
            ["ja", tr("日语")],
            ["ko", tr("韩语")],
            ["fr", tr("法语")],
            ["de", tr("德语")],
            ["ru", tr("俄语")],
            ["es", tr("西班牙语")],
            ["pt", tr("葡萄牙语")],
            ["it", tr("意大利语")],
        ],
        "default": "auto",
        "toolTip": tr("识别的目标语言，自动检测可能会影响准确性。"),
    },
    "image_min_size": {
        "title": tr("最小图像尺寸"),
        "isInt": True,
        "default": 0,
        "min": 0,
        "max": 1000,
        "toolTip": tr("提取图像的最小尺寸（像素）。0表示不限制。"),
        "advanced": True,
    },
}
