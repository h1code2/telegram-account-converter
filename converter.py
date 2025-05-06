#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/6 14:38
# @Author  : h1code2
# @File    : converter.py
# @Software: PyCharm

import base64
from typing import Optional

def zip_to_base64(filepath: str) -> Optional[str]:
    """
    将zip文件转换为base64字符串。
    :param filepath: zip文件路径
    :return: base64字符串（转换失败返回None）
    """
    try:
        with open(filepath, 'rb') as file:
            zip_data = file.read()
            return base64.b64encode(zip_data).decode('utf-8')
    except Exception as e:
        print(f"转换失败：{e}")
        return None

def get_owner_id(filename: str) -> str:
    """
    从文件名提取owner_id
    :param filename: 文件路径或文件名
    :return: owner_id字符串
    """
    return filename.split("/")[-1].split(".")[0].split("_")[0]