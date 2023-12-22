# OCR 插件开发文档

开发者你好，欢迎探索 Umi-OCR 插件开发。这篇文档将介绍 **OCR插件** 的开发方法。

目录 `demo_AbaOCR` 中的文件构成一个最小demo，可在此基础上进行开发。

## 开始吧

下面将通过一个例子来介绍OCR插件的开发流程。

假设我们需要将一个已有的OCR组件：**阿巴阿巴OCR** 导入Umi。顾名思义， **阿巴阿巴OCR** 就是无论输入什么图片，都只会返回 `阿巴阿巴阿巴` 。

## 1. 提取可配置项

每个OCR插件，都一定会有一些配置项，能让用户自定义。大体上，配置项会分为两类：**全局配置项**和**局部配置项**。

##### 全局配置项：

无论在什么情景下，或者在哪个标签页中，都应该一致的配置项。如：在线Api接口的密钥key，超时时间，本地引擎组件的线程数，是否启用硬件加速……等。

##### 局部配置项：

不同标签页中，可能不相同配置项。如：识别语言等。

#### 阿巴的配置：

假设 **阿巴OCR** 含有以下配置：

| 配置项   | 类型   | 位置 |
| -------- | ------ | ---- |
| api_key  | 字符串 | 全局 |
| language | 枚举   | 局部 |

那么，创建一个 [aba_ocr_config.py](aba_ocr_config.py) ：

```python
from plugin_i18n import Translator

# UI翻译
tr = Translator(__file__, "i18n.csv")

# 全局配置
globalOptions = {
    "title": tr("阿巴阿巴OCR"),
    "type": "group",
    "api_key": {
        "title": tr("Api密钥"),
        "default": "",
        "toolTip": tr("阿巴阿巴OCR的Api密钥。"),
    },
}

# 局部配置
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
```
#### 说明：

##### UI翻译机制：

Umi-OCR 内嵌了一套简单的插件UI翻译机制（并非标准库或第三方库，只能在Umi中使用）。

在开头，翻译初始化的固定写法：

```python
from plugin_i18n import Translator
tr = Translator(__file__, "i18n.csv")
```

翻译某些字符串的写法：

```python
str1 = tr("字符串1")
str2 = tr("字符串2")
```

编写翻译表：

`i18n.csv` 中规定了每个字符串及对应的多语言翻译。以下示例，翻译了英文、繁中、日语、俄语：

```
key,en_US,zh_TW,ja_JP,ru_RU
字符串1,String 1,字串1,文字列1,Строка 1
字符串2,String 2,字串2,文字列2,Строка 2
```

如果嫌麻烦，可以只翻译英文。非中文的语言（如日韩俄德法……）缺失时，默认会采用英文翻译。

可以用Excel来编辑csv表格，但最后要将csv文件转为`utf-8`编码。（Excel默认可能不是utf-8，请务必检查。）

阿巴OCR的 `i18n.csv` 示例：

```
key,en_US
阿巴阿巴OCR,Aba OCR
Api密钥,Api Key
阿巴阿巴OCR的Api密钥。,Api key for Aba OCR.
文字识别（阿巴阿巴OCR）,Text recognition (Aba OCR)
语言,language
```

##### 插件配置字典：

插件需要定义两个字典：全局配置 `globalOptions` 和 局部配置 `localOptions` 。

每个配置字典，外层的固定写法如下：

```python
options = {
    "title": tr("配置组名称"),
    "type": "group",
    # TODO: 配置项
}
```

内层配置项的写法：

```python
    "布尔 boolean （开关）": {
        "title": "标题",
        "toolTip": "鼠标悬停提示",
        "default": True / False,
    },
    "文本 text （文本框）": {
        "title": ,
        "default": "文本",
    },
    "数字 number （输入框）": {
        "title": ,
        "isInt": True 整数 / False 浮点数,
        "default": 233,
        "max": 可选，上限,
        "min": 可选，下限,
        "unit": 可选，单位。如 tr("秒"),
    },
    "枚举 enum （下拉框）": {
        "title": ,
        "optionsList": [
            ["键1", "名称1"],
            ["键2", "名称2"],
        ],
    },
    "文件路径 file （文件选择框）": {
        "title": ,
        "type": "file",
        "default": "默认路径",
        "selectExisting": True 选择现有文件 / False 新创建文件(夹),
        "selectFolder": True 选择文件夹 / False 选择文件,
        "dialogTitle": 对话框标题,
        "nameFilters": ["图片 (*.jpg *.jpeg)", "类型2..."] 文件夹类型可不需要
    },

    # 每个配置项都可选的参数：
    "toolTip": 可选，字符串，鼠标悬停时的提示,
    "advanced": 可选，填True时为高级选项，平时隐藏
```

##### 空配置组

如果插件确实没有全局配置或局部配置，则可提供一个空配置组字典：
```python
# 空的局部配置
localOptions = {
    "title": tr("文字识别（阿巴阿巴OCR）"),
    "type": "group",
}
```


## 2. 构造OCR接口

每个OCR插件，都必须提供一个接口类，必须含有以下方法：

| 方法        | 说明                                   | 输入             | 返回值                                |
| ----------- | -------------------------------------- | ---------------- | ------------------------------------- |
| `__init__`  | 初始化接口类。不要进行耗时长的操作。   | 全局配置字典     | /                                     |
| `start`     | 启动引擎或接口。可以进行耗时长的操作。 | 局部配置字典     | 成功返回""，失败返回 "[Error] XXX..." |
| `stop`      | 停止引擎或接口。                       | /                | /                                     |
| `runPath`   | 输入路径，进行OCR                      | 图片路径字符串   | OCR结果                               |
| `runBytes`  | 输入字节流，进行OCR                    | 图片字节流       | OCR结果                               |
| `runBase64` | 输入base64，进行OCR                    | 图片base64字符串 | OCR结果                               |

OCR结果的格式：

成功，且有文字：
```python
{
    "code": 100,
    "data": [
        { # 第一组文本
            "text": "识别文本",
            "box": [[0, 0], [200, 0], [200, 40], [0, 40]], # 文本包围盒
            "score": 1, # 置信度，0~1。缺省就填1。
        },
        {}, # 第二组文本……
    ],
}
```

成功，但图中没有文字：
```python
{
    "code": 101,
    "data": "",
}
```

失败：
```python
{
    "code": 102, # 自定错误码：>101的数值
    "data": "[Error] 错误原因……",
}
```

#### 阿巴的接口：

创建一个 [aba_ocr.py](aba_ocr.py) ：

```python
class Api:  # 接口
    def __init__(self, globalArgd):
        self.lang = ""  # 当前语言
        api_key = globalArgd["api_key"]
        print("阿巴阿巴OCR获取 api_key： ", api_key)

    # 启动引擎。返回： "" 成功，"[Error] xxx" 失败
    def start(self, argd):
        self.lang = argd["language"]
        print("阿巴阿巴OCR当前语言： ", self.lang)
        return ""

    def stop(self):  # 停止引擎
        pass

    def runPath(self, imgPath: str):  # 路径识图
        res = self._ocr()
        return res

    def runBytes(self, imageBytes):  # 字节流
        res = self._ocr()
        return res

    def runBase64(self, imageBase64):  # base64字符串
        res = self._ocr()
        return res

    def _ocr(self):
        flag = True
        text = ""
        if self.lang == "zh_CN":
            text = "阿巴阿巴阿巴"
        elif self.lang == "zh_TW":
            text = "阿巴阿巴阿巴"
        elif self.lang == "en_US":
            text = "Aba Aba Aba"
        elif self.lang == "ja_JP":
            text = "あばあばあば"
        else:
            flag = False
            text = f"[Error] 未知的语言：{self.lang}"
        if flag:
            res = {
                "code": 100,
                "data": [
                    {
                        "text": text,
                        "box": [[0, 0], [200, 0], [200, 40], [0, 40]],
                        "score": 1,
                    }
                ],
            }
        else:
            res = {"code": 102, "data": text}
        return res
```

## 3. 构造插件结构

每个插件是一个文件夹。

文件夹名称唯一标识一个插件。文件夹名须为Ascii字符，且 **不能和python中已有的任何模块重名** 。

文件夹中必须有一个 [`__init__.py`](__init__.py) 。Umi会读取并载入`__init__.py`，以实现动态导入插件。

`__init__.py` 中必须定义一个字典 `PluginInfo` ，如下：
```python
PluginInfo = {
    "group": "ocr",  # 固定写法，定义插件组
    "global_options": ,  # 全局配置字典
    "local_options": ,  # 局部配置字典
    "api_class": ,  # 接口类
}
```

#### 阿巴的结构：

阿巴OCR插件文件夹为 `demo_AbaOCR` ，包含文件有：

[`__init__.py`](__init__.py)  
[`aba_ocr.py`](aba_ocr.py)  
[`aba_ocr_config.py`](aba_ocr_config.py)  
[`i18n.csv`](i18n.csv)  

其中 `__init__.py` 的内容为：

```python
from . import aba_ocr
from . import aba_ocr_config

# 插件信息
PluginInfo = {
    # 插件组别
    "group": "ocr",
    # 全局配置
    "global_options": aba_ocr_config.globalOptions,
    # 局部配置
    "local_options": aba_ocr_config.localOptions,
    # 接口类
    "api_class": aba_ocr.Api,
}
```

## 4. 放置插件

通过以上步骤，我们已经创建了一个可运行的 **阿巴OCR** 插件：`demo_AbaOCR`。

接下来，将它放入 Umi-OCR 的目录：

`UmiOCR-data\plugins`

启动 Umi-OCR ，即可在全局设置中，切换到 **阿巴OCR** 。
