# -*- coding:utf-8 -*-

import os

if __name__ == "__main__":
    source_dir_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\PhotographVersion\BankCard\JT_engine_8062"
    target_dir_path = source_dir_path
    strA = "(null)"
    strB = ""

    for file in os.listdir(source_dir_path):
        data = ""
        with open(os.path.join(source_dir_path, file)) as source_file:
            data = source_file.read()

        with open(os.path.join(target_dir_path, file), "w") as target_file:
            target_file.write(data.replace(strA, strB))