# PDF 压缩机参数提取工具

一款用于从PDF文件中提取压缩机参数的 Windows GUI 应用程序。

## 功能特性

- **批量提取**：从PDF规格书中自动提取压缩机参数
- **参数识别**：支持提取以下参数：
  - 压缩机型号 (Model)
  - 制造商 (GMCC/美芝、HIGHLY/海立等)
  - 极数 / 极对数 (Pole Numbers / Pole Pairs)
  - 绕组电阻 (Winding Resistance)
  - D轴电感 LD (Inductance-Ld)
  - Q轴电感 LQ (Inductance-Lq)
  - 反电动势系数 KE (Voltage Constant)
  - 退磁电流 (Demagnetizing Current)
- **结果保存**：支持JSON和TXT格式导出
- **图形界面**：简洁易用的中文界面

## 安装与运行

### 方法一：直接运行 Python 脚本

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行程序：
```bash
python pdf_extractor.py
```

### 方法二：打包为 EXE 文件

1. 安装依赖（同上）

2. 打包生成 EXE：
```bash
pyinstaller --onefile --windowed --name="PDF压缩机参数提取工具" pdf_extractor.py
```

3. 在 `dist` 目录下找到生成的 EXE 文件，双击运行

## 使用说明

1. 点击 **"选择PDF文件"** 按钮上传PDF规格书
2. 点击 **"提取参数"** 按钮开始分析
3. 查看提取结果，未找到的参数会以红色标注
4. 点击 **"保存结果"** 导出提取的参数数据
5. 点击 **"清空"** 重置界面

## 系统要求

- Windows 10 或更高版本
- Python 3.8+ (如需运行脚本)
- PDF文件规格书

## 开发

### 项目结构

```
.
├── pdf_extractor.py      # 主程序文件
├── requirements.txt      # Python依赖
└── README.md            # 说明文档
```

### 添加新的参数提取规则

编辑 `pdf_extractor.py` 中的 `parse_parameters` 方法，在 `patterns` 字典中添加新的正则表达式规则：

```python
patterns = {
    "new_parameter": [
        r"Parameter Name\s*[:=]\s*([A-Z0-9\-_]+)",
        r"参数名称\s*[:=]\s*([\d\.]+)"
    ],
    # ... 其他规则
}
```

## 注意事项

- 参数提取依赖于PDF中的文本格式，如果PDF是扫描图片需要先进行OCR处理
- 不同厂家的PDF格式可能不同，可能需要调整正则表达式规则
- 绕组电阻需要根据PDF中的说明判断是否为 line-to-line 值

## 许可证

MIT License

---

如有问题或建议，欢迎提交 Issue。