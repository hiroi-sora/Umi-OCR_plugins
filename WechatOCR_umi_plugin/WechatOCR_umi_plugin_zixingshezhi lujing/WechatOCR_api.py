import base64
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'third_party_libs'))
import wechat_ocr

from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID


class Api:
    def __init__(self, globalArgd):
        """
        初始化接口类，不进行耗时操作
        """
        wechat_ocr_dir = globalArgd["wechat_ocr_dir"].replace("\\", "/")
        wechat_dir = globalArgd["wechat_dir"].replace("\\", "/")
        
        self.wechat_ocr_dir = wechat_ocr_dir
        self.wechat_dir = wechat_dir
        self.ocr_manager = None
        self._last_results = None
        print("OCR 接口初始化完成。")

    def start(self, argd):
        """
        启动引擎，可以进行耗时操作
        """
        try:
            self.ocr_manager = OcrManager(self.wechat_dir)
            self.ocr_manager.SetExePath(self.wechat_ocr_dir)
            self.ocr_manager.SetUsrLibDir(self.wechat_dir)
            self.lang = argd.get("language", "zh_CN")  # 设置语言（目前未使用）
            print(f"OCR 引擎启动，语言：{self.lang}")
            self.ocr_manager.SetOcrResultCallback(self._ocr_result_callback)
            self.ocr_manager.StartWeChatOCR()
            return ""
        except Exception as e:
            return f"[Error] 启动失败：{str(e)}"

    def stop(self):
        """
        停止引擎
        """
        if self.ocr_manager:
            self.ocr_manager.KillWeChatOCR()
            # 确保进程彻底关闭
            try:
                terminate_process_by_name("WeChatOCR.exe")
            except Exception as e:
                print(f"终止进程失败：{e}")
            print("OCR 引擎已停止。")

    def runPath(self, imgPath: str):
        """
        输入路径进行 OCR
        """
        try:
            return self._process_ocr(imgPath)
        except Exception as e:
            return {"code": 102, "data": f"[Error] 路径识别失败：{str(e)}"}

    def runBytes(self, imageBytes):
        """
        输入字节流进行 OCR
        """
        try:
            temp_path = self._save_temp_file(imageBytes, "temp_image.png")
            result = self._process_ocr(temp_path)
            os.remove(temp_path)  # 删除临时文件
            return result
        except Exception as e:
            return {"code": 102, "data": f"[Error] 字节流识别失败：{str(e)}"}

    def runBase64(self, imageBase64):
        """
        输入 Base64 字符串进行 OCR
        """
        try:
            imageBytes = base64.b64decode(imageBase64)
            return self.runBytes(imageBytes)
        except Exception as e:
            return {"code": 102, "data": f"[Error] Base64 识别失败：{str(e)}"}

    def _process_ocr(self, imgPath: str):
        """
        通用 OCR 处理逻辑
        """
        self._last_results = None  # 重置结果状态

        # 启动 OCR 任务
        start_time = time.time()
        self.ocr_manager.DoOCRTask(imgPath)

        # 等待任务完成，带超时机制
        timeout = 10
        while self.ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
            if time.time() - start_time > timeout:
                raise TimeoutError("OCR 任务超时")
            time.sleep(0.1)

        # 清空任务队列
        while not self.ocr_manager.m_task_id.empty():
            self.ocr_manager.m_task_id.get()

        elapsed_time = (time.time() - start_time) * 1000  # 计算耗时
        print(f"处理时间：{elapsed_time:.2f} 毫秒")

        if self._last_results is not None:
            return self._last_results
        else:
            return {"code": 102, "data": "[Error] 未能获取 OCR 结果"}

    def _ocr_result_callback(self, img_path: str, results: dict):
        """
        OCR 结果回调函数，将结果转换为统一格式
        """
        try:
            if "ocrResult" in results:
                ocr_data = [
                    {
                        "text": item["text"],
                        "box": [
                            [item["location"]["left"], item["location"]["top"]],
                            [item["location"]["right"], item["location"]["top"]],
                            [item["location"]["right"], item["location"]["bottom"]],
                            [item["location"]["left"], item["location"]["bottom"]],
                        ],
                        "score": 1,  # 默认置信度为 1
                    }
                    for item in results["ocrResult"]
                ]
                self._last_results = {"code": 100, "data": ocr_data}
            else:
                self._last_results = {"code": 101, "data": ""}
        except Exception as e:
            self._last_results = {"code": 102, "data": f"[Error] 结果处理失败：{str(e)}"}

    @staticmethod
    def _save_temp_file(imageBytes, file_name):
        """
        将字节流保存为临时文件
        """
        temp_path = os.path.join(os.getcwd(), file_name)
        with open(temp_path, "wb") as f:
            f.write(imageBytes)
        return temp_path
