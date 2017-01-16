# -*- coding:utf-8 -*-
'''
切分以坐标分割的, 汉王的OCR名片识别结果
切分逗号分隔的同一类型的多个值,转换为多行
将结果按key:value保存
'''
import os
import re
import json

coordinate_pattern = r"(,\d{1,4}){4}"

ym_split_list = ["姓名", "单位", "职位", "手机", "传真", "办公室电话", "电子邮件"]
hh_split_list = ["地址(其他)"]


def change_format(file_path):
    content = []
    with open(file_path, "r") as source_file:
        for line in source_file.readlines():
            item = {}
            tag = line.find("\t")
            tag_size = 1
            if tag < 0:
                tag = line.find(":")
                if tag < 0:
                    tag = line.find("：")
                    tag_size = 2
                    if tag < 0:
                        tag_size = 0

            key = line[:tag]
            item[key] = []
            values = line[tag + tag_size:].replace("\n", "")

            matchObj = re.search(coordinate_pattern, values)
            while matchObj:
                coordinate = matchObj.group()
                tag_at = values.find(coordinate)
                value = values[:tag_at]
                item[key].append(value)
                values = values[tag_at + len(coordinate):].replace(",", "", 1)
                matchObj = re.search(coordinate_pattern, values)

            if len(values) > 0:
                if key in hh_split_list:
                    tag = values.find(",")
                    while tag > 0:
                        isLtd = False
                        try:
                            isLtd = values[tag + 1:tag + 4] == "Ltd"
                        except:
                            pass
                        if values[tag - 1] == "." or isLtd:
                            print "all: " + values
                            after = values[tag + 1:]
                            temp_tag = after.find(",")
                            temp_values = values
                            if temp_tag > 0:
                                value = temp_values[:temp_tag + tag + 1]
                                item[key].append(value)
                                values = after[temp_tag + 1:]
                                tag = values.find(",")
                                continue
                            else:
                                break
                        value = values[:tag]
                        values = values[tag + 1:]
                        tag = values.find(",")
                        item[key].append(value)
                item[key].append(values)

            content.append(item)
    # print json.dumps(content, ensure_ascii=False, indent=4)
    with open(file_path, "w") as result_file:
        for item in content:
            for key in item.keys():
                for value in item[key]:
                    result_file.write(key + ":" + value + "\n")

                    # print json.dumps(content, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\ScanVersion\BizCard\HH/"
    # path = "../TestData/Test/"
    for file in os.listdir(path):
        change_format(path + file)
