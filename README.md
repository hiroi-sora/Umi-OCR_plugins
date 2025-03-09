<p align="center">
  <a href="https://github.com/hiroi-sora/Umi-OCR">
    <img width="200" height="128" src="https://tupian.li/images/2022/10/27/icon---256.png" alt="Umi-OCR">
  </a>
</p>

<h1 align="center">Umi-OCR 插件库</h1>

这里是存放开源软件 [Umi-OCR](https://github.com/hiroi-sora/Umi-OCR) 的插件的仓库。

Umi-OCR (v2 以上) 支持以插件的形式导入 OCR 引擎等组件，只需将插件文件放置于软件指定目录即可。

- [如何开发插件？](demo_AbaOCR)

## 如何安装插件

1. **在 [Releases](https://github.com/hiroi-sora/Umi-OCR_plugins/releases) 中下载插件压缩包。** 不要直接下载仓库的源代码！
2. **在 [Releases](https://github.com/hiroi-sora/Umi-OCR_plugins/releases) 中下载插件压缩包。** 不要直接下载仓库的源代码！！
3. **在 [Releases](https://github.com/hiroi-sora/Umi-OCR_plugins/releases) 中下载插件压缩包。** 不要直接下载仓库的源代码！！！

（重要的事情说三遍）

4. 将下载的文件解压，放置于：`UmiOCR-data/plugins`

## OCR 文字识别 插件

### win7_x64_PaddleOCR-json / linux_x64_PaddleOCR-json

- Umi-OCR_Paddle 版自带此插件
- 目前唯一支持 Windows、Linux 双平台的插件

> 性能和准确率优秀的开源离线 OCR 组件。支持 mkldnn 数学库加速，能充分榨干 CPU 的潜力。适合高配置电脑使用。

| 源仓库     | [PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)                   |
| ---------- | -------------------------------------------------------------------------------- |
| 下载       | [Releases](https://github.com/hiroi-sora/Umi-OCR_plugins/releases)               |
| 计算方式   | 本地，CPU                                                                        |
| 平台兼容   | Windows 7 x64 / Linux x64                                                        |
| 硬件兼容   | CPU 须带 AVX 指令集（不支持凌动 Atom，安腾 Itanium，赛扬 Celeron，奔腾 Pentium） |
| 附带语言库 | `简, 繁, 英, 日, 韩, 俄`                                                         |

---

### win7_x64_RapidOCR-json

- Umi-OCR_Rapid 版自带此插件

> 相当于PaddleOCR的“轻量版”。CPU兼容性好、内存占用低。速度相对慢一点。适合低配置老电脑使用。

| 源仓库     | [RapidOCR-json](https://github.com/hiroi-sora/RapidOCR-json)       |
| ---------- | ------------------------------------------------------------------ |
| 下载       | [Releases](https://github.com/hiroi-sora/Umi-OCR_plugins/releases) |
| 计算方式   | 本地，CPU                                                          |
| 平台兼容   | win7 以上，64 位                                                   |
| 硬件兼容   | 无特殊要求                                                         |
| 附带语言库 | `简, 繁, 英, 日, 韩, 俄`                                           |

---

### win7_x64_Pix2Text

> 支持中英文/数学公式/混合排版。插件体积大，加载速度较慢，识别速度快。

| 源仓库     | [Pix2Text](https://github.com/breezedeus/Pix2Text)                 |
| ---------- | ------------------------------------------------------------------ |
| 下载       | [Releases](https://github.com/hiroi-sora/Umi-OCR_plugins/releases) |
| 计算方式   | 本地，CPU                                                          |
| 平台兼容   | win7 以上，64 位                                                   |
| 硬件兼容   | 无特殊要求                                                         |
| 附带语言库 | `中文/英文/数学公式`                                               |

---

### TesseractOCR_umi_plugin

> 老牌开源模型，支持多国语言。速度较快，英文准确率优秀，中文准确率稍差。支持导入多个小语种识别库。  
> 自带排版识别模型，能整理复杂的文档排版，比Umi自带的排版解析器准确率更好。如果使用此插件，请在Umi的标签页设置中将“排版解析方案”设为“不做处理”。  

| 源仓库     | [TesseractOCR](https://github.com/tesseract-ocr/tesseract)               |
| ---------- | ------------------------------------------------------------------------ |
| 下载       | [Releases](https://github.com/qwedc001/tesseractOCR_umi_plugin/releases) |
| 计算方式   | 本地，CPU                                                                |
| 平台兼容   | win7 以上，64 位                                                         |
| 硬件兼容   | 无特殊要求                                                               |
| 附带语言库 | `简, 繁, 英, 日，数学公式` （另支持自行下载其他语言模型                  |

---

### chineseocr_umi_plugin

> 支持中英文识别，ChineseOCR 的轻量级模型，仍在接入适配中。

| 源仓库     | [ChineseOCR](https://github.com/DayBreak-u/chineseocr_lite/)           |
| ---------- | ---------------------------------------------------------------------- |
| 下载       | [Releases](https://github.com/qwedc001/chineseocr_umi_plugin/releases) |
| 计算方式   | 本地，CPU                                                              |
| 平台兼容   | win7 以上，64 位                                                       |
| 硬件兼容   | 无特殊要求                                                             |
| 附带语言库 | 中英文                                                                 |

---

### WechatOCR_umi_plugin

> 离线调用微信OCR进行ocr识别文字

| 源仓库     | [WechatOCR_umi_plugin](https://github.com/eaeful/WechatOCR_umi_plugin/releases)           |
| ---------- | ---------------------------------------------------------------------- |
| 下载       | [Releases](https://github.com/eaeful/WechatOCR_umi_plugin/releases) |
| 计算方式   | 本地，CPU                                                              |
| 平台兼容   | win7 以上，64 位                                                       |
| 硬件兼容   | 无特殊要求                                                             |
| 附带语言库 | 中英日文                                                                 |

---
### mistral.ai_umi_plugin

> 基于 Mistral AI OCR API 进行文字识别

| 源仓库     | [mistral.ai_umi_plugin](https://github.com/chunzhimoe/mistral.ai_umi_plugin/releases)           |
| ---------- | ---------------------------------------------------------------------- |
| 下载       | [Releases](https://github.com/chunzhimoe/mistral.ai_umi_plugin/releases) |
| 计算方式   | 云端，API 调用                                                              |
| 平台兼容   | 跨平台                                                       |
| 硬件兼容   | 无特殊要求                                                             |
| 附带语言库 | 多语言识别                                                                 |

## 插件开发

请见 [插件开发文档及 demo](demo_AbaOCR)。

# Umi-OCR 项目结构

### 各仓库：

- [主仓库](https://github.com/hiroi-sora/Umi-OCR)
- [插件库](https://github.com/hiroi-sora/Umi-OCR_plugins) 👈
- [Win 运行库](https://github.com/hiroi-sora/Umi-OCR_runtime_windows)
- [Linux 运行库](https://github.com/hiroi-sora/Umi-OCR_runtime_linux)

### 工程结构：

`**` 后缀表示本仓库(`插件库`)包含的内容。

```
Umi-OCR
└─ UmiOCR-data
   ├─ main.py
   ├─ version.py
   ├─ qt_res
   │  └─ 项目qt资源，包括图标和qml源码
   ├─ py_src
   │  └─ 项目python源码
   ├─ plugins **
   │  └─ 插件
   └─ i18n
      └─ 翻译文件
```
