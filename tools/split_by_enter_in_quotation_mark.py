# -*- coding:utf-8 -*-
'''
将在引号内的多行文本, 按行补齐标签并去除引号
'''
import os


def change_format(file_path):
    '''
    将单个文件内的引号内的多行文本,按行补齐标签并去除引号,保存到原文件中
    :param file_path:文件路径
    :return:None
    '''
    with open(file_path, "r") as source_file:
        source = source_file.read()

    tag_count = source.count("\"")
    back = source

    result = ""
    for i in range(tag_count / 2):

        tag = back.find("\"")
        front = back[:tag]
        result += front

        label = front[front.rfind("\n") + 1:].replace("\t", "")

        back = back[tag + 1:]

        tag = back.find("\"")
        content = back[:tag]
        back = back[tag + 1:]

        i = 0
        for value in content.split("\n"):
            if i > 0:
                result += "\n" + label + "\t" + value
            else:
                result += value
            i += 1

    result += back

    with open(file_path, "w") as result_file:
        # 因合合的识别结果中外部链接内还有其他标签, 无法统计, 去掉前置标签
        result_file.write(result.replace("外部链接\t", ""))

            # print "back:" + back


if __name__ == "__main__":
    path = "D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\ScanVersion\BizCard\HH/"
    for file in os.listdir(path):
        change_format(path + file)
