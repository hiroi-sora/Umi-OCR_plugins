import base64
import json
import time
import os
import sys
from urllib.parse import urlparse
import socket
import ssl
from http.client import HTTPConnection, HTTPSConnection

# 内置HTTP客户端实现，避免依赖requests库
class Response:
    """HTTP响应类，模拟requests.Response"""
    def __init__(self, status_code, headers, content):
        self.status_code = status_code
        self.headers = headers
        self._content = content
        self._text = None
        self._json = None
    
    @property
    def content(self):
        """获取响应内容的字节流"""
        return self._content
    
    @property
    def text(self):
        """获取响应内容的文本形式"""
        if self._text is None:
            self._text = self._content.decode('utf-8')
        return self._text
    
    def json(self):
        """解析JSON响应"""
        if self._json is None:
            self._json = json.loads(self.text)
        return self._json

class RequestException(Exception):
    """请求异常基类"""
    pass

class Timeout(RequestException):
    """请求超时异常"""
    pass

class ConnectionError(RequestException):
    """连接错误异常"""
    pass

# 创建一个简单的requests模块替代品
class SimpleRequests:
    def __init__(self):
        self.exceptions = type('exceptions', (), {
            'Timeout': Timeout,
            'ConnectionError': ConnectionError,
            'RequestException': RequestException
        })
    
    def post(self, url, headers=None, json_data=None, timeout=30):
        """
        发送POST请求
        
        参数:
            url (str): 请求URL
            headers (dict): 请求头
            json_data (dict): JSON请求体
            timeout (int): 超时时间（秒）
        
        返回:
            Response: 响应对象
        """
        parsed_url = urlparse(url)
        
        # 确定是HTTP还是HTTPS
        is_https = parsed_url.scheme == 'https'
        
        # 设置主机和端口
        host = parsed_url.netloc
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        else:
            port = 443 if is_https else 80
        
        # 准备请求路径
        path = parsed_url.path
        if not path:
            path = '/'
        if parsed_url.query:
            path = f"{path}?{parsed_url.query}"
        
        # 准备请求头
        if headers is None:
            headers = {}
        
        # 准备请求体
        body = None
        if json_data is not None:
            body = json.dumps(json_data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
            headers['Content-Length'] = str(len(body))
        
        try:
            # 创建连接
            if is_https:
                conn = HTTPSConnection(host, port, timeout=timeout)
            else:
                conn = HTTPConnection(host, port, timeout=timeout)
            
            # 发送请求
            conn.request('POST', path, body=body, headers=headers)
            
            # 获取响应
            resp = conn.getresponse()
            
            # 读取响应内容
            content = resp.read()
            
            # 获取响应头
            headers = {k.lower(): v for k, v in resp.getheaders()}
            
            # 创建响应对象
            response = Response(resp.status, headers, content)
            
            # 关闭连接
            conn.close()
            
            return response
            
        except socket.timeout:
            raise Timeout("请求超时")
        except (socket.error, ssl.SSLError) as e:
            raise ConnectionError(f"连接错误: {str(e)}")
        except Exception as e:
            raise RequestException(f"请求失败: {str(e)}")

# 创建requests模块替代品的实例
requests = SimpleRequests()
HTTP_CLIENT_AVAILABLE = True

class Api:
    def __init__(self, globalArgd):
        """初始化Mistral OCR API接口"""
        self.api_key = globalArgd.get("api_key", "")
        self.model = globalArgd.get("model", "mistral-ocr-latest")
        self.timeout = globalArgd.get("timeout", 30)
        self.include_image_base64 = globalArgd.get("include_image_base64", False)
        self.language = "auto"
        self.image_min_size = 0
        self.api_url = "https://api.mistral.ai/v1/ocr"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        # 检查依赖是否已安装
        self.dependency_error = self._check_dependencies()

    def _check_dependencies(self):
        """检查必要的依赖是否已安装"""
        if not HTTP_CLIENT_AVAILABLE:
            return "[Error] HTTP客户端初始化失败。请联系插件作者。"
        return ""

    def start(self, argd):
        """启动引擎，设置局部配置"""
        # 首先检查依赖错误
        if self.dependency_error:
            return self.dependency_error
            
        if not self.api_key:
            return "[Error] API密钥未设置，请在全局设置中配置Mistral API密钥。"
        
        self.language = argd.get("language", "auto")
        self.image_min_size = argd.get("image_min_size", 0)
        return ""

    def stop(self):
        """停止引擎"""
        pass

    def runPath(self, imgPath):
        """通过图片路径进行OCR识别"""
        # 检查依赖错误
        if self.dependency_error:
            return {"code": 102, "data": self.dependency_error}
            
        try:
            # 读取图片文件并转换为base64
            with open(imgPath, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            
            return self._process_image_base64(image_base64)
        except Exception as e:
            return {"code": 102, "data": f"[Error] 图片读取失败: {str(e)}"}

    def runBytes(self, imageBytes):
        """通过图片字节流进行OCR识别"""
        # 检查依赖错误
        if self.dependency_error:
            return {"code": 102, "data": self.dependency_error}
            
        try:
            image_base64 = base64.b64encode(imageBytes).decode('utf-8')
            return self._process_image_base64(image_base64)
        except Exception as e:
            return {"code": 102, "data": f"[Error] 图片处理失败: {str(e)}"}

    def runBase64(self, imageBase64):
        """通过base64编码的图片进行OCR识别"""
        # 检查依赖错误
        if self.dependency_error:
            return {"code": 102, "data": self.dependency_error}
            
        try:
            return self._process_image_base64(imageBase64)
        except Exception as e:
            return {"code": 102, "data": f"[Error] 图片处理失败: {str(e)}"}

    def _process_image_base64(self, image_base64):
        """处理base64编码的图片并调用Mistral OCR API"""
        if not HTTP_CLIENT_AVAILABLE:
            return {"code": 102, "data": self.dependency_error}
            
        try:
            # 构建API请求
            payload = {
                "model": self.model,
                "document": {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                },
                "include_image_base64": self.include_image_base64,
                "image_min_size": self.image_min_size
            }
            
            # 发送请求到Mistral API
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json_data=payload,
                timeout=self.timeout
            )
            
            # 检查响应状态
            if response.status_code != 200:
                error_message = f"API请求失败: HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_message += f" - {error_data['error']['message']}"
                except:
                    pass
                return {"code": 102, "data": f"[Error] {error_message}"}
            
            # 解析响应数据
            ocr_result = response.json()
            
            # 转换为Umi-OCR期望的格式
            return self._convert_to_umi_format(ocr_result)
            
        except requests.exceptions.Timeout:
            return {"code": 102, "data": f"[Error] API请求超时，请检查网络连接或增加超时时间。"}
        except requests.exceptions.ConnectionError:
            return {"code": 102, "data": f"[Error] 网络连接错误，请检查网络连接。"}
        except Exception as e:
            return {"code": 102, "data": f"[Error] OCR处理失败: {str(e)}"}

    def _convert_to_umi_format(self, mistral_result):
        """将Mistral OCR结果转换为Umi-OCR期望的格式"""
        try:
            # 检查是否有页面数据
            if not mistral_result.get("pages"):
                return {"code": 101, "data": ""}
            
            # 提取第一页的markdown文本
            page = mistral_result["pages"][0]
            markdown_text = page.get("markdown", "")
            
            if not markdown_text:
                return {"code": 101, "data": ""}
            
            # 提取文本内容
            text_blocks = []
            
            # 从markdown中提取文本并创建文本块
            lines = markdown_text.split("\n")
            y_offset = 0
            line_height = 40  # 假设每行高度为40像素
            
            for line in lines:
                if line.strip():  # 忽略空行
                    # 创建文本块
                    text_block = {
                        "text": line,
                        "box": [[0, y_offset], [800, y_offset], [800, y_offset + line_height], [0, y_offset + line_height]],
                        "score": 1.0
                    }
                    text_blocks.append(text_block)
                    y_offset += line_height
            
            # 如果没有提取到文本块，返回无文字结果
            if not text_blocks:
                return {"code": 101, "data": ""}
            
            # 返回成功结果
            return {
                "code": 100,
                "data": text_blocks
            }
            
        except Exception as e:
            return {"code": 102, "data": f"[Error] 结果转换失败: {str(e)}"}
