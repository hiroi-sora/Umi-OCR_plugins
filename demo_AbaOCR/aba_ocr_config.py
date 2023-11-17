from plugin_i18n import Translator

tr = Translator(__file__, "i18n.csv")

globalOptions = {
    "title": tr("阿巴阿巴OCR"),
    "type": "group",
    "api_key": {
        "title": tr("Api密钥"),
        "default": "",
        "toolTip": tr("阿巴阿巴OCR的Api密钥。"),
    },
}

localOptions = {
    "title": tr("文字识别（阿巴阿巴OCR）"),
    "type": "group",
    "language": {
        "title": tr("语言"),
        "optionsList": [
            ["zh_CN", "简体中文"],
            ["zh_TW", "繁體中文"],
            ["en_US", "English"],
            ["ja_JP", "日本語"],
        ],
    },
}
