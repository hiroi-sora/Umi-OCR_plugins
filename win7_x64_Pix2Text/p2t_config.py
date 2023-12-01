from plugin_i18n import Translator

# UI翻译
tr = Translator(__file__, "i18n.csv")

tips = tr("支持中文/英文/数学公式混排")

# 全局配置
globalOptions = {
    "title": "Pix2Text" + tr("（本地）"),
    "type": "group",
    "tips": {"title": tips, "btnsList": []},
}

# 局部配置
localOptions = {
    "title": tr("文字识别") + " (Pix2Text)",
    "type": "group",
    "tips": {"title": tips, "btnsList": []},
}
