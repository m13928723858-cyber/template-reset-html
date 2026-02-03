# 🎨 AI智能页面生成系统 (macOS版)

> **一键生成专业营销页面** - 无需编程知识，60秒自动生成

[![版本](https://img.shields.io/badge/版本-v2.1.0-blue.svg)](https://github.com/yourusername/brand-swap)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-16+-green.svg)](https://nodejs.org/)
[![平台](https://img.shields.io/badge/平台-macOS-lightgrey.svg)](https://www.apple.com/macos/)

---

## 🎯 这是什么？

一个基于AI的智能营销页面生成系统，只需输入产品信息，即可自动生成完整的产品对比评测页面。

### ✨ 核心功能

- 🤖 **AI自动生成** - 竞品分析、文案创作、图片爬取
- 📄 **专业模板** - 基于真实营销页面优化
- 🖼️ **本地图片** - 图片下载到本地，加载更快
- 🎨 **完全自动** - 无需手动编辑，一键生成

### 🚀 快速开始

**只需3步**：

1. **输入产品信息**
   ```
   产品名称：Ororo Heated Vest
   产品类型：heated vest
   ```

2. **点击生成**
   ```
   等待60秒...
   ```

3. **下载结果**
   ```
   获得完整的HTML网页
   ```

---

## 📚 文档导航

### 🆕 新用户必读

| 文档 | 说明 | 阅读时间 |
|------|------|----------|
| [快速启动指南-macOS.md](快速启动指南-macOS.md) | 5分钟快速上手 | ⏱️ 5分钟 |
| [使用手册-macOS.md](使用手册-macOS.md) | 图文教程，详细步骤 | ⏱️ 15分钟 |
| [项目移交文档-macOS.md](项目移交文档-macOS.md) | 完整技术文档 | ⏱️ 30分钟 |

### 📖 推荐阅读顺序

```
第一次使用？
    ↓
1. 阅读《快速启动指南-macOS》
    ↓
2. 按照步骤安装软件
    ↓
3. 配置API密钥
    ↓
4. 运行 ./install-dependencies.sh
    ↓
5. 运行 ./start-services.sh
    ↓
6. 打开浏览器开始使用
    ↓
遇到问题？
    ↓
查看《使用手册-macOS》的常见问题部分
```

---

## 🔧 系统要求

### 必需软件

| 软件 | 版本 | 下载地址 |
|------|------|----------|
| Python | 3.8+ | https://www.python.org/downloads/ |
| Node.js | 16+ | https://nodejs.org/ |

### 硬件要求

- **处理器**: 双核或更高
- **内存**: 4GB或更高
- **硬盘**: 2GB可用空间
- **网络**: 稳定的互联网连接

---

## ⚡ 快速安装

### 方法1：自动安装（推荐）

```bash
# 1. 打开终端，进入项目目录
cd ~/Desktop/网页重置

# 2. 添加执行权限
chmod +x install-dependencies.sh

# 3. 运行安装脚本
./install-dependencies.sh

# 4. 配置API密钥
# 编辑 backend/.env 文件
```

### 方法2：手动安装

```bash
# 安装后端依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 安装前端依赖
cd ../frontend
npm install
```

---

## 🚀 启动系统

### 最简单的方法

```bash
# 添加执行权限（首次需要）
chmod +x start-services.sh

# 启动系统
./start-services.sh
```

### 手动启动

```bash
# 终端1 - 启动后端
cd backend
source venv/bin/activate
python main.py

# 终端2 - 启动前端
cd frontend
npm run dev
```

### 访问系统

打开浏览器，访问：
```
http://localhost:5174/
```

---

## 📊 功能特性

### AI自动生成

| 功能 | 说明 | 数量 |
|------|------|------|
| 竞品生成 | 自动生成真实竞品 | 4个 |
| 标题生成 | 营销标题 | 46个 |
| 段落生成 | 产品描述 | 37个 |
| 列表生成 | 优点/缺点 | 17个 |
| 图片爬取 | 产品图片 | 12张 |

### 处理性能

| 指标 | 数值 |
|------|------|
| 总处理时间 | ~60秒 |
| 竞品生成 | ~4秒 |
| 内容生成 | ~35秒 |
| 图片爬取 | ~18秒 |
| Token消耗 | ~4,600 |

---

## 📁 项目结构

```
网页重置/
├── 📄 快速启动指南-macOS.md     # 5分钟快速上手
├── 📄 使用手册-macOS.md         # 图文教程
├── 📄 项目移交文档-macOS.md     # 完整技术文档
├── 📄 README-macOS.md          # 本文件
│
├── 🔧 install-dependencies.sh  # 安装依赖脚本
├── 🚀 start-services.sh       # 启动系统脚本
├── 🔍 diagnose.sh             # 诊断工具
│
├── backend/                   # 后端服务
│   ├── services/             # 核心服务
│   ├── main.py              # 主程序
│   ├── .env                 # 配置文件（需要配置）
│   └── requirements.txt     # Python依赖
│
├── frontend/                 # 前端界面
│   ├── src/                 # 源代码
│   └── package.json         # Node.js依赖
│
└── top5Grounded Footwear/   # 原始模板
    ├── index.html
    ├── css/
    └── image/
```

---

## 🎯 使用示例

### 示例1：加热背心

**输入**：
```
产品名称：Ororo Heated Vest
产品类型：heated vest
```

**输出**：
- 完整的产品对比页面
- 包含4个竞品
- 12张产品图片
- 专业的营销文案

---

## ❓ 常见问题

### Q: 需要编程知识吗？

**A**: 完全不需要！只需要：
1. 会使用终端运行命令
2. 会在浏览器中填写表单
3. 会下载和解压文件

### Q: 生成一次需要多长时间？

**A**: 约60秒

### Q: 与Windows版本有什么区别？

**A**: 
- 使用 `.sh` 脚本代替 `.bat` 脚本
- 使用 `python3` 代替 `python`
- 使用 `source` 激活虚拟环境
- 其他功能完全相同

---

## 🐛 故障排查

### 问题1：脚本无法执行

**症状**：提示 "Permission denied"

**解决**：
```bash
chmod +x *.sh
```

### 问题2：Python命令不存在

**症状**：提示 "command not found: python3"

**解决**：
1. 安装Python 3.8+
2. 确保Python已添加到PATH

### 更多问题？

运行诊断工具：
```bash
./diagnose.sh
```

---

## 📞 获取帮助

### 自助资源

1. **文档**
   - [快速启动指南-macOS](快速启动指南-macOS.md)
   - [使用手册-macOS](使用手册-macOS.md)
   - [项目移交文档-macOS](项目移交文档-macOS.md)

2. **工具**
   - 诊断工具：`./diagnose.sh`
   - 日志文件：查看终端输出

---

## 🔄 更新日志

### v2.1.0 (2026-02-03)

#### 新增功能
- ✅ macOS版本支持
- ✅ Shell脚本替代批处理文件
- ✅ 完整的macOS文档

---

## 📄 许可证

本项目采用 MIT 许可证。

---

<div align="center">

**最后更新**: 2026年2月3日  
**版本**: v2.1.0 (macOS)  
**状态**: ✅ 稳定运行

---

**感谢使用 AI智能页面生成系统！** 🎉

</div>
