"""
PDF Compressor Parameter Extractor
用于从PDF文件中提取压缩机参数的Windows GUI应用
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
import json
import os
from datetime import datetime
from typing import Dict, Optional


class PDFExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 压缩机参数提取工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.setup_ui()

    def setup_ui(self):
        """设置GUI界面"""
        # 标题
        title_frame = tk.Frame(self.root, padx=10, pady=10)
        title_frame.pack(fill=tk.X)

        tk.Label(
            title_frame,
            text="PDF 压缩机参数提取工具",
            font=("Microsoft YaHei UI", 16, "bold")
        ).pack()

        # 文件选择区域
        file_frame = tk.Frame(self.root, padx=10, pady=5)
        file_frame.pack(fill=tk.X)

        self.file_label = tk.Label(file_frame, text="未选择文件", anchor=tk.W)
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.browse_button = tk.Button(
            file_frame,
            text="选择PDF文件",
            command=self.browse_file,
            width=15
        )
        self.browse_button.pack(side=tk.RIGHT)

        # 操作按钮
        button_frame = tk.Frame(self.root, padx=10, pady=5)
        button_frame.pack(fill=tk.X)

        self.extract_button = tk.Button(
            button_frame,
            text="提取参数",
            command=self.extract_parameters,
            width=15,
            state=tk.DISABLED
        )
        self.extract_button.pack(side=tk.LEFT, padx=(0, 5))

        self.save_button = tk.Button(
            button_frame,
            text="保存结果",
            command=self.save_results,
            width=15,
            state=tk.DISABLED
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_button = tk.Button(
            button_frame,
            text="清空",
            command=self.clear_all,
            width=15
        )
        self.clear_button.pack(side)

        # 结果显示区域
        result_frame = tk.Frame(self.root, padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(result_frame, text="提取结果:", font=("Microsoft YaHei UI", 12)).pack(anchor=tk.W)

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            height=20
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=10
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # 存储变量
        self.current_file = None
        self.extracted_data = None

    def browse_file(self):
        """浏览并选择PDF文件"""
        file_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )

        if file_path:
            self.current_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.extract_button.config(state=tk.NORMAL)
            self.status_var.set(f"已选择: {os.path.basename(file_path)}")

    def extract_parameters(self):
        """从PDF中提取参数"""
        if not self.current_file:
            messagebox.showwarning("警告", "请先选择PDF文件")
            return

        self.status_var.set("正在提取参数...")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "正在读取PDF文件...\n")
        self.root.update()

        try:
            # 提取PDF文本
            pdf_text = self.extract_pdf_text(self.current_file)

            # 显示提取的文本（调试用）
            self.result_text.insert(tk.END, "\n=== PDF文本内容 ===\n")
            self.result_text.insert(tk.END, pdf_text[:5000] + "...\n" if len(pdf_text) > 5000 else pdf_text + "\n")
            self.root.update()

            # 提取参数
            self.extracted_data = self.parse_parameters(pdf_text)

            # 显示提取结果
            self.display_results(self.extracted_data)
            self.save_button.config(state=tk.NORMAL)
            self.status_var.set("参数提取完成")

        except Exception as e:
            messagebox.showerror("错误", f"提取失败: {str(e)}")
            self.status_var.set("提取失败")

    def extract_pdf_text(self, file_path: str) -> str:
        """从PDF文件中提取文本"""
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            # 尝试使用 PyPDF2
            try:
                import PyPDF2
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                raise Exception(
                    "请安装PDF处理库: pip install pdfplumber 或 pip install PyPDF2"
                )

    def parse_parameters(self, text: str) -> Dict[str, Optional[str]]:
        """从文本中解析参数"""
        text_upper = text.upper()

        # 定义参数提取规则
        patterns = {
            "model": [
                r"Model\s*[:=]\s*([A-Z0-9\-_]+)",
                r"压缩机型号\s*[:=]\s*([A-Z0-9\-_]+)",
                r"MODEL\s*[:=]\s*([A-Z0-9\-_]+)"
            ],
            "manufacturer": [
                r"(GMCC|美芝|HIGHLY|海立|Panasonic|松下|Mitsubishi|三菱|Hitachi|日立)",
                r"Manufacturer\s*[:=]\s*(\w+)"
            ],
            "pole_numbers": [
                r"Pole\s+Numbers?\s*[:=]\s*(\d+)",
                r"极数\s*[:=]\s*(\d+)",
                r"Poles\s*[:=]\s*(\d+)"
            ],
            "winding_resistance": [
                r"Winding\s+Resistance\s*[:=]\s*([\d\.]+)",
                r"绕组电阻\s*[:=]\s*([\d\.]+)",
                r"Resistance\s*[:=]\s*([\d\.]+)"
            ],
            "inductance_ld": [
                r"Inductance\s*[\-—]?\s*Ld\s*[:=]\s*([\d\.]+)",
                r"电感\s*[\-—]?\s*LD\s*[:=]\s*([\d\.]+)",
                r"Ld\s*[:=]\s*([\d\.]+)"
            ],
            "inductance_lq": [
                r"Inductance\s*[\-—]?\s*Lq\s*[:=]\s*([\d\.]+)",
                r"电感\s*[\-—]?\s*LQ\s*[:=]\s*([\d\.]+)",
                r"Lq\s*[:=]\s*([\d\.]+)"
            ],
            "voltage_constant": [
                r"Voltage\s+Constant\s*[:=]\s*([\d\.]+)",
                r"电压常数\s*[:=]\s*([\d\.]+)",
                r"KE\s*[:=]\s*([\d\.]+)"
            ],
            "demagnetizing_current": [
                r"Demagnetizing\s+Current\s*[:=]\s*([\d\.]+)",
                r"退磁电流\s*[:=]\s*([\d\.]+)"
            ]
        }

        results = {}

        # 提取各参数
        for param, pattern_list in patterns.items():
            value = None
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    break
            results[param] = value

        # 计算极对数
        if results.get("pole_numbers"):
            try:
                pole_num = int(results["pole_numbers"])
                results["pole_pairs"] = str(pole_num // 2)
            except (ValueError, TypeError):
                results["pole_pairs"] = None

        return results

    def display_results(self, data: Dict[str, Optional[str]]):
        """显示提取结果"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "=== 提取结果 ===\n\n")

        # 参数显示映射
        display_map = {
            "model": ("压缩机型号", ""),
            "manufacturer": ("制造商", ""),
            "pole_numbers": ("极数", "Poles"),
            "pole_pairs": ("极对数", "Pole Numbers ÷ 2"),
            "winding_resistance": ("绕组电阻", "注意是否为line-to-line"),
            "inductance_ld": ("D轴电感 LD", "Inductance-Ld"),
            "inductance_lq": ("Q轴电感 LQ", "Inductance-Lq"),
            "voltage_constant": ("反电动势系数 KE", "Vrms/Krpm"),
            "demagnetizing_current": ("退磁电流", "Apk")
        }

        for key, (cn_label, en_label) in display_map.items():
            value = data.get(key)
            if value:
                self.result_text.insert(tk.END, f"{cn_label}: {value}")
                if en_label:
                    self.result_text.insert(tk.END, f" ({en_label})")
                self.result_text.insert(tk.END, "\n")
            else:
                self.result_text.insert(tk(
                    END,
                    f"{cn_label}: [未找到]\n"
                ), "missing")

        # 标记未找到的参数
        self.result_text.tag_config("missing", foreground="red")

        # 添加提取时间
        self.result_text.insert(tk.END, f"\n提取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def save_results(self):
        """保存提取结果"""
        if not self.extracted_data:
            messagebox.showwarning("警告", "没有可保存的结果")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".json",
            filetypes=[
                ("JSON文件", "*.json"),
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )

        if file_path:
            try:
                if file_path.endswith(".json"):
                    # 添加元数据
                    save_data = {
                        "source_file": os.path.basename(self.current_file),
                        "extracted_at": datetime.now().isoformat(),
                        "parameters": self.extracted_data
                    }
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(save_data, f, indent=2, ensure_ascii=False)
                else:
                    # 保存为文本
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(self.result_text.get(1.0, tk.END))

                messagebox.showinfo("成功", f"结果已保存到: {file_path}")
                self.status_var.set(f"结果已保存: {os.path.basename(file_path)}")

            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")

    def clear_all(self):
        """清空所有内容"""
        self.current_file = None
        self.extracted_data = None
        self.file_label.config(text="未选择文件")
        self.result_text.delete(1.0, tk.END)
        self.extract_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.status_var.set("已清空")


def main():
    """主函数"""
    root = tk.Tk()
    app = PDFExtractorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
