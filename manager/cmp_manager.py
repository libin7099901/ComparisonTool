# -*- coding:utf-8 -*-

import os
import sys
import json
from comparer import comparer
import ConfigParser


def read_config(config_path):
    '''
    从配置文件中读取配置
    :param config_path:配置文件路径
    :return:config_dict
    '''
    config_reader = ConfigParser.ConfigParser()
    config_dict = {}

    config_res = config_reader.read(config_path)
    if len(config_res) < 1:
        print 'Need config file ' + config_path
        sys.exit(-1)

    config_dict["left_path"] = config_reader.get("CompareConfig", "left_path")
    config_dict["right_path"] = config_reader.get("CompareConfig", "right_path")
    config_dict["recursion_compare"] = config_reader.getboolean("CompareConfig", "recursion_compare")
    config_dict["result_file_path"] = config_reader.get("CompareConfig", "result_file_path")
    config_dict["standard_path"] = config_reader.get("CompareConfig", "standard_path")
    config_dict["not_skip_different_file"] = config_reader.getboolean("CompareConfig", "not_skip_different_file")
    config_dict["need_csv_file"] = config_reader.getboolean("CompareConfig", "need_csv_file")
    config_dict["need_result_file"] = config_reader.getboolean("CompareConfig", "need_result_file")

    return config_dict


def get_file_list(path, check_subfolders=False, depth=0):
    '''
    扫描目录, 获取一棵文件树
    :param path: 带扫描路径
    :param check_subfolders: 是否递归扫描
    :param depth: 路径深度
    :return: 文件树
    '''
    # type: (str, bool, int) -> dict()
    file_tree = {}
    file_tree["path"] = path
    file_tree["file_list"] = []
    file_tree["sub_dirs"] = {}
    file_tree["depth"] = depth

    for sub_path in os.listdir(path):
        sub_path = sub_path.decode(sys.getdefaultencoding()).encode("utf-8")
        if os.path.isdir(path + "\\" + sub_path):
            file_tree["sub_dirs"][sub_path] = None
        else:
            file_tree["file_list"].append(sub_path)

    if check_subfolders:
        for sub_dir in file_tree["sub_dirs"]:
            file_tree["sub_dirs"][sub_dir] = get_file_list(path + "\\" + sub_dir, check_subfolders=True,
                                                           depth=depth + 1)

    return file_tree


def compare(config):
    '''
    比对正确率
    :param config:比对配置
    :return: 比对的详细结果, 比对的统计结果
    '''

    compare_result = {}
    # 临时放在这里
    compare = comparer.Compare()
    # TODO: 比对两个路径是否为同一类型(目录/目录)(文件/文件)

    # 当两侧都为目录时
    if os.path.isdir(config["left_path"]) and os.path.isdir(config["right_path"]):
        # TODO: 完成递归调扫目录的实现,方式还未确定
        left_file_tree = get_file_list(config["left_path"], check_subfolders=config["recursion_compare"])
        right_file_tree = get_file_list(config["right_path"], check_subfolders=config["recursion_compare"])

        if config["standard_path"] == "left_path":
            compare = comparer.PathCompare(left_file_tree, right_file_tree, not_skip_different_file=config["not_skip_different_file"])
        else:
            compare = comparer.PathCompare(right_file_tree, left_file_tree, not_skip_different_file=config["not_skip_different_file"])

    return compare.get_compare_result(), compare.get_statistical_result()


    # print json.dumps(right_file_tree, ensure_ascii=False, indent=4)


def write_result(file_path, detail, statistical):
    '''
    将比对的详细结果及统计结果写入结果文件
    :param file_path: 结果文件路径
    :param detail: 比对详情
    :param statistical: 比对统计结果
    :return: None
    '''
    print file_path
    with open(file_path, "w") as result_file:
        result_file.write(json.dumps(statistical, ensure_ascii=False))
        result_file.write("\n--------------------------------\n")
        result_file.write(json.dumps(detail,ensure_ascii=False,indent=4))

def write_result_to_csv_file(file_path, detail):
    '''
    将比对的详细结果中每个文件的统计结果写入csv文件
    :param file_path: 结果文件路径(任意格式)
    :param detail: 比对详情
    :return: None
    '''
    file_name_source = os.path.basename(file_path)
    file_name_csv = file_name_source[:file_name_source.find(".")] + ".csv"
    file_path = file_path.replace(file_name_source, file_name_csv)
    print file_path

    with open(file_path, "w") as csv_file:
        csv_file.write("file_name, item, word\n")
        for per_file in detail["SubCompareResult"].keys():
            file_dict = detail["SubCompareResult"][per_file]

            item_total_count = 0
            item_same_count = 0
            word_total_count = 0
            word_same_count = 0

            for item in file_dict["SubCompareResult"].keys():
                item_dict = file_dict["SubCompareResult"][item]
                item_total_count += item_dict["TotalCount"]
                item_same_count += item_dict["SameCount"]
                word_total_count += item_dict["SubCompareResult"]["WordCompareResult"]["TotalCount"]
                word_same_count += item_dict["SubCompareResult"]["WordCompareResult"]["SameCount"]

            if item_total_count == 0:
                item_proportion = "0.00"
            else:
                item_proportion = "%.2f%%" % (float(item_same_count) / float(item_total_count) * 100)
            if word_total_count == 0:
                word_proportion = "0.00"
            else:
                word_proportion = "%.2f%%" % (float(word_same_count) / float(word_total_count) * 100)

            csv_file.write(per_file + "," + item_proportion + "," + word_proportion + "\n")

if __name__ == "__main__":
    # 读取配置文件
    config = read_config("comparer.conf")

    # 获取比对结果
    result_detail, result_statistical = compare(config)

    # 将详细结果和统计结果写入结果文件
    if config["need_result_file"]:
        write_result(config["result_file_path"], result_detail, result_statistical)

    # 将每个文件的统计结果写入csv文件
    if config["need_csv_file"]:
        write_result_to_csv_file(config["result_file_path"], result_detail)

    # 打印结果
    print result_statistical
    # print json.dumps(result_detail, ensure_ascii=False)