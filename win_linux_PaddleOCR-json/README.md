# PaddleOCR-json 插件

兼容 `Windows 7 x64`、`Linux x64` 。

- [Windows 简易部署](#win-1)
- [Windows 源码部署](#win-2)
- [Linux 简易部署](#linux-1)
- [Linux 源码部署](#linux-2)

<a id="win-1"></a>

## Windows 简易部署步骤

- 按照 [Umi-OCR Linux 运行环境](https://github.com/hiroi-sora/Umi-OCR_runtime_linux) 的说明，配置 Umi-OCR 本体。
- 访问 [Umi-OCR_plugins 发布页](https://github.com/hiroi-sora/Umi-OCR_plugins/releases) ，下载最新的 Windows 发行包 `win7_x64_PaddleOCR-json_**.7z` ，解压。
- 解压得到的文件夹，丢到 Umi-OCR 的插件目录 `UmiOCR-data/plugins` 。

<a id="win-2"></a>

## Windows 源码部署步骤

### 第1步：准备 Umi-OCR 本体、插件源码

- 按照 [Umi-OCR Windows 运行环境](https://github.com/hiroi-sora/Umi-OCR_runtime_windows) 的说明，配置 Umi-OCR 本体。
- 在本体目录中，创建一个 `tools` 目录。
- 下载 **插件仓库** 源码：

```sh
git clone https://github.com/hiroi-sora/Umi-OCR_plugins.git
```

### 第2步：准备 PaddleOCR-json 可执行文件

#### 方式1：直接下载

- 浏览器访问 [PaddleOCR-json 发布页](https://github.com/hiroi-sora/PaddleOCR-json/releases) ，获取最新的 Windows 发行包 `PaddleOCR-json_v1.X.X_windows_x86-64.7z` 的链接，下载压缩包并解压。
- 解压出来的文件夹，改名为 `win7_x64_PaddleOCR-json` 。

#### 方式2：从源码构建

- 见 [PaddleOCR-json Windows 构建指南](https://github.com/hiroi-sora/PaddleOCR-json/blob/main/cpp/README.md) 。

- 假设你完成了编译，那么将生成的所有可执行文件拷贝到一个 `win7_x64_PaddleOCR-json` 文件夹中。

### 第3步：组装插件，放置插件

- 将 `tools\Umi-OCR_plugins\win_linux_PaddleOCR-json` 中的所有文件，复制到 `win7_x64_PaddleOCR-json` 。
- 在 `win7_x64_PaddleOCR-json` 中，双击 `PaddleOCR-json.exe` 测试。正常情况下，应该打开一个控制台窗口，显示 `OCR init completed.` 。
- 将 `win7_x64_PaddleOCR-json` 整个文件夹，复制到 `UmiOCR-data\plugins` 中。

### 最终测试

启动 Umi-OCR ，测试各种功能吧。

在全局设置→拉到最底下，可以看到 PaddleOCR-json 插件相关的性能设置。

<a id="linux-1"></a>

## Linux 简易部署步骤

- 按照 [Umi-OCR Linux 运行环境](https://github.com/hiroi-sora/Umi-OCR_runtime_linux) 的说明，配置 Umi-OCR 本体。
- 去到 Umi-OCR 的插件目录 `UmiOCR-data/plugins`
- 浏览器访问 [Umi-OCR_plugins 发布页](https://github.com/hiroi-sora/Umi-OCR_plugins/releases) ，获取最新的 Linux 发行包 `linux_x64_PaddleOCR-json` 的链接，下载压缩包并解压。

示例：

```
# 去到插件目录
cd UmiOCR-data/plugins
# 如果没有则创建
# mkdir UmiOCR-data/plugins
# 下载
wget https://github.com/hiroi-sora/Umi-OCR_plugins/releases/download/2.1.3_dev/linux_x64_PaddleOCR-json_v140_beta.tar.xz
# 解压
tar -v -xf linux_x64_PaddleOCR-json_v140_beta.tar.xz
# 完成，打开 Umi-OCR 软件，进行测试吧
```

<a id="linux-2"></a>

## Linux 源码部署步骤

### 第1步：准备 Umi-OCR 本体、插件源码

- 按照 [Umi-OCR Linux 运行环境](https://github.com/hiroi-sora/Umi-OCR_runtime_linux) 的说明，配置 Umi-OCR 本体。
- 在本体目录中，创建一个 `tools` 目录：

```sh
mkdir tools
cd tools
```

- 下载 插件仓库源码：

```sh
git clone https://github.com/hiroi-sora/Umi-OCR_plugins.git
```

### 第2步：准备 PaddleOCR-json 可执行文件

#### 方式1：直接下载

- 浏览器访问 [PaddleOCR-json 发布页](https://github.com/hiroi-sora/PaddleOCR-json/releases) ，获取最新的 Linux 发行包 `PaddleOCR-json_v1.X.X_debian_gcc_x86-64.tar.xz` 的链接，下载压缩包并解压。示例：

```
# 下载
wget https://github.com/hiroi-sora/PaddleOCR-json/releases/download/v1.4.0-beta.2/PaddleOCR-json_v1.4.0.beta.2_debian_gcc_x86-64.tar.xz
# 解压
tar -v -xf PaddleOCR-json_v1.4.0.beta.2_debian_gcc_x86-64.tar.xz
# 改个短一点的名，更好操作
mv PaddleOCR-json_v1.4.0_debian_gcc_x86-64 PaddleOCR-json-bin
# 测试一下。如果没有测试图片，那么留空即可。
./PaddleOCR-json-bin/run.sh --image_path="测试图片路径"
# 如果输出 OCR init completed. 那么测试通过。
# 如果输出 OCR init completed. 后没有停止，那么按 Ctrl+C 强制停止即可。
```

#### 方式2：从源码构建

- 见 [PaddleOCR-json Linux 构建指南](https://github.com/hiroi-sora/PaddleOCR-json/blob/main/cpp/README-linux.md) 。

- 假设你完成了编译，那么将生成的所有可执行文件拷贝到前文所述的 `tools/PaddleOCR-json-bin` 目录。

#### 准备完成

- 通过以上步骤，你应该得到这样的目录结构：

```
Umi-OCR
├─ umi-ocr.sh
├─ UmiOCR-data
└─ tools
   ├─ Umi-OCR_plugins
   └─ PaddleOCR-json-bin
```

### 第3步：组装插件，放置插件

- 确保当前在 `tools` 目录中，其中有 `Umi-OCR_plugins` 和 `PaddleOCR-json-bin` 。
- 进行以下操作：

```sh
# 创建插件目录
mkdir -p linux_x64_PaddleOCR-json
# 复制可执行文件
cp -rf PaddleOCR-json-bin/* linux_x64_PaddleOCR-json/
# 复制插件控制源码
cp -rf Umi-OCR_plugins/win_linux_PaddleOCR-json/* linux_x64_PaddleOCR-json/
# 将组装完毕的完整插件，放入 Umi-OCR 的插件目录
cp -rf linux_x64_PaddleOCR-json ../UmiOCR-data/plugins/
```

### 最终测试

启动 Umi-OCR ，测试各种功能吧。

在全局设置→拉到最底下，可以看到 PaddleOCR-json 插件相关的性能设置。
