# -*- coding:utf-8 -*-

import os
import copy
import json
from verify_new22 import stringdiffanalysis

temp_file_name = "./~compaer_tools_null_file.tmp"


class Compare(object):
    """
    比对类
    """

    def __init__(self, is_atom=False):
        """
        Init
        :param is_atom:是否为原子级比对, 如果为是将不进行更低级别的比对
        """
        self._is_atom = is_atom
        self._same = True
        self._same_part = []
        self._same_count = 0
        self._different_part = []
        self._different_count = 0
        self._total_count = 0
        self._compare_result = {}
        self._left_only = []
        self._right_only = []
        self._sub_compare_result = {}

        # 待定
        self._type = "CompareAbstract"
        self._sub_type = "None"

    def get_compare_result(self):
        """
        获取比对结果
        :return: 将比对结果拼装为Json返回
        """
        # 拼装结果
        self._compare_result["Type"] = self._type
        self._compare_result["SamePart"] = self._same_part
        self._compare_result["DifferentPart"] = self._different_part
        self._compare_result["LeftOnly"] = self._left_only
        self._compare_result["RightOnly"] = self._right_only

        if not self._is_atom:
            self._compare_result["SubType"] = self._sub_type
            self._compare_result["SubCompareResult"] = self._sub_compare_result

        self._compare_result["SameCount"] = self._same_count
        self._compare_result["DifferentCount"] = self._different_count
        self._compare_result["TotalCount"] = self._total_count
        self._compare_result["IsSame"] = self._same
        return self._compare_result

    def get_string_result(self, indent=0):
        """
        获取字符串格式的比对结果
        :param indent: 缩进深度
        :return: None
        """
        return json.dumps(self.get_compare_result(), ensure_ascii=False, indent=indent)

    def get_statistical_result(self):
        """
        获取统计结果
        :return: Json格式的统计结果
        """
        compare_result = self.get_compare_result()
        sub_type = compare_result["SubType"]
        statistical_result = {sub_type: {}}
        statistical_result[sub_type]["Total"] = compare_result["TotalCount"]
        statistical_result[sub_type]["Same"] = compare_result["SameCount"]
        if compare_result["TotalCount"] != 0:
            statistical_result[sub_type]["Proportion"] = "%.2f%%" % (float(compare_result["SameCount"]) /
                                                                    float(compare_result["TotalCount"]) * 100)
        else:
            statistical_result[sub_type]["Proportion"] = "%.2f%%" % 0

        # TODO: 实现多层级结果的统计,可以考虑将该方法转为静态方法?

        # TODO: 暂时的统计条目正确率的方法, 之后使用其他方法进行替换

        item_total_count = 0
        item_same_count = 0
        word_total_count = 0
        word_same_count = 0
        for sub_file in compare_result["SubCompareResult"]:
            for sub_file2 in compare_result["SubCompareResult"][sub_file]["SubCompareResult"]:
                item_total_count += compare_result["SubCompareResult"][sub_file]["SubCompareResult"][sub_file2][
                    "TotalCount"]
                item_same_count += compare_result["SubCompareResult"][sub_file]["SubCompareResult"][sub_file2][
                    "SameCount"]
                word_total_count += \
                compare_result["SubCompareResult"][sub_file]["SubCompareResult"][sub_file2]["SubCompareResult"][
                    "WordCompareResult"]["TotalCount"]
                word_same_count += \
                compare_result["SubCompareResult"][sub_file]["SubCompareResult"][sub_file2]["SubCompareResult"][
                    "WordCompareResult"]["SameCount"]

        statistical_result["Item"] = {}
        statistical_result["Item"]["Total"] = item_total_count
        statistical_result["Item"]["Same"] = item_same_count
        if item_total_count == 0:
            statistical_result["Item"]["Proportion"] = "0.00"
        else:
            statistical_result["Item"]["Proportion"] = "%.2f%%" % (
            float(item_same_count) / float(item_total_count) * 100)

        statistical_result["Word"] = {}
        statistical_result["Word"]["Total"] = word_total_count
        statistical_result["Word"]["Same"] = word_same_count
        if word_total_count == 0:
            statistical_result["Word"]["Proportion"] = "0.00"
        else:
            statistical_result["Word"]["Proportion"] = "%.2f%%" % (
            float(word_same_count) / float(word_total_count) * 100)

        return statistical_result


# TODO: 实现字比对
class WordCompare(Compare):
    """
    实现字符串的比对, 统计字正确率
    """

    def __init__(self, left_word, right_word):
        """
        Init
        :param left_word: 标准字符串
        :param right_word:  比对字符串
        """
        super(WordCompare, self).__init__(is_atom=True)

        self._type = "Word"
        self._sub_type = None

        # 将字符串转换Unicode格式再转换为list
        try:
            left_tokens = list(left_word.decode("utf-8"))
        except UnicodeDecodeError:
            left_tokens = list(left_word.decode("GBK"))
        self._total_count = len(left_tokens)
        try:
            right_tokens = list(right_word.decode("utf-8"))
        except UnicodeDecodeError:
            try:
                right_tokens = list(right_word.decode("GBK"))
            except UnicodeDecodeError:
                print right_word
                right_tokens = list(right_word.decode("GBK"))

        # 将list中的每个字符转换为UTF-8格式
        for i in range(len(left_tokens)):
            left_tokens[i] = left_tokens[i].encode("utf-8")
        for i in range(len(right_tokens)):
            right_tokens[i] = right_tokens[i].encode("utf-8")

        # 获取比对结果
        stringdiff = stringdiffanalysis(" ".join(left_tokens), " ".join(right_tokens))
        stringdiff.calclate_diff_lcs2()
        self._different_part = stringdiff._diffstring
        self._total_count = stringdiff._allcount
        self._same_count = stringdiff._samecount

        # 以下方法为简单粗暴的字统计结果
        # i = 0
        # while i < len(left_tokens):
        #     token = left_tokens[i]
        #     if token in right_tokens:
        #         self._same_count += 1
        #         # self._same_part.append(token)
        #         left_tokens.remove(token)
        #         right_tokens.remove(token)
        #     else:
        #         i += 1

        # for token in left_tokens:
        #     self._left_only.append(token)
        # for token in right_tokens:
        #     self._right_only.append(token)

        # 判断字符串是否相等
        if (len(self._left_only) + len(self._right_only)) > 0:
            self._same = False


class ItemCompare(Compare):
    def __init__(self, left_item, right_item):
        super(ItemCompare, self).__init__(is_atom=False)  # 暂时将item作为最底层的比对元素, 不考虑字正确率
        self._type = "Item"
        self._sub_type = "Word"
        self._total_count = len(left_item)

        for item in left_item:
            if item in right_item:
                self._same_part.append(item)
                self._same_count += 1
            else:
                self._different_part.append(item)
                self._different_count += 1
        self._same_part = list(set(self._same_part))

        if self._total_count == self._same_count:
            self._same = True
        else:
            self._same = False

        self._left_only = copy.deepcopy(left_item)
        self._right_only = copy.deepcopy(right_item)
        self._compare_result["LeftOnly"] = self._left_only
        self._compare_result["RightOnly"] = self._right_only

        for value in self._same_part:
            self._left_only.remove(value)
            self._right_only.remove(value)

        left_word = "".join(left_item)
        right_word = "".join(right_item)
        self._sub_compare_result["WordCompareResult"] = WordCompare(left_word, right_word).get_compare_result()


class FileCompare(Compare):
    def __init__(self, left_file_path, right_file_path):
        super(FileCompare, self).__init__()
        self._type = "File"
        self._sub_type = "Item"
        self._compare_result["ItemResult"] = {}

        left_items = self.get_items(left_file_path)
        self._total_count = len(left_items.keys())
        right_items = self.get_items(right_file_path)

        # TODO: 比对
        for key in left_items.keys():
            if key in right_items.keys():
                self._same_part.append(key)

        self._left_only = left_items.keys()
        self._right_only = right_items.keys()
        for key in self._same_part:
            self._left_only.remove(key)
            self._right_only.remove(key)

        # 获取每个条目的比对信息
        for key in left_items.keys():
            if key in self._same_part:
                compare_result = ItemCompare(left_items[key], right_items[key]).get_compare_result()
            else:
                compare_result = ItemCompare(left_items[key], []).get_compare_result()
            self._sub_compare_result[key] = compare_result
            if not compare_result["IsSame"]:
                self._different_part.append(key)
                self._different_count += 1
            else:
                self._same_count += 1
        # 这里可能有问题
        self._same_part = left_items.keys()
        for key in self._different_part:
            self._same_part.remove(key)
        if self._same_count != self._total_count:
            self._same = False

    @staticmethod
    def get_items(file_path):
        items = {}
        with open(file_path, "r") as source_file:
            for line in source_file.readlines():
                # line = line.decode("GBK").encode("utf-8")
                tag = line.find("\t")
                tag_size = 1
                if tag < 0:
                    tag = line.find(":")
                    if tag < 0:
                        tag = line.find("：")
                        tag_size = 2

                key = line[:tag]
                # 按照一定规则去除相应的元素
                if key in ["tel", "tel_cell", "fax"]:
                    value = line[tag + tag_size:].replace("\n", "").replace("-", "").replace(" ", "").replace("(", "").replace(
                        ")", "")
                elif key in ["有效期限"]:
                    value = line[tag + tag_size:].replace("\n", "").replace(".", "").replace(" ", "")
                else:
                    value = line[tag + tag_size:].replace("\n", "").replace(" ", "")

                if key not in items.keys():
                    items[key] = []
                items[key].append(value)

                # TODO: 将item读出写到字典中
        return items


class PathCompare(Compare):
    def __init__(self, left_file_tree, right_file_tree, not_skip_different_file=True):
        super(PathCompare, self).__init__()
        self._type = "Path"
        self._sub_type = "File"
        self._compare_result["FileCompareResult"] = {}

        # 准备临时文件
        if os.path.exists(temp_file_name):
            pass
        else:
            with open(temp_file_name, "w") as temp_file:
                temp_file.write("")

        # 获取两侧的文件列表
        left_file_list = left_file_tree["file_list"]
        right_file_list = right_file_tree["file_list"]

        # 找出在两个目录中相同的文件
        for left_file in left_file_list:
            if left_file in right_file_list:
                self._same_part.append(left_file)

        # 比对全部文件时以左侧目录计算比对数量
        if not_skip_different_file:
            self._total_count = len(left_file_list)
        else:  # 仅比对相同文件时以相同目录计算比对数量
            self._total_count = len(self._same_part)

        if not_skip_different_file:  # 当比对全部文件是统计两侧相同的文件
            # 深复制之后需要重新指定关系
            self._left_only = copy.deepcopy(left_file_list)
            self._right_only = copy.deepcopy(right_file_list)
            self._compare_result["LeftOnly"] = self._left_only
            self._compare_result["RightOnly"] = self._right_only

            # 找出两个目录独有的文件
            for same_file in self._same_part:
                self._left_only.remove(same_file)
                self._right_only.remove(same_file)

        if len(self._left_only + self._right_only) > 0:
            self._same = False

        # 获取每个文件的比对信息
        for each_file in left_file_list:
            if each_file in self._same_part:
                compare_result = FileCompare(left_file_tree["path"] + "\\" + each_file,
                                             right_file_tree["path"] + "\\" + each_file).get_compare_result()
            else:
                if not_skip_different_file:
                    compare_result = FileCompare(left_file_tree["path"] + "\\" + each_file,
                                                 temp_file_name).get_compare_result()
                else:
                    continue
            self._sub_compare_result[each_file] = compare_result
            if not compare_result["IsSame"]:
                self._same = False
                self._different_part.append(each_file)
                self._different_count += 1
            else:
                self._same_count += 1

        if not_skip_different_file:
            self._same_part = left_file_list
        for different_file in self._different_part:
            self._same_part.remove(different_file)

        # 删除临时文件
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
