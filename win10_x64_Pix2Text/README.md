# P2T插件 开发环境部署流程

1. 本地需按照 python 3.8.10 x64
2. 在本地某目录下创建虚拟环境：
```
python -m venv myvenv
myvenv\Scripts\Activate.ps1
```
3. 在虚拟环境中，pip安装p2t：
```
pip install pix2text
```
4. 将`onnxruntime`降级为`1.14.0`，以便支持win7：
```
pip uninstall onnxruntime
pip install onnxruntime==1.14.0
```
5. 虚拟环境中，尝试运行一遍p2t。第一次运行时会自动下载模型库。
6. 搜索出所有模型库文件，拷贝出来，组成一个models文件夹：
```
models
├─ cnocr
│    └─ 2.2
│           ├─ densenet_lite_136-fc
│           │    ├─ cnocr-v2.2-densenet_lite_136-fc-epoch=039-complete_match_epoch=0.8597-model.onnx
│           │    └─ label_cn.txt
│           └─ ppocr
│                  ├─ en_PP-OCRv3_rec_infer.onnx
│                  └─ en_dict.txt
├─ cnstd
│    └─ 1.2
│           ├─ Users
│           │    └─ king
│           │           └─ .cnstd
│           │                  └─ 1.2
│           │                         └─ analysis
│           │                                └─ mfd-yolov7_tiny.pt
│           ├─ analysis
│           │    └─ mfd-yolov7_tiny.pt
│           └─ ppocr
│                  ├─ ch_PP-OCRv3_det_infer.onnx
│                  └─ en_PP-OCRv3_det_infer.onnx
├─ pix2text
│    ├─ clf
│    │    └─ pix2text-v0.2-mobilenet_v2-epoch=015-val-accuracy-epoch=0.9394-model.ckpt
│    └─ formula
│           ├─ image_resizer.pth
│           └─ weights.pth
└─ torch
       └─ hub
              └─ checkpoints
                     └─ mobilenet_v2-7ebf99e0.pth
```
7. 将models文件夹放置到P2T插件目录下
8. 拷贝虚拟环境的包目录：`myvenv/Lib/site-packages`到P2T插件目录下。