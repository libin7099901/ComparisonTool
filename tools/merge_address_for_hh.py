#-*- coding:utf-8 -*-
'''
合并合合名片识别结果中的地址信息
'''


import os
import json
import chardet

def change_format(file_path):
    content = []
    with open(file_path, "r") as source_file:
        address1= {"地址":[""]}
        address2= {"地址":[""]}
        for line in source_file.readlines():

            # print chardet.detect(line)
            # line = line
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
            value = line[tag + tag_size:].replace("\n", "")

            if key in ["省1", "城市1", "街道1"]:
                address1["地址"][0] += value
            elif key in ["省2", "城市2", "街道2"]:
                address2["地址"][0] += value
            else:
                item[key].append(value)
                content.append(item)

        content.append(address1)
        content.append(address2)

    # print json.dumps(content, ensure_ascii=False, indent=4)
    with open(file_path, "w") as result_file:
        for item in content:
            for key in item.keys():
                for value in item[key]:
                    result_file.write(key + "\t" + value + "\n")

    # print json.dumps(content, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    path = "D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\ScanVersion\BizCard\HH/"
    # path = "../TestData/Test/"
    for file in os.listdir(path):
        change_format(path+file)