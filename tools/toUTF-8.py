#-*- coding=utf-8 -*-
"""
该工具用于根据一个标注了文件格式的列表, 将不同格式的文本文件转换为UTF-8格式
可以使用Linux下的file工具获取文件编码列表
"""

import sys
import os

def change(path, file):
    '''
    依据文件编码表, 使用不同方法转换各种格式的文件到UTF-8格式
    :param path:
    :param file:
    :return:
    '''
    if file["format"].find("UTF-8 Unicode text") >= 0:
        return
    elif file["format"].find("ISO-8859 text") >= 0:
        content = ""
        with open(os.path.join(path,file["file"]), "r") as source_file:
            content = source_file.read()
        with open(os.path.join(path,file["file"]), "w") as result_file:
            result_file.write(content.decode("GBK").encode("utf-8"))
    else:
        removeBom(os.path.join(path,file["file"]))


def removeBom(file):
    '''
    移除文件中的Bom头,保存到原文件中
    :param file: 文件路径
    :return: None
    '''
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s == BOM else False

    f = open(file, 'rb')
    if existBom(f.read(3)):
        fbody = f.read()
        # f.close()
        with open(file, 'wb') as f:
            f.write(fbody)

def get_format_info_from_file(format_file):
    format = []
    with open(format_file,"r") as file_list:
        for file in file_list:
            tag = file.find(":")
            file_name = file[:tag]
            file_format = file[tag+1:].lstrip().replace("\n","")
            format.append({"file":file_name, "format":file_format})

    return format



if __name__ == "__main__":
    file_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\ScanVersion\VAT\stand"
    file_list = get_format_info_from_file("./file_format_list/file_list_vat")
    for file in file_list:
        # print file
        change(file_path, file)