# -*- coding:utf-8 -*-

import os
import shutil


def move_file_by_path(source_path, fliter_path, target_path):
    fliter_path_file_list = [fliter_file for fliter_file in os.listdir(fliter_path) ]  # if os.path.isfile(fliter_file)]
    print fliter_path_file_list

    for source_file in os.listdir(source_path):
        if source_file in fliter_path_file_list:
            shutil.copy(os.path.join(source_path, source_file), os.path.join(target_path, source_file))

if __name__ == "__main__":
    source_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\ScanVersion\VAT\JT_engine_result_r8928"
    fliter_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\ScanVersion\VAT\YM_result_11pic"
    target_path = r"D:\PythonWorkSpaces\OtherWorkSpaces\ComparisonTool\TestData\ScanVersion\VAT\JT_endine_result_r8928_11pic"

    move_file_by_path(source_path, fliter_path, target_path)