# -*- coding:utf-8 -*-
import formatting_from_xml
import os

def ocr_recognize(pic_file_path, result_path):
    pass

if __name__ == "__main__":
    pic_path = ""
    result_path = ""
    for file in os.listdir(pic_path):
        ocr_recognize(os.path.join(pic_path, file), result_path)
    formatting_from_xml.formatting(result_path, result_path)
