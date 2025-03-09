# Mistral OCR 插件

这是一个基于Mistral AI OCR API的Umi-OCR插件，可以帮助您使用Mistral的OCR服务进行文字识别。

## 安装说明

1. 从[Releases](https://github.com/yourusername/mistral-ocr-plugin/releases)页面下载最新版本
2. 将整个`MistralOCR`文件夹放入Umi-OCR的插件目录：
   - Windows: `%APPDATA%\Umi-OCR\plugins\`
   - Linux: `~/.config/Umi-OCR/plugins/`
   - macOS: `~/Library/Application Support/Umi-OCR/plugins/`
3. 重启Umi-OCR
4. 在设置中启用Mistral OCR插件

> **注意**: 插件已内置所有必要的依赖库，无需手动安装任何依赖。

## 配置说明

### 全局配置
- **API密钥**: 您的Mistral API密钥，可以从[Mistral AI控制台](https://console.mistral.ai/)获取
- **模型**: OCR模型名称，默认为`mistral-ocr-latest`
- **超时时间**: API请求的超时时间（秒）
- **包含图像Base64**: 是否在响应中包含图像的Base64编码（高级选项）

### 局部配置
- **语言**: 识别的目标语言，支持自动检测、中文、英文等多种语言
- **最小图像尺寸**: 提取图像的最小尺寸（像素），0表示不限制（高级选项）

## 使用方法

1. 启动Umi-OCR后，在全局设置中切换到"Mistral OCR"
2. 配置您的API密钥和其他参数
3. 在识别界面选择"文字识别（Mistral OCR）"
4. 设置识别语言等参数
5. 开始使用OCR功能

## 故障排除

如果遇到OCR识别失败，请检查：

1. **API密钥错误**: 确保您在插件设置中输入了有效的Mistral AI API密钥
2. **网络错误**: 检查您的网络连接是否正常，插件需要网络访问Mistral AI API
3. **超时错误**: 如果您处理的图像较大，请尝试在设置中增加超时值
4. **额度不足**: 确保您的Mistral账户有足够的API调用额度

## 项目结构

```
MistralOCR/
├── __init__.py           # 插件入口点
├── mistral_ocr.py        # OCR实现
├── mistral_ocr_config.py # 插件配置
├── i18n.csv              # 国际化字符串
└── README.md             # 文档
```

## 开发指南

### 从源代码构建

1. 克隆仓库:
   ```
   git clone https://github.com/yourusername/mistral-ocr-plugin.git
   ```
2. 进行您的修改
3. 通过将`MistralOCR`文件夹复制到Umi-OCR插件目录来测试插件

### 自动发布

本项目使用GitHub Actions自动构建和发布插件包。当您创建一个新的标签（如`v1.0.0`）时，工作流将自动构建插件包并创建一个新的发布版本。

## 许可证

本项目采用MIT许可证 - 详情请参阅LICENSE文件。

## 致谢

- 感谢[Mistral AI](https://mistral.ai/)提供OCR API
- 感谢[Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)提供优秀的OCR平台

---

# Mistral OCR Plugin

*[English version below](#mistral-ocr-plugin-for-umi-ocr)*

## Mistral OCR Plugin for Umi-OCR

A powerful OCR plugin for Umi-OCR that utilizes Mistral AI's OCR capabilities to extract text from images.

### Features

- High-accuracy text recognition powered by Mistral AI's OCR API
- Supports multiple languages
- Simple integration with Umi-OCR
- No external dependencies required
- Easy configuration

### Installation

1. Download the latest release from the [Releases](https://github.com/yourusername/mistral-ocr-plugin/releases) page
2. Extract the `MistralOCR` folder to the Umi-OCR plugins directory:
   - Windows: `%APPDATA%\Umi-OCR\plugins\`
   - Linux: `~/.config/Umi-OCR/plugins/`
   - macOS: `~/Library/Application Support/Umi-OCR/plugins/`
3. Restart Umi-OCR
4. Enable the Mistral OCR plugin in the Umi-OCR settings

### Configuration

#### Required Settings

- **API Key**: Your Mistral AI API key. You can obtain one from [Mistral AI Platform](https://console.mistral.ai/).

#### Optional Settings

- **Model**: The Mistral OCR model to use (default: `mistral-ocr-latest`)
- **Timeout**: Request timeout in seconds (default: 30)
- **Include Image Base64**: Whether to include the base64-encoded image in the response (default: false)
- **Image Minimum Size**: Minimum size for the image in pixels (default: 0)

### Usage

1. Open Umi-OCR
2. Select "Mistral OCR" as the OCR engine
3. Configure your API key and other settings
4. Use Umi-OCR as normal to process images

### Troubleshooting

#### Common Issues

- **API Key Error**: Ensure you have entered a valid Mistral AI API key in the plugin settings.
- **Network Error**: Check your internet connection. The plugin requires internet access to communicate with the Mistral AI API.
- **Timeout Error**: If you're processing large images, try increasing the timeout value in the settings.

### Development

#### Project Structure

```
MistralOCR/
├── __init__.py           # Plugin entry point
├── mistral_ocr.py        # OCR implementation
├── mistral_ocr_config.py # Plugin configuration
├── i18n.csv              # Internationalization strings
└── README.md             # Documentation
```

#### Automated Releases

This project uses GitHub Actions to automatically build and release plugin packages. When you create a new tag (e.g., `v1.0.0`), the workflow will automatically build the plugin package and create a new release.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgements

- [Mistral AI](https://mistral.ai/) for providing the OCR API
- [Umi-OCR](https://github.com/hiroi-sora/Umi-OCR) for the excellent OCR platform
