# demo: 阿巴阿巴OCR


class Api:  # 接口
    def __init__(self, globalArgd):
        self.lang = ""  # 当前语言
        api_key = globalArgd["api_key"]
        print("阿巴阿巴OCR获取 api_key： ", api_key)

    # 启动引擎。返回： "" 成功，"[Error] xxx" 失败
    def start(self, argd):
        self.lang = argd["language"]
        print("阿巴阿巴OCR当前语言： ", self.lang)
        return ""

    def stop(self):  # 停止引擎
        pass

    def runPath(self, imgPath: str):  # 路径识图
        res = self._ocr()
        return res

    def runBytes(self, imageBytes):  # 字节流
        res = self._ocr()
        return res

    def runBase64(self, imageBase64):  # base64字符串
        res = self._ocr()
        return res

    def _ocr(self):
        flag = True
        text = ""
        if self.lang == "zh_CN":
            text = "阿巴阿巴阿巴"
        elif self.lang == "zh_TW":
            text = "阿巴阿巴阿巴"
        elif self.lang == "en_US":
            text = "Aba Aba Aba"
        elif self.lang == "ja_JP":
            text = "あばあばあば"
        else:
            flag = False
            text = f"[Error] 未知的语言：{self.lang}"
        if flag:
            res = {
                "code": 100,
                "data": [
                    {
                        "text": text,
                        "box": [[0, 0], [200, 0], [200, 40], [0, 40]],
                        "score": 1,
                    }
                ],
            }
        else:
            res = {"code": 102, "data": text}
        return res
