# 适用于 Umi-OCR 文字识别工具 的 WeChatOCR 插件


WeChatOCR 是一款专为 [Umi-OCR](https://github.com/hiroi-sora/Umi-OCR) 设计的文字识别插件。

---

## 插件介绍

通过将 WeChatOCR 插件加载到 Umi-OCR，可以直接使用微信 离线OCR 的强大功能来识别文字。

### 与其他插件（如 PaddleOCR）的对比优势

- 👍**精准度更高**：对生僻字和使用频率较低的字符识别效果优于 PaddleOCR。
- 👍**速度略胜一筹**：识别速度相比 PaddleOCR 略快。
- 👍**多语言支持**：支持中文、英文、日语等多语言的自动识别，无需手动切换语言模型。
- 👍**智能换行**：当排版解析方案设置为 “不处理” 时，识别内容会根据输出结果自动换行。如果不需要换行，可将排版解析方案设置为 “单栏-无换行”。

---
试一试用WeChatOCR和PaddleOCR识别下面这个图：
![18-230537](https://github.com/user-attachments/assets/4f13b12f-c09e-4566-b859-306dddd49944)
![对比](https://github.com/user-attachments/assets/186c4900-7c37-4beb-b0f7-9ec97c2cb226)



## 插件版本说明

WeChatOCR 插件提供以下两种版本，供用户选择：

### 1. 微信本地 OCR 模型版本（WechatOCR_umi_plugin_zidai ocr）

- 插件内置了关键文件：`wechatocr.exe`、`wechat` 文件夹、`mmmojo.dll` 和 `mmmojo_64.dll`等。
- **无需安装微信，也无需运行微信**，即可直接调用微信 OCR 功能完成文字识别。
  
- **注意事项：**
  - 本版本可能涉及微信文件的版权或许可问题。这些文件由腾讯公司所有，未经授权，可能不符合其使用条款。
  - 本版本的分发仅用于技术交流和学习目的。请勿用于商业用途，或以任何方式侵犯腾讯的版权。
- **免责声明：**
  - 使用此版本可能存在法律风险，下载和使用由用户自行承担责任。
### 2. 微信 OCR 用户自定义路径版本（WechatOCR_umi_plugin_zixingshezhi lujing）

- 用户需在 Umi-OCR 的全局设置中，手动填写以下路径：
  - 电脑中的微信安装目录的完整路径。
  - 电脑中的`WeChatOCR.exe` 文件路径。
  - 
- **优点：**
  - 避免分发闭源文件，无版权风险。
  - 用户完全控制所需文件的来源和版本。
- **缺点：**
  - 微信更新后，本插件可能路径失效，你需要自己更新路径
- **推荐人群：**
  - 对合规性和合法性有更高要求的用户。
  - 熟悉文件配置并愿意进行手动设置的用户。
  **要使用此版本，您需要准备以下内容：**

  - **`wechatocr.exe`**：例如  
    `C:\Users\Administrator\AppData\Roaming\Tencent\WeChat\XPlugin\Plugins\WeChatOCR\7079\extracted\WeChatOCR.exe`
  - **`wechat` 文件夹**：例如  
    `C:\Program Files (x86)\Tencent\WeChat\[3.9.8.25]`

  配置完成后，即可调用本地微信进行文字识别。

---

## 两个版本的区别

| 特性               | 微信本地 OCR 模型版本           | 微信 OCR 用户自定义路径版本    |
|--------------------|---------------------------------|--------------------------------|
| **初次识别速度**   | 可能首次加载稍慢（数百毫秒），后续识别正常    | 可能首次加载稍慢（数百毫秒），后续识别正常   |
| **使用便捷性**     | 更加便捷，无需额外配置          | 需手动配置路径，稍微复杂       |
| **版权与 LICENSE** | 可能涉及许可协议和 LICENSE 风险，仅用于技术交流和学习目的。请勿用于商业用途     | 用户自行选择路径，降低法律风险，优先推荐这个"用户自定义路径版本"版本。   |

---

## 使用说明

1. 访问https://github.com/eaeful/WechatOCR_umi_plugin/releases，下载对应的版本并解压插件包，放入 Umi-OCR/UmiOCR-data/plugins 文件夹中。
2. 打开 Umi-OCR，并加载 WeChatOCR 插件。
3. （可选）根据版本选择是否配置路径：
   - **本地 OCR 模型版本**：无需额外配置，直接使用。
   - **用户自定义路径版本**：在 Umi-OCR 设置中填写对应路径，并准备所需文件和文件夹。
4. 开始识别文字！

---

## 注意事项

- 两个版本在首次加载时可能会有轻微的延迟，但后续识别速度无差异。
- 我只在windows 10 运行过这个插件，其他系统版本不清楚，请自行测试
- 使用本地 OCR 模型版本时，请确保遵循相关版权协议和 LICENSE 要求。

---
## 可能出现的问题和解决方法
- 1：如果在使用本插件的"微信OCR用户自定义路径版本"，当软件正确设置路径后，仍然提示找不到路径。可以通过任务管理器先把umi-OCR.exe软件进行结束进程，然后以管理员身份重新打开此软件。
- 2：如果遇到前面识别文字，能够正常运行，但是后面识别就一直没有响应。可以通过任务管理器把软件umi-OCR.exe跟Wechatocr.exe的进程进行结束，然后重新打开软件。
---
## 感谢
- https://github.com/kanadeblisst00/wechat_ocr
- https://github.com/EEEEhex/QQImpl
- https://github.com/swigger/wechat-ocr
- https://www.52pojie.cn/thread-1959012-1-1.html
- https://www.52pojie.cn/thread-1958424-1-1.html

---

欢迎通过 Issue 或 Pull Request 提交建议和改进意见！ 🎉
