# -*- coding:utf-8 -*-
import common_tools
import os
import json


def add_bank_id(source_file_path, target_dir_path, bankid_map):
    file_name = os.path.basename(source_file_path)
    contents = common_tools.get_item_list(source_file_path)
    bank_name = ""
    for item in contents:
        for key in item.keys():
            if key in ["bankname"]:
                bank_name = item[key]
                break
            if key in ["bankid"]:
                try:
                    item[key] = bankid_map[bank_name]
                except KeyError:
                    try:
                        item[key] = bankid_map[bank_name.replace("中国", "")]
                    except:
                        print 'file: "' + file_name + '" add bank id Failed, bank name is "' + bank_name + '"'

    # print json.dumps(contents, ensure_ascii=False)

    common_tools.writh_item_list(os.path.join(target_dir_path, file_name), contents)

def get_bankid_map(resource_file_path):
    bank_id_dict = {}
    with open(resource_file_path, "r") as resource_file:
        for line in resource_file:
            line = line.replace("\r", "").replace("\n", "")
            (value, key) = line.split("\t")
            bank_id_dict[key] = value

    return bank_id_dict

if __name__== "__main__":
    source_dir_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\PhotographVersion\BankCard\stand"
    target_dir_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\PhotographVersion\BankCard\stand_add_bank_id"
    resource_file_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\tools\dat\bankidmap.txt"

    bankid_map = get_bankid_map(resource_file_path)

    for file in os.listdir(source_dir_path):
        add_bank_id(os.path.join(source_dir_path, file), target_dir_path, bankid_map)