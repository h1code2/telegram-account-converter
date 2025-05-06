#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/6 14:38
# @Author  : h1code2
# @File    : main.py
# @Software: PyCharm

import tkinter as tk
from gui import ZipBase64ConverterGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = ZipBase64ConverterGUI(root)
    root.mainloop()
