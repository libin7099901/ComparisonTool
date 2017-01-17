# -*- coding=utf-8 -*-
'''
改变文件的标签名
支持以":","：","\t"分割的key-value对文件
保存为以冒号分格的键值对
'''

import os

idcard_ym_map = {
    "Name": "姓名",
    "CardNo.": "身份号码",
    "Sex": "性别",
    "Birthday": "出生",
    "Address": "住址",
    "Folk": "民族",
    "ValidPeriod": "有效期限",
    "IssueAuthority": "签发机关"
}

idcard_wt_map = {
    "姓名": "姓名",
    "公民身份号码": "身份号码",
    "性别": "性别",
    "出生": "出生",
    "住址": "住址",
    "民族": "民族",
    "有效期限": "有效期限",
    "签发机关": "签发机关"
}

bizcard_wt_map = {
    "姓名": "name",
    "职务/部门": "title",
    "手机": "tel_cell",
    "公司": "org",
    "地址": "adr",
    "电话": "tel",
    "传真": "fax",
    "电子邮箱": "email",
    "网址": "url",
    "邮编": "postalcode",
}

bizcard_hw_map = {
    "姓名": "name",
    "头衔": "title",
    "手机": "tel_cell",
    "分机号": "tel_extension",
    "电话": "tel",
    "学历": "education",
    "部门": "department",
    "公司": "org",
    "网址": "url",
    "邮编": "postalcode",
    "地址": "adr",
    "传真": "fax",
    "邮箱": "email"
}

bizcard_ym_map = {
    "姓名": "name",
    "单位": "org",
    "职位": "title",
    "手机": "tel_cell",
    "办公室电话": "tel",
    "办公室电话1": "tel",
    "电子邮件": "email",
    "传真": "fax",
    "网址": "url",
    "地址": "adr",
    "即时通讯": "impp",
    "备注": "memo",
    "直拨电话": "tel",
}

bizcard_hh_map = {
    "姓名": "name",
    "所在地": "adr",
    "公司1": "org",
    "公司2": "org",
    "公司（其他）": "org",
    "部门1": "department",
    "部门2": "department",
    "部门（其他）": "department",
    "职位1": "title",
    "职位2": "title",
    "职位（其他）": "title",
    "手机1": "tel_cell",
    "手机2": "tel_cell",
    "手机（其他）": "tel_cell",
    "电话1": "tel",
    "电话2": "tel",
    "电话（其他）": "tel",
    "传真1": "fax",
    "传真2": "fax",
    "传真（其他）": "fax",
    "邮箱1": "email",
    "邮箱2": "email",
    "邮箱（其他）": "email",
    "邮政编码1": "postalcode",
    "邮政编码2": "postalcode",
    "地址": "adr",
    "地址（其他）": "adr",
    "公司主页": "url",
    "昵称": "name",
    "tal_cell": "tel_cell"
}

vat_ym_map = {
    "票号1": "序号",
    "票号2": "编号",
    "开票日期": "日期",
    "购买方名称": "购货单位名称",
    "购买方纳税人识别号": "购货单位纳税人识别号",
    "购买方开户行及账号": "购货单位开户行及帐号",
    "合计（金额）": "金额",
    "合计（税额）": "税额",
    "价税合计（小写）": "总额",
    "销售方名称": "销货单位名称",
    "销售方纳税人识别号": "销货单位纳税人识别号",
    "销售方开户行及账号": "销货单位开户行及帐号"
}

stand_change_map = {
    "emall": "email"
}

bankcard_wt_map = {
    "卡号": "cardnumber",
    "银行卡类型": "cardtype",
    "银行卡名称": "cardnum",
    "银行名称": "bankname",
    "银行编号": ""
}


def change_tag(file_path, map):
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

            if key in map.keys():
                if value.count("-") == 2 and "公民身份号码" in map.keys():
                    value = value.replace("-", "年", 1)
                    value = value.replace("-", "月", 1)
                    value += "日"
                contents.append({map[key]: value})
            else:
                contents.append({key: value})

    with open(file_path, "w") as file:
        for content in contents:
            for key in content.keys():
                if key != "":
                    file.write(key + ":" + content[key] + "\n")


if __name__ == "__main__":
    path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\PhotographVersion\BankCard\WT"
    for file in os.listdir(path):
        change_tag(os.path.join(path, file), bankcard_wt_map)
