# Umi-OCR 插件库

这里是存放 [Umi-OCR_v2](https://github.com/hiroi-sora/Umi-OCR_v2) 的插件的仓库。

Umi-OCR 支持以插件的形式导入OCR引擎等组件，只需将插件文件放置于软件指定目录即可。

注意，插件可能会限制平台（win7、win10……），下载插件前请检查是否与你的平台是否相符。

## 下载

在 Release 中下载插件。

## OCR插件

放置位置：`UmiOCR-data/plugins/ocr`

---

### win10_PaddleOCR-json

> 性能和准确率优秀的开源离线OCR组件。支持mkldnn数学库加速，能充分榨干CPU的潜力。适合高配置电脑使用。

| 源仓库     | [PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)              |
| ---------- | --------------------------------------------------------------------------- |
| 离线       | √                                                                           |
| 平台兼容   | win10以上，64位                                                             |
| 硬件兼容   | CPU，须带AVX指令集（不支持凌动Atom，安腾Itanium，赛扬Celeron，奔腾Pentium） |
| 附带语言库 | `简, 繁, 英, 日, 韩, 俄`                                                    |

---

### win7_RapidOCR-json

> 轻量、高兼容性的开源离线OCR组件。支持win7，内存与CPU占用低。速度相对慢一点。适合低配置老电脑使用。

| 源仓库     | [PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json) |
| ---------- | -------------------------------------------------------------- |
| 离线       | √                                                              |
| 平台兼容   | win7以上，64位                                                 |
| 硬件兼容   | 无特殊要求                                                     |
| 附带语言库 | `简, 繁, 英, 日, 韩, 俄`                                       |

---

## 插件开发

文档待补充……