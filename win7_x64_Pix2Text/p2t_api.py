import os
import sys
import site
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

    # 检查部分模型文件是否已经放置到系统指定目录，如果不存在，则复制文件
    def _checkSysModels(self):
        user = os.path.expanduser("~")
        mobilenet = "mobilenet_v2-7ebf99e0.pth"
        sysDir = user + "/.cache/torch/hub/checkpoints/"
        sysPath = sysDir + mobilenet
        modelPath = Models + "/torch/hub/checkpoints/" + mobilenet
        if not os.path.exists(sysDir):  # 创建系统路径
            os.makedirs(sysDir)
        if not os.path.exists(sysPath):
            shutil.copy2(modelPath, sysPath)
            print(f"模型库导入系统目录：{sysPath}")

    # 启动引擎。返回： "" 成功，"[Error] xxx" 失败
    def start(self, argd):
        if self.p2t:  # 引擎已启动
            return ""
        # 将依赖目录 添加到搜索路径
        site.addsitedir(SitePackages)
        try:
            # 模型库放置
            self._checkSysModels()

            # 补充输出接口，避免第三方库报错
            class _std:
                def write(self, e):
                    print(e)

            sys.__stdout__ = _std
            sys.__stderr__ = _std
            # 导入P2T库
            from pix2text import Pix2Text
            from pix2text.consts import (
                IMAGE_TYPES,
                LATEX_CONFIG_FP,
            )

            # 实例化P2T
            self.p2t = Pix2Text(
                # =============== 版面分析/公式检测模型 ===============
                analyzer_config={
                    "model_name": "mfd",
                    "model_type": "yolov7_tiny",  # 当前支持 [`yolov7_tiny`, `yolov7`]'
                    "model_backend": "pytorch",  # 仅支持pytorch
                    "model_categories": None,  # 基于 model_name 自动决定
                    "model_fp": Models + "/cnstd/1.2/analysis/mfd-yolov7_tiny.pt",
                    "model_arch_yaml": None,
                    "root": Models + "/cnstd",
                },
                # =============== 分类模型 ===============
                clf_config={
                    "base_model_name": "mobilenet_v2",
                    # 分类标签
                    "categories": IMAGE_TYPES,
                    "transform_configs": {
                        "crop_size": [150, 450],
                        "resize_size": 160,
                        "resize_max_size": 1000,
                    },
                    # 分类模型目录
                    "model_dir": Models + "/pix2text/clf",
                    "model_fp": Models
                    + "/pix2text/clf/pix2text-v0.2-mobilenet_v2-epoch=015-val-accuracy-epoch=0.9394-model.ckpt",
                },
                # =============== CnOcr 通用模型 ===============
                general_config={
                    # det 检测库
                    "det_root": Models + "/cnstd/1.2/ppocr",
                    "det_model_fp": Models
                    + "/cnstd/1.2/ppocr/ch_PP-OCRv3_det_infer.onnx",
                    "det_model_backend": "onnx",  # ['pytorch', 'onnx']
                    # "det_more_configs": Optional[Dict[str, Any]] = None,
                    # rec 识别库
                    "rec_root": Models + "/cnocr/2.2/densenet_lite_136-fc",
                    "rec_model_fp": Models
                    + "/cnocr/2.2/densenet_lite_136-fc/cnocr-v2.2-densenet_lite_136-fc-epoch=039-complete_match_epoch=0.8597-model.onnx",
                    "rec_model_backend": "onnx",  # ['pytorch', 'onnx']
                    "rec_vocab_fp": Models
                    + "/cnocr/2.2/densenet_lite_136-fc/label_cn.txt",
                    # "rec_more_configs": Optional[Dict[str, Any]] = None,
                    #
                },
                # =============== PP OCR 英文模型 ===============
                english_config={
                    # det 检测库
                    "det_root": Models + "/cnstd/1.2/ppocr",
                    "det_model_fp": Models
                    + "/cnstd/1.2/ppocr/en_PP-OCRv3_det_infer.onnx",
                    "det_model_backend": "onnx",  # ['pytorch', 'onnx']
                    # "det_more_configs": Optional[Dict[str, Any]] = None,
                    # rec 识别库
                    "rec_root": Models + "/cnocr/2.2/ppocr",
                    "rec_model_fp": Models
                    + "/cnocr/2.2/ppocr/en_PP-OCRv3_rec_infer.onnx",
                    "rec_model_backend": "onnx",  # ['pytorch', 'onnx']
                    # "rec_vocab_fp": Models + "/cnocr/2.2/ppocr/en_dict.txt",
                    # "rec_more_configs": Optional[Dict[str, Any]] = None,
                    #
                },
                # =============== 公式模型 ===============
                formula_config={
                    "config": LATEX_CONFIG_FP,
                    "model_fp": Models + "/pix2text/formula/weights.pth",
                    "resizer_checkpoint": Models
                    + "/pix2text/formula/image_resizer.pth",
                    # 'no_cuda': True,
                    "no_resize": False,
                },
                # =============== 识别阈值 ===============
                thresholds={
                    "formula2general": 0.65,  # 如果识别为 `formula` 类型，但得分小于此阈值，则改为 `general` 类型
                    "english2general": 0.75,  # 如果识别为 `english` 类型，但得分小于此阈值，则改为 `general` 类型
                },
                # 计算设备
                device="cpu",
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

    # 将p2t的结果转为Umi-OCR的格式
    def _standardized(self, res):
        datas = []
        for tb in res:
            # print(tb["line_number"], tb["text"])
            datas.append(
                {
                    "text": tb["text"],
                    "box": tb["position"].tolist(),  # np数组转list
                    "score": 1,  # 无置信度信息
                    "type": tb["type"],
                }
            )
        if datas:
            out = {"code": 100, "data": datas}
        else:
            out = {"code": 101, "data": ""}
        return out

    # 进行一次识图。可输入路径字符串或PIL Image
    def _run(self, img: Union[str, Image.Image]):
        if not self.p2t:
            res = {"code": 201, "data": "p2t not initialized."}
        else:
            try:
                res = self.p2t(img)
                res = self._standardized(res)
            except Exception as e:
                res = {"code": 202, "data": f"p2t recognize error: {e}"}
        return res

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
