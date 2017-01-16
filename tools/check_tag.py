#-*- coding:utf-8 -*-

import os

vat_tag = ["加密版本"]

def check_tag(file_path, tags):
    file_list = []
    with open(file_path) as file:
        content = file.read()
        for tag in tags:
            if content.find(tag) > 0:
                file_list.append(file_path)
                print file_path
                break

    return file_list

if __name__ == "__main__":
    dir_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\ScanVersion\VAT\stand"
    for file_path in os.listdir(dir_path):
        check_tag(os.path.join(dir_path, file_path), vat_tag)