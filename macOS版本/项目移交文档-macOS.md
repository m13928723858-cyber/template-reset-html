# 🎯 AI智能页面生成系统 - 项目移交文档 (macOS版)

> **适用对象**: 完全不懂代码的使用者  
> **最后更新**: 2026年2月3日  
> **版本**: v2.1.0 (macOS)

---

## 📋 目录

1. [项目简介](#项目简介)
2. [系统要求](#系统要求)
3. [安装步骤](#安装步骤)
4. [启动系统](#启动系统)
5. [使用指南](#使用指南)
6. [常见问题](#常见问题)
7. [macOS特别说明](#macos特别说明)
8. [注意事项](#注意事项)
9. [联系支持](#联系支持)

---

## 📖 项目简介

### 这个系统是做什么的？

这是一个**AI智能营销页面生成系统**，可以帮您自动生成专业的产品对比评测页面。

**您只需要提供**：
- ✅ 您的产品名称（例如：Ororo Heated Vest）
- ✅ 产品类型（例如：heated vest）
- ✅ 可选：上传一张产品图片

**系统会自动**：
- 🤖 生成4个竞品品牌
- ✍️ 生成完整的营销文案（标题、段落、列表等）
- 🖼️ 爬取12张产品图片
- 📄 生成完整的HTML网页

**最终您会得到**：
- 📦 一个ZIP压缩包
- 📄 包含完整的网页文件（HTML、CSS、图片）
- 🌐 可以直接上传到服务器使用

---

## 💻 系统要求

### 必需软件

在开始之前，您的Mac需要安装以下软件：

#### 1. Python（编程语言）
- **版本**: Python 3.8 或更高
- **下载地址**: https://www.python.org/downloads/
- **安装提示**: 
  - 下载 `.pkg` 安装包
  - 双击安装，使用默认选项

#### 2. Node.js（JavaScript运行环境）
- **版本**: Node.js 16 或更高
- **下载地址**: https://nodejs.org/
- **安装提示**: 
  - 选择 LTS（长期支持）版本
  - 下载 `.pkg` 安装包
  - 使用默认安装选项即可

### 检查是否安装成功

安装完成后，打开**终端**（按 `Command + 空格`，输入 `Terminal`，回车），输入以下命令检查：

```bash
python3 --version
```
应该显示类似：`Python 3.11.0`

```bash
node --version
```
应该显示类似：`v18.17.0`

如果显示版本号，说明安装成功！

---

## 🔧 安装步骤

### 第一步：获取项目文件

1. 将整个项目文件夹复制到您的Mac
2. 建议放在桌面或容易找到的位置
3. 文件夹名称：`网页重置`

### 第二步：配置API密钥

**重要**：系统需要AI服务来生成内容，您需要配置API密钥。

1. 打开Finder，进入：`网页重置/backend`
2. 按 `Command + Shift + .` 显示隐藏文件
3. 找到文件：`.env`（如果没有，创建一个新的文本文件，命名为 `.env`）
4. 用文本编辑器打开，填入以下内容：

```env
# AI服务密钥（必需）
DOLPHIN_API_KEY=你的API密钥
DOLPHIN_BASE_URL=https://dolphin-chat.ihippogame.com/api/v1

# 服务器配置
PORT=8000
HOST=0.0.0.0

# 文件配置
MAX_FILE_SIZE=104857600
UPLOAD_DIR=./uploads
OUTPUT_DIR=./outputs
TEMP_DIR=./temp

# 爬虫配置
IMAGES_PER_BRAND=10
CRAWL_TIMEOUT=30
MAX_CONCURRENT_DOWNLOADS=5
```

⚠️ **重要**：将 `你的API密钥` 替换为实际的密钥

### 第三步：安装依赖包

#### 使用安装脚本（推荐）

1. 打开**终端**（按 `Command + 空格`，输入 `Terminal`，回车）
2. 进入项目目录：
   ```bash
   cd ~/Desktop/网页重置
   ```
3. 添加执行权限：
   ```bash
   chmod +x install-dependencies.sh
   ```
4. 运行安装脚本：
   ```bash
   ./install-dependencies.sh
   ```
5. 等待安装完成（约5-10分钟）

#### 手动安装（备选方案）

**安装后端依赖：**
```bash
cd ~/Desktop/网页重置/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

**安装前端依赖：**
```bash
cd ~/Desktop/网页重置/frontend
npm install
```

---

## 🚀 启动系统

### 方法一：使用启动脚本（推荐）

**最简单的方法**：

1. 打开终端
2. 进入项目目录：
   ```bash
   cd ~/Desktop/网页重置
   ```
3. 添加执行权限（首次需要）：
   ```bash
   chmod +x start-services.sh
   ```
4. 运行启动脚本：
   ```bash
   ./start-services.sh
   ```
5. 会自动打开两个新的终端窗口
6. 等待几秒钟，直到看到：
   - 窗口1显示：`INFO: Uvicorn running on http://0.0.0.0:8000`
   - 窗口2显示：`Local: http://localhost:5173/`
7. 系统启动成功！

⚠️ **注意**：
- 不要关闭这两个终端窗口
- 关闭窗口会停止系统运行

### 方法二：手动启动

如果启动脚本不工作，可以手动启动：

#### 启动后端

1. 打开终端
2. 进入后端文件夹：
   ```bash
   cd ~/Desktop/网页重置/backend
   ```
3. 激活虚拟环境：
   ```bash
   source venv/bin/activate
   ```
4. 启动后端：
   ```bash
   python main.py
   ```

#### 启动前端

1. 打开**新的**终端窗口（`Command + T`）
2. 进入前端文件夹：
   ```bash
   cd ~/Desktop/网页重置/frontend
   ```
3. 启动前端：
   ```bash
   npm run dev
   ```

### 访问系统

启动成功后，打开浏览器（推荐使用Chrome或Safari），访问：

```
http://localhost:5174/
```

---

## 📱 使用指南

### 界面说明

打开系统后，您会看到一个简洁的界面，包含三个输入框：

1. **Winner产品名称** - 您的产品名称
2. **产品类型** - 产品的类别
3. **上传产品图片** - 可选，上传您的产品主图

### 操作步骤

#### 第一步：填写产品信息

**示例1：加热背心**
- Winner产品名称：`Ororo Heated Vest`
- 产品类型：`heated vest`

**示例2：运动鞋**
- Winner产品名称：`Nike Air Max`
- 产品类型：`running shoes`

**示例3：咖啡机**
- Winner产品名称：`Nespresso Vertuo`
- 产品类型：`coffee machine`

#### 第二步：上传产品图片（可选）

1. 点击"选择文件"按钮
2. 选择您的产品图片（支持 JPG、PNG 格式）
3. 建议图片尺寸：600x600 像素
4. 如果不上传，系统会自动爬取图片

#### 第三步：生成页面

1. 点击"生成页面"按钮
2. 系统开始处理，您会看到进度提示：
   - ⏳ 正在生成竞品...（约4秒）
   - ⏳ 正在生成营销文案...（约35秒）
   - ⏳ 正在爬取产品图片...（约18秒）
   - ⏳ 正在填充模板...（约1秒）
3. 总共需要约60秒

#### 第四步：下载结果

1. 处理完成后，会显示"下载结果"按钮
2. 点击按钮，下载ZIP压缩包
3. 双击ZIP文件自动解压，您会得到：
   ```
   生成的页面/
   ├── index.html      # 网页文件
   ├── css/            # 样式文件
   │   └── custom-styles.css
   └── image/          # 图片文件夹
       ├── image_1.jpg
       ├── image_2.jpg
       └── ...
   ```

#### 第五步：查看结果

1. 找到解压后的文件夹
2. 双击打开 `index.html`
3. 会在浏览器中打开生成的页面
4. 您可以查看完整的产品对比评测页面

---

## ❓ 常见问题

### 问题1：提示"Permission denied"

**原因**：脚本没有执行权限

**解决方法**：
```bash
cd ~/Desktop/网页重置
chmod +x *.sh
```

### 问题2：提示"command not found: python3"

**原因**：Python未正确安装

**解决方法**：
1. 重新安装Python 3.8+
2. 确保安装的是macOS版本
3. 重启终端
4. 验证：`python3 --version`

### 问题3：提示"command not found: node"

**原因**：Node.js未正确安装

**解决方法**：
1. 重新安装Node.js 16+
2. 选择LTS版本
3. 重启终端
4. 验证：`node --version`

### 问题4：浏览器无法访问

**原因**：端口被占用或服务未启动

**解决方法**：

**检查服务是否启动**：
```
1. 查看两个终端窗口
2. 确认没有错误信息
3. 看到"Uvicorn running"说明启动成功
```

**检查端口占用**：
```bash
# 检查8000端口
lsof -i :8000

# 检查5174端口
lsof -i :5174

# 如果被占用，杀死进程
kill -9 <PID>
```

### 问题5：生成失败，提示API错误

**原因**：API密钥无效或配额不足

**解决方法**：

**检查API密钥**：
```bash
cat backend/.env | grep DOLPHIN_API_KEY
```

确保：
- 密钥完整（通常很长）
- 没有多余的空格
- 格式正确：`DOLPHIN_API_KEY=sk-xxx...`

**检查API配额**：
1. 登录API服务提供商网站
2. 查看剩余配额
3. 如果配额不足，需要充值

### 问题6：图片无法显示或下载失败

**原因**：网络问题或图片源不可用

**解决方法**：

**检查网络**：
```bash
ping google.com
```

**重新生成**：
1. 点击"重新生成"
2. 或上传自己的产品图片
3. 系统会使用您上传的图片

---

## 🍎 macOS特别说明

### 与Windows版本的区别

| 项目 | Windows | macOS |
|------|---------|-------|
| 脚本格式 | `.bat` | `.sh` |
| Python命令 | `python` | `python3` |
| 虚拟环境激活 | `venv\Scripts\activate` | `source venv/bin/activate` |
| 路径分隔符 | `\` | `/` |
| 终端 | CMD/PowerShell | Terminal |

### 终端使用技巧

**打开终端的方法**：
1. 按 `Command + 空格`
2. 输入 `Terminal`
3. 回车

**常用快捷键**：
- `Control + C`: 停止当前进程
- `Command + T`: 新建标签
- `Command + W`: 关闭当前标签
- `Command + Q`: 退出终端

### 文件权限

macOS对脚本执行有严格的权限控制：

```bash
# 查看文件权限
ls -la

# 添加执行权限
chmod +x script.sh

# 添加所有.sh文件的执行权限
chmod +x *.sh
```

### 显示隐藏文件

在Finder中：
- 按 `Command + Shift + .`（点号）
- 可以显示/隐藏以 `.` 开头的文件（如 `.env`）

### 安全提示

首次运行脚本时，macOS可能会提示安全警告：

1. 打开"系统偏好设置"
2. 选择"安全性与隐私"
3. 在"通用"标签下，点击"仍要打开"

或者使用命令：
```bash
xattr -d com.apple.quarantine script.sh
```

---

## ⚠️ 注意事项

### 使用前必读

1. **保持网络连接**
   - 系统需要联网才能使用AI服务
   - 需要联网才能爬取图片

2. **不要关闭终端窗口**
   - 系统运行时会有两个终端窗口
   - 关闭窗口会停止服务

3. **API配额**
   - 每次生成会消耗约4,600个Token
   - 请注意API配额限制

4. **处理时间**
   - 每次生成需要约60秒
   - 请耐心等待，不要重复点击

5. **文件保存**
   - 生成的文件保存在 `backend/outputs` 文件夹
   - 定期清理旧文件以节省空间

### 系统限制

- **图片数量**: 每次生成12张图片
- **竞品数量**: 固定生成4个竞品
- **文案长度**: 约46个标题、37个段落
- **处理时间**: 约60秒
- **文件大小**: 生成的ZIP约5-10MB

---

## 🔄 停止系统

### 正常停止

1. 关闭浏览器标签页
2. 在两个终端窗口中按 `Control + C`
3. 等待服务停止
4. 关闭终端窗口（`Command + Q`）

### 强制停止

如果无法正常停止：

```bash
# 杀死所有Python进程
killall python3

# 杀死所有Node进程
killall node

# 或者使用活动监视器
# 打开"活动监视器"（在"应用程序/实用工具"中）
# 搜索"python"和"node"
# 选中进程，点击"退出"
```

---

## 🆘 联系支持

### 遇到问题？

如果您遇到无法解决的问题，请：

1. **查看日志**
   - 终端窗口中的错误信息
   - 截图保存

2. **运行诊断**
   ```bash
   ./diagnose.sh
   ```
   - 查看诊断报告

3. **联系技术支持**
   - 提供错误截图
   - 说明操作步骤
   - 提供诊断报告
   - 说明macOS版本

### 诊断工具

项目包含诊断工具，可以自动检查常见问题：

```bash
cd ~/Desktop/网页重置
chmod +x diagnose.sh
./diagnose.sh
```

---

## 📚 附录

### 文件说明

```
网页重置/
├── backend/                    # 后端程序（Python）
│   ├── services/              # 核心功能模块
│   ├── main.py               # 主程序
│   ├── .env                  # 配置文件（需要您填写）
│   ├── requirements.txt      # 依赖列表
│   └── venv/                 # 虚拟环境（自动创建）
├── frontend/                  # 前端界面（网页）
│   ├── src/                  # 源代码
│   ├── package.json          # 依赖配置
│   └── node_modules/         # 依赖包（自动创建）
├── top5Grounded Footwear/    # 模板文件
│   ├── index.html            # 模板HTML
│   ├── css/                  # 样式文件
│   └── image/                # 模板图片
├── install-dependencies.sh   # 安装脚本
├── start-services.sh        # 启动脚本
├── diagnose.sh             # 诊断脚本
└── 项目移交文档-macOS.md    # 本文档
```

### 技术术语解释

- **Python**: 一种编程语言，用于后端处理
- **Node.js**: JavaScript运行环境，用于前端界面
- **API**: 应用程序接口，用于调用AI服务
- **Token**: AI服务的计费单位
- **ZIP**: 压缩文件格式
- **HTML**: 网页文件格式
- **CSS**: 网页样式文件
- **Shell脚本**: `.sh` 文件，用于自动化任务

### 快捷键参考

| 快捷键 | 功能 |
|--------|------|
| `Command + 空格` | 打开Spotlight搜索 |
| `Command + T` | 新建终端标签 |
| `Command + W` | 关闭当前标签 |
| `Command + Q` | 退出应用 |
| `Control + C` | 停止当前进程 |
| `Command + Shift + .` | 显示/隐藏隐藏文件 |

---

## ✅ 检查清单

在开始使用前，请确认：

- [ ] 已安装Python 3.8+
- [ ] 已安装Node.js 16+
- [ ] 已配置 `.env` 文件
- [ ] 已添加脚本执行权限
- [ ] 已安装后端依赖
- [ ] 已安装前端依赖
- [ ] 网络连接正常
- [ ] API密钥有效
- [ ] 已阅读使用指南
- [ ] 了解macOS特别说明

---

## 📞 技术支持

**项目版本**: v2.1.0 (macOS)  
**最后更新**: 2026年2月3日  
**文档版本**: 1.0

---

**祝您使用愉快！** 🎉
