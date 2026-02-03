# 📦 macOS版本说明

> **本文件夹包含 macOS 系统专用的文档和脚本**

---

## 📋 文件清单

### 📄 文档文件

| 文件名 | 说明 | 适用对象 |
|--------|------|----------|
| `README-macOS.md` | 项目总览和快速导航 | 所有用户 |
| `快速启动指南-macOS.md` | 5分钟快速上手 | 新用户 |
| `使用手册-macOS.md` | 详细图文教程 | 所有用户 |
| `项目移交文档-macOS.md` | 完整技术文档 | 管理员/技术人员 |

### 🔧 脚本文件

| 文件名 | 说明 | 使用方法 |
|--------|------|----------|
| `install-dependencies.sh` | 自动安装所有依赖 | `./install-dependencies.sh` |
| `start-services.sh` | 一键启动前后端服务 | `./start-services.sh` |
| `diagnose.sh` | 系统诊断工具 | `./diagnose.sh` |

---

## 🚀 快速开始

### 首次使用（3步）

```bash
# 1. 进入项目目录
cd ~/Desktop/网页重置

# 2. 添加执行权限
chmod +x macOS版本/*.sh

# 3. 安装依赖
./macOS版本/install-dependencies.sh
```

### 日常使用（1步）

```bash
# 启动系统
./macOS版本/start-services.sh
```

然后打开浏览器访问：`http://localhost:5174/`

---

## 🔄 与 Windows 版本的区别

| 项目 | Windows | macOS |
|------|---------|-------|
| **脚本格式** | `.bat` | `.sh` |
| **Python命令** | `python` | `python3` |
| **虚拟环境激活** | `venv\Scripts\activate` | `source venv/bin/activate` |
| **路径分隔符** | `\` | `/` |
| **终端** | CMD/PowerShell | Terminal |
| **前端端口** | 5174 | 5174 |
| **后端端口** | 8000 | 8000 |

---

## ⚠️ 重要提示

### 1. 脚本权限

macOS 需要给脚本添加执行权限：

```bash
chmod +x *.sh
```

### 2. 显示隐藏文件

在 Finder 中按 `Command + Shift + .` 可以显示/隐藏 `.env` 等隐藏文件。

### 3. 安全提示

首次运行脚本时，macOS 可能会提示安全警告：
- 打开"系统偏好设置" → "安全性与隐私"
- 点击"仍要打开"

### 4. 端口号

- 前端服务：`http://localhost:5174/`
- 后端服务：`http://localhost:8000/`

---

## 📚 推荐阅读顺序

```
1. README-macOS.md          # 了解项目概况
   ↓
2. 快速启动指南-macOS.md    # 5分钟快速上手
   ↓
3. 使用手册-macOS.md        # 详细操作步骤
   ↓
4. 项目移交文档-macOS.md    # 完整技术文档
```

---

## 🆘 遇到问题？

### 1. 运行诊断工具

```bash
./diagnose.sh
```

### 2. 查看文档

- 常见问题：查看《使用手册-macOS.md》
- 技术细节：查看《项目移交文档-macOS.md》

### 3. 检查权限

```bash
# 查看文件权限
ls -la

# 添加执行权限
chmod +x *.sh
```

---

## 📞 技术支持

如果遇到无法解决的问题：

1. 运行 `./diagnose.sh` 获取诊断报告
2. 截图错误信息
3. 说明操作步骤
4. 提供 macOS 版本信息

---

## ✅ 安装检查清单

使用前请确认：

- [ ] 已安装 Python 3.8+
- [ ] 已安装 Node.js 16+
- [ ] 已配置 `backend/.env` 文件
- [ ] 已添加脚本执行权限（`chmod +x *.sh`）
- [ ] 已运行 `install-dependencies.sh`
- [ ] 网络连接正常
- [ ] API 密钥有效

---

## 🎯 系统要求

### 必需软件

- **Python**: 3.8 或更高
- **Node.js**: 16 或更高
- **macOS**: 10.14 (Mojave) 或更高

### 硬件要求

- **处理器**: 双核或更高
- **内存**: 4GB 或更高
- **硬盘**: 2GB 可用空间
- **网络**: 稳定的互联网连接

---

## 📝 版本信息

- **版本**: v2.1.0 (macOS)
- **更新日期**: 2026年2月3日
- **兼容系统**: macOS 10.14+
- **前端端口**: 5174
- **后端端口**: 8000

---

## 🔗 相关链接

- Python 下载：https://www.python.org/downloads/
- Node.js 下载：https://nodejs.org/
- 项目主页：（待添加）

---

**祝您使用愉快！** 🎉

如有问题，请查看相关文档或联系技术支持。
