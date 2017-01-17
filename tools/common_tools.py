# -*- coding:utf-8 -*-
import os
import json


def get_item_list(file_path):
    contents = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            tag = line.find("\t")
            tag_size = 1
            if tag < 0:
                tag = line.find(":")
                if tag < 0:
                    tag = line.find("：")
                    tag_size = 2
                    if tag < 0:
                        tag_size = 0

            key = line[:tag].rstrip().lstrip()
            value = line[tag + tag_size:].replace("\n", "").rstrip().lstrip()
            contents.append({key: value})

    return contents


def writh_item_list(file_path, contents):
    with open(file_path, "w") as file:
        for content in contents:
            for key in content.keys():
                if key != "":
                    file.write(key + ":" + content[key] + "\n")

if __name__ == "__main__":
    path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\Test"
    for file in os.listdir(path):
        print json.dumps(get_item_list(os.path.join(path, file)), ensure_ascii=False)