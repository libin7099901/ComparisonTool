# -*- coding=utf-8 -*-
'''
该脚本用于根据文件大小或某文件列表,将一个目录中的文件分到两个目录中去
'''
import os
import shutil
from os.path import join, getsize


def getdirsize(dir):
    size = 0L
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])

    return size


def get_file_by_size(path, size, type="lt"):
    '''
    按照文件大小获取目录下的文件列表
    :param path:目录的路径
    :param size:文件的大小
    :param type:lt(little than)或gt(great than),大于或小于文件大小的值被保存到列表中
    :return:list格式的文件列表
    '''
    file_list = []
    for file in os.listdir(path):
        if type == "lt":
            if getsize(path + file) < size:
                file_list.append(file)
        elif type == "gt":
            if getsize(path + file) > size:
                file_list.append(file)
        else:
            raise Exception("type error, must be one of \"lt, bt\"")

    with open(path + "../file_list", "w") as list_file:
        for file in file_list:
            list_file.write(file + "\n")
    return file_list


def move_file(source_path, file_list, target_path, target_path_2):
    '''
    将源目录中,在文件列表内的文件转移到目标目录1, 不在文件列表内的文件转移到目标目录2
    :param source_path: 源目录
    :param file_list: 文件列表
    :param target_path: 目标目录1
    :param target_path_2: 目标目录2
    :return:
    '''
    for file in os.listdir(source_path):
        if file.lower() in file_list:
            if target_path != None:
                shutil.copy(source_path + file, target_path + file)
        else:
            if target_path_2 != None:
                shutil.copy(source_path + file, target_path_2 + file)


def get_file_list(path):
    file_list = []
    with open(path, "r") as list_file:
        for line in list_file.readlines():
            line = line.lower()
            file_list.append(line.replace("\n", ""))

    return file_list


if __name__ == "__main__":
    # 原目录
    path = "../TestData/ScanVersion/IDCard/pic/"
    # 目标目录1, 用于存放在filelist中的文件
    target_path = "../TestData/ScanVersion/IDCard/pic_back/"
    # 目标目录2, 用于存放不在filelist中的文件
    target_path_2 = "../TestData/ScanVersion/IDCard/pic_front/"

    # 按大小筛选出文件列表
    # file_list = get_file_by_size(path, 90)

    # 从文件中读取文件列表
    file_list = get_file_list("../TestData/ScanVersion/IDCard/file_list")

    # 将文件名中的.txt转换为.jpg,以转移原图
    for i,file_name in enumerate(file_list):
        file_name = file_name.replace(".txt", ".jpg")
        file_list[i] = file_name

    move_file(path, file_list, target_path, target_path_2)
