from plugin_i18n import Translator

# UI翻译
tr = Translator(__file__, "i18n.csv")



globalOptions = {
    "title": tr("微信OCR(本地)"),
    "type": "group",
}

localOptions = {
    "title": tr("微信OCR(本地)"),
    "type": "group",
}