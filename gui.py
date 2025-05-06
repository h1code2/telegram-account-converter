#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/6 14:38
# @Author  : h1code2
# @File    : gui.py
# @Software: PyCharm

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from converter import zip_to_base64, get_owner_id


class ModernStyle:
    """现代UI样式配置"""

    def __init__(self):
        self.primary_color = "#2E8B57"
        self.secondary_color = "#4682B4"
        self.bg_color = "#F5F5F5"
        self.text_color = "#333333"
        self.font_family = "Helvetica Neue"

    def apply_style(self, root):
        style = ttk.Style()

        # 配置主题
        style.theme_use('clam')

        # 全局样式配置
        style.configure(".",
                        font=(self.font_family, 12),
                        background=self.bg_color,
                        foreground=self.text_color)

        # 按钮样式
        style.configure("Primary.TButton",
                        padding=10,
                        relief="flat",
                        background=self.primary_color,
                        foreground="white",
                        font=(self.font_family, 11, "bold"))

        style.map("Primary.TButton",
                  background=[('active', '#1C563D')])

        style.configure("Secondary.TButton",
                        padding=10,
                        relief="flat",
                        background=self.secondary_color,
                        foreground="white",
                        font=(self.font_family, 11))

        style.map("Secondary.TButton",
                  background=[('active', '#3370A1')])

        # 文件路径显示样式
        style.configure("Path.TLabel",
                        padding=8,
                        relief="groove",
                        background="white",
                        borderwidth=1,
                        width=50,
                        wraplength=400)

        # 配置根窗口背景
        root.configure(bg=self.bg_color)


class ZipBase64ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ZIP转Base64转换器")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)

        # 应用现代样式
        self.style = ModernStyle()
        self.style.apply_style(root)

        # 初始化变量
        self.current_path = tk.StringVar(value="未选择文件")

        # 创建界面元素
        self.create_widgets()

    def create_widgets(self):
        # 主容器
        main_container = ttk.Frame(self.root, padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 文件选择区域
        file_frame = ttk.LabelFrame(main_container, text="文件选择", padding=15)
        file_frame.pack(fill=tk.X, pady=(0, 15))

        # 文件路径显示
        self.file_label = ttk.Label(
            file_frame,
            textvariable=self.current_path,
            style="Path.TLabel",
            anchor="w"
        )
        self.file_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 选择文件按钮
        self.select_btn = ttk.Button(
            file_frame,
            text="选择文件",
            style="Primary.TButton",
            command=self.select_file,
            width=12
        )
        self.select_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # 信息显示区域
        info_frame = ttk.Frame(main_container, padding=15)
        info_frame.pack(fill=tk.X, pady=(0, 15))

        # Owner ID显示
        owner_frame = ttk.Frame(info_frame)
        owner_frame.pack(side=tk.LEFT)

        ttk.Label(owner_frame, text="Owner ID:", font=(self.style.font_family, 11, "bold")).pack(anchor="w")
        self.owner_value = ttk.Label(owner_frame, text="", font=(self.style.font_family, 11), width=30)
        self.owner_value.pack(anchor="w")

        # 文件信息显示
        self.file_info = ttk.Label(info_frame, text="", width=35, font=(self.style.font_family, 11))
        self.file_info.pack(side=tk.RIGHT, anchor="e")

        # Base64输出区域
        result_frame = ttk.LabelFrame(main_container, text="Base64输出", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # 结果文本框
        self.result_text = tk.Text(
            result_frame,
            height=12,
            width=60,
            wrap=tk.WORD,
            font=(self.style.font_family, 11),
            bg="#FFFFFF",
            bd=1,
            relief="solid"
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 滚动条
        scroll = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=scroll.set)

        # 操作按钮区域
        btn_frame = ttk.Frame(main_container)
        btn_frame.pack(fill=tk.X)

        self.convert_btn = ttk.Button(
            btn_frame,
            text="转换",
            style="Primary.TButton",
            command=self.convert_file,
            width=10
        )
        self.convert_btn.pack(side=tk.LEFT, padx=5)

        self.copy_btn = ttk.Button(
            btn_frame,
            text="复制结果",
            style="Secondary.TButton",
            command=self.copy_result,
            width=10
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(
            btn_frame,
            text="清空",
            style="Secondary.TButton",
            command=self.clear_all,
            width=10
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # 版权信息
        ttk.Label(main_container, text="© 2025 h1code2", font=(self.style.font_family, 9), foreground="#888").pack(
            pady=5)

    def select_file(self):
        """选择ZIP文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")]
        )
        if file_path:
            self.current_path.set(file_path)
            self.owner_value.config(text=get_owner_id(file_path))

            # 显示文件信息
            file_size = os.path.getsize(file_path)
            self.file_info.config(
                text=f"文件大小：{file_size / 1024:.2f} KB | 修改时间：{os.path.getmtime(file_path):.0f}"
            )

            self.result_text.delete(1.0, tk.END)

    def convert_file(self):
        """执行转换"""
        file_path = self.current_path.get()
        if file_path == "未选择文件":
            messagebox.showwarning("警告", "请先选择ZIP文件！", parent=self.root)
            return

        try:
            result = zip_to_base64(file_path)
            if result:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result)
                messagebox.showinfo("成功", "转换完成！", parent=self.root)
            else:
                raise Exception("转换失败")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{str(e)}\n请检查文件格式是否正确", parent=self.root)

    def copy_result(self):
        """复制结果到剪贴板"""
        result = self.result_text.get(1.0, tk.END)
        if result.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("提示", "已复制到剪贴板！", parent=self.root)
        else:
            messagebox.showwarning("警告", "没有可复制的内容", parent=self.root)

    def clear_all(self):
        """清空所有内容"""
        self.current_path.set("未选择文件")
        self.owner_value.config(text="")
        self.file_info.config(text="")
        self.result_text.delete(1.0, tk.END)