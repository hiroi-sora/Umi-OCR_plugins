from plugin_i18n import Translator

# UI翻译
tr = Translator(__file__, "i18n.csv")


# 全局配置
globalOptions = {
    "title": "Pix2Text" + tr("（本地）"),
    "type": "group",
    "tips": {
        "title": tr("支持中文/英文/数学公式/混排"),
        "btnsList": [],
    },
}

# 局部配置
localOptions = {
    "title": tr("文字识别") + " (Pix2Text)",
    "type": "group",
    "recognize_text": {
        "title": tr("启用文字识别"),
        "toolTip": tr("支持简体中文+英文"),
        "default": True,
    },
    "recognize_formula": {
        "title": tr("启用数学公式"),
        "default": True,
    },
    "resized_shape": {
        "title": tr("限制图像边长"),
        "optionsList": [
            [608, "608 " + tr("（默认）")],
            [1216, "1216"],
            [2432, "2432"],
            [4864, "4864"],
        ],
        "toolTip": tr(
            "将边长大于该值的图片进行压缩，可以提高识别速度。可能降低识别精度。"
        ),
    },
}
