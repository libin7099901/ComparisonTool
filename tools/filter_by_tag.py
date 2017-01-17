# -*- coding:utf-8 -*-
'''
依据tag值处理某一目录下的所有文件, 存在的tag值将被保留,不存在的将被清除, 文件名不变
支持以":","：","\t"分割的key-value对文件
保存为以冒号分格的键值对
'''
import os


bizcard_wt_map = {
    "姓名":"name",
    "职务/部门":"title",
    "手机":"tel_cell",
    "公司":"org",
    "地址":"adr",
    "电话":"tel",
    "传真":"fax",
    "电子邮箱":"email",
    "网址":"url",
    "邮编":"postalcode",
}

bizcard_hw_map = {
    "姓名":"name",
    "头衔":"title",
    "手机":"tel_cell",
    "分机号":"tel_extension",
    "电话":"tel",
    "学历":"education",
    "部门":"department",
    "公司":"org",
    "网址":"url",
    "邮编":"postalcode",
    "地址":"adr",
    "传真":"fax",
    "邮箱":"email"
}

bizcard_ym_map = {
    "姓名":"name",
    "单位":"org",
    "职位":"title",
    "手机":"tel_cell",
    "办公室电话":"tel",
    "办公室电话1":"tel",
    "电子邮件":"email",
    "传真":"fax",
    "网址":"url",
    "地址":"adr",
    "即时通讯":"impp",
    "备注":"memo",
    "直拨电话":"tel",
}

bizcard_hh_map = {
    "姓名":"name",
    "所在地":"adr",
    "公司1":"org",
    "公司2":"org",
    "公司（其他）":"org",
    "部门1":"department",
    "部门2":"department",
    "部门（其他）":"department",
    "职位1":"title",
    "职位2":"title",
    "职位（其他）":"title",
    "手机1":"tel_cell",
    "手机2":"tel_cell",
    "手机（其他）":"tel_cell",
    "电话1":"tel",
    "电话2":"tel",
    "电话（其他）":"tel",
    "传真1":"fax",
    "传真2":"fax",
    "传真（其他）":"fax",
    "邮箱1":"email",
    "邮箱2":"email",
    "邮箱（其他）":"email",
    "邮政编码1":"postalcode",
    "邮政编码2":"postalcode",
    "地址":"adr",
    "地址（其他）":"adr",
    "公司主页":"url"
}

idcard_qianfajiguanye_tag = ["签发机关"]

vat_ym_not_include_tag = ["密码区", "税率"]

item_names = set()

def do_filter(source_path, target_path, tags, is_include=True):
    '''
    依据tag分割文件
    :param source_path:源目录
    :param target_path:目标目录
    :param tags:tag
    :param is_include:True包含这些tag,Flase:不包含这些tag
    :return:None
    '''
    for file in os.listdir(source_path):
        content = []
        with open(os.path.join(source_path, file), "r") as source_file:
            for line in source_file:
                item = {}
                tag = line.find("\t")
                tag_size=1
                if tag < 0:
                    tag = line.find(":")
                    if tag < 0:
                        tag = line.find("：")
                        tag_size = 2

                key = line[:tag]
                value = line[tag + tag_size:].replace("\n", "")

                if is_include:
                    if key in tags:
                        item_names.add(key)
                        item[key] = value
                        content.append(item)
                else:
                    if key not in tags:
                        item_names.add(key)
                        item[key] = value
                        content.append(item)

        with open(os.path.join(target_path, file), "w") as target_file:
            for item in content:
                for key in item:
                    target_file.write(key + ":" + item[key] + "\n")


if __name__ == "__main__":
    source_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\PhotographVersion\BankCard\stand"
    target_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\PhotographVersion\BankCard\stand_only_validdate"
    # filter_tags = bizcard_hh_map.values()
    # print set(filter_tags)
    do_filter(source_path, target_path, ["validdate"], is_include=True)
    print item_names