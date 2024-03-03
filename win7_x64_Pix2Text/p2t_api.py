import os
import sys
import site
import time
import base64
import shutil
from PIL import Image
from io import BytesIO
from typing import Union

# 当前目录
CurrentDir = os.path.dirname(os.path.abspath(__file__))
# 依赖包目录
SitePackages = os.path.join(CurrentDir, "site-packages")
# 模型库目录
Models = os.path.join(CurrentDir, "models")


class Api:  # 接口
    def __init__(self, globalArgd):
        self.p2t = None
        self.argd = {
            "recognize_text": True,  # 启用文字识别
            "recognize_formula": True,  # 启用公式识别
            "resized_shape": 608,  # 缩放限制
        }

    # 启动引擎。返回： "" 成功，"[Error] xxx" 失败
    def start(self, argd):
        self.argd = argd  # 记录局部参数
        self.argd["resized_shape"] = int(argd["resized_shape"])  # 确保类型正确
        if self.p2t:  # 引擎已启动
            return ""
        # 将依赖目录 添加到搜索路径
        site.addsitedir(SitePackages)
        try:
            # 补充输出接口，避免第三方库报错
            class _std:
                def write(self, e):
                    print(e)

            sys.__stdout__ = _std
            sys.__stderr__ = _std
            # 导入依赖库
            t1 = time.time()
            from pix2text import Pix2Text
            import numpy as np

            t2 = time.time()
            print("import 耗时：", t2 - t1)

            self.np = np
            # 实例化P2T
            self.p2t = Pix2Text(
                # 分类模型
                analyzer_config=dict(
                    model_name="mfd",
                    model_type="yolov7_tiny",
                    model_fp=os.path.join(Models, "mfd-yolov7_tiny.pt"),
                ),
                # 公式模型
                formula_config=dict(
                    model_name="mfr",
                    model_backend="onnx",
                    model_dir=os.path.join(Models, "mfr-onnx"),
                ),
                # 文字模型
                text_config=dict(
                    # 检测
                    det_model_name="ch_PP-OCRv3_det",
                    det_model_backend="onnx",
                    det_model_fp=os.path.join(Models, "ch_PP-OCRv3_det_infer.onnx"),
                    # 识别
                    rec_model_name="densenet_lite_136-gru",
                    rec_model_backend="onnx",
                    rec_model_fp=os.path.join(
                        Models,
                        "cnocr-v2.3-densenet_lite_136-gru-epoch=004-ft-model.onnx",
                    ),
                ),
            )
            return ""
        except Exception as e:
            self.p2t = None
            err = str(e)
            if "DLL load failed while importing onnxruntime_pybind11_state" in str(e):
                err += "\n请下载 Please download VC++2022 :\nhttps://aka.ms/vs/17/release/vc_redist.x64.exe"
            return f"[Error] {err}"

    def stop(self):
        self.p2t = None

    # 将p2t的text结果转为Umi-OCR的格式
    def _text_standardized(self, res):
        datas = []
        for tb in res:
            datas.append(
                {
                    "text": tb["text"],
                    "box": tb["position"].tolist(),  # np数组转list
                    "score": 1,  # 无置信度信息
                }
            )
        if datas:
            return {"code": 100, "data": datas}
        else:
            return {"code": 101, "data": ""}

    # 将p2t的混合结果转为Umi-OCR的格式
    def _tf_standardized(self, res):
        # print("获取结果：", res)
        resL = len(res)
        tbs = []

        # 合并box
        def mergeBox(b1, b2):
            p00 = min([b1[0][0], b1[3][0], b2[0][0], b2[3][0]])
            p01 = min([b1[0][1], b1[1][1], b2[0][1], b2[1][1]])
            p20 = max([b1[1][0], b1[2][0], b2[1][0], b2[2][0]])
            p21 = max([b1[2][1], b1[3][1], b2[2][1], b2[3][1]])
            return [
                [p00, p01],
                [p20, p01],
                [p20, p21],
                [p00, p21],
            ]

        # 当前行信息
        line_number = 0
        index = 0
        while True:
            if index == resL:
                break
            # 一行
            text = ""
            score = 0
            num = 0
            box = res[index]["position"].tolist()
            # 遍历一行
            while True:
                # 行结束
                data = res[index]
                if data["line_number"] > line_number:
                    line_number = data["line_number"]
                    break
                # 行收集
                text += data["text"]
                score += data["score"] if "score" in data else 1.0
                num += 1
                box = mergeBox(data["position"].tolist(), box)
                index += 1
                if index == resL:
                    break
            print(index, score, num)
            # 整合一行
            tbs.append(
                {
                    "text": text,
                    "score": score / num,
                    "box": box,
                }
            )
        if tbs:
            return {"code": 100, "data": tbs}
        else:
            return {"code": 101, "data": ""}

    # 进行一次识图。可输入路径字符串或PIL Image
    def _run(self, img: Union[str, Image.Image]):
        if not self.p2t:
            return {"code": 201, "data": "p2t not initialized."}
        t, f = self.argd["recognize_text"], self.argd["recognize_formula"]
        resized_shape = self.argd["resized_shape"]
        try:
            if t and f:  # 混合识别
                res = self.p2t.recognize(img, resized_shape=resized_shape)
                return self._tf_standardized(res)
            elif t:  # 仅文字识别
                # res = self.p2t.recognize_text(img)
                res = self.p2t.text_ocr.ocr(self.np.array(img))
                return self._text_standardized(res)
            elif f:  # 仅公式识别
                im = img
                if isinstance(im, str):  # 读入路径
                    im = Image.open(im)
                text = self.p2t.recognize_formula(im)
                w, h = im.size
                if text:
                    return {
                        "code": 100,
                        "data": [
                            {
                                "box": [[0, 0], [w, 0], [w, h], [0, h]],
                                "score": 1,
                                "text": text,
                            }
                        ],
                    }
                else:
                    return self._text_standardized([])
            else:
                return {
                    "code": 202,
                    "data": "未启用文字识别或公式识别。\nText or formula recognition is not enabled.",
                }
        except Exception as e:
            return {"code": 203, "data": f"p2t recognize error: {e}"}

    def runPath(self, imgPath: str):  # 路径识图
        return self._run(imgPath)

    def runBytes(self, imageBytes):  # 字节流
        bytesIO = BytesIO(imageBytes)
        image = Image.open(bytesIO)
        return self._run(image)

    def runBase64(self, imageBase64):  # base64字符串
        imageBytes = base64.b64decode(imageBase64)
        return self.runBytes(imageBytes)


"""
如果Win7报错
[Error] DLL load failed while importing onnxruntime_pybind11_state: 找不到指定的程序。
那么下载VC++2019
https://aka.ms/vs/16/release/VC_redist.x64.exe
"""
