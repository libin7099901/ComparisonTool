# -*- coding:utf-8 -*-
'''
将JT OCE XML格式的识别结果转换为key:value对样式的识别结果
'''

import os
import xml.etree.ElementTree as ETree

def formatting(source_file_path, target_path, type="bizcard"):
    '''
    将源文件转换为目标目录下的同名文件,可指定转换格式
    :param source_file_path:
    :param target_path:
    :param type:
    :return:
    '''
    filename = os.path.basename(source_file_path)
    print filename

    if type!="idcard":
        with open(source_file_path, "r") as source_file:
            xml_string = source_file.read()
            if len(xml_string) <= 0:
                print source_file_path + " is empty "

        result = ""
        try:
            key_attrib = "item"
            res_attrib = "text"
            if type=="bizcard":
                root_node = ETree.fromstring(xml_string)
            elif type=="vat":
                root_node = ETree.fromstring(xml_string)
                root_node = root_node.find("form").find("page")
                key_attrib = "name"
                res_attrib = "result"
            else:
                raise TypeError("type must be one of bizcard,vat,idcard")

            for cell_node in root_node.findall("cell"):
                try:  # try to get result cell
                    cell_node_child = cell_node.getchildren()[0]
                    result += cell_node.attrib[key_attrib] + ':' + cell_node_child.attrib[res_attrib] + '\n'
                except:  # if not have result cell
                    result += cell_node.attrib[key_attrib] + ':\n'
        except Exception as ex:
            print source_file_path + " is invalid xml file, ex : " + str(ex)

        with open(os.path.join(target_path, filename), "w") as target_file:
            target_file.write(result.encode("utf-8"))

    elif type=="idcard":
        with open(source_file_path, "r") as source_file:
            write_verify_result(os.path.join(target_path, filename), source_file.read())

def write_verify_result(filepath, str_result):
    '''
    将IDCard的返回结果转换为身份证实际使用的标签名, 便于比较
    :param filepath:结果文件路径
    :param str_result:xml字符串
    :return:None
    '''
    verify_result = ""
    check_fields = ["姓名", "性别", "民族", "出生日期", "地址", "身份证号码", "签发机关", "有效期限"]
    birthday_fields = ["年", "月", "日"]
    map_fields = {"姓名": "姓名", "性别": "性别", "民族": "民族", "出生日期": "出生", "地址": "住址", "身份证号码": "身份号码", "签发机关": "签发机关",
                  "有效期限": "有效期限"}
    result = {}
    try:
        xml_result = ETree.fromstring(str_result)
        page = xml_result.find("form").find("page")
        for cell in page.findall("cell"):
            try:
                name = cell.get("name").encode("utf-8")
                if name in check_fields:
                    result[name] = cell.find("result").get("result").encode("utf-8")
                if name == "出生日期":
                    birthday_dict = {}
                    for birthday_cell in cell.findall("cell"):
                        birthday_dict[birthday_cell.get("name").encode("utf-8")] = birthday_cell.find("result").get(
                            "result").encode("utf-8")
                    result[name] = ""
                    for field in birthday_fields:
                        result[name] += birthday_dict[field] + field
            except Exception, ex:
                print ex
        for check_field in check_fields:
            try:
                verify_result += map_fields[check_field] + ":" + result[check_field] + "\r\n"
            except:
                #                 verify_result += map_fields[check_field] + "：null\r\n"
                pass
    except Exception, ex:
        print ex
        print "change xml failed"
        for check_field in check_fields:
            verify_result += map_fields[check_field] + "：null\r\n"

    with open(filepath, "wb") as result_file:
        for line in verify_result:
            result_file.write(line)


if __name__ == "__main__":
    source_path=r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\ScanVersion\VAT\JT_engine_result_r8928_add_entry"
    target_path=source_path

    for file in os.listdir(source_path):
        formatting(os.path.join(source_path,file), target_path, type="vat")