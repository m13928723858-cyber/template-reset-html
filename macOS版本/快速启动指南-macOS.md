# ⚡ 快速启动指南 (macOS版)

> **5分钟快速上手** - 适合完全不懂代码的用户

---

## 🎯 第一次使用？按这个顺序操作！

### 步骤1️⃣：安装必需软件（只需做一次）

#### 安装Python
1. 访问：https://www.python.org/downloads/
2. 下载最新版本（3.8或更高）
3. 打开下载的 `.pkg` 文件
4. 按照安装向导完成安装

#### 安装Node.js
1. 访问：https://nodejs.org/
2. 下载LTS版本（推荐）
3. 打开下载的 `.pkg` 文件
4. 使用默认选项安装

#### 验证安装
打开**终端**（按 `Command + 空格`，输入 `Terminal`，回车），输入：
```bash
python3 --version
node --version
```
如果显示版本号，说明安装成功！✅

---

### 步骤2️⃣：配置API密钥（只需做一次）

1. 打开文件夹：`网页重置/backend`
2. 找到文件：`.env`
3. 用文本编辑器打开，修改这一行：
   ```
   DOLPHIN_API_KEY=你的API密钥
   ```
4. 将 `你的API密钥` 替换为实际的密钥
5. 保存文件（`Command + S`）

---

### 步骤3️⃣：安装依赖包（只需做一次）

#### 方法A：使用安装脚本（推荐）

1. 找到文件：`网页重置/install-dependencies.sh`
2. 打开终端，输入：
   ```bash
   cd ~/Desktop/网页重置
   chmod +x install-dependencies.sh
   ./install-dependencies.sh
   ```
3. 等待安装完成（约5-10分钟）

#### 方法B：手动安装

**安装后端依赖：**
```bash
cd ~/Desktop/网页重置/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**安装前端依赖：**
```bash
cd ~/Desktop/网页重置/frontend
npm install
```

---

### 步骤4️⃣：启动系统（每次使用都要做）

#### 最简单的方法：

1. 找到文件：`网页重置/start-services.sh`
2. 打开终端，输入：
   ```bash
   cd ~/Desktop/网页重置
   chmod +x start-services.sh
   ./start-services.sh
   ```
3. 等待几秒钟，会打开两个终端窗口
4. 看到以下信息说明启动成功：
   - 窗口1：`Uvicorn running on http://0.0.0.0:8000`
   - 窗口2：`Local: http://localhost:5173/`

⚠️ **重要**：不要关闭这两个终端窗口！

---

### 步骤5️⃣：打开系统

打开浏览器（推荐Chrome或Safari），访问：
```
http://localhost:5174/
```

---

## 🎨 如何使用

### 界面说明

您会看到三个输入框：

1. **Winner产品名称** - 填写您的产品名称
2. **产品类型** - 填写产品类别
3. **上传产品图片** - 可选，上传产品主图

### 操作示例

**示例1：加热背心**
```
Winner产品名称：Ororo Heated Vest
产品类型：heated vest
```

**示例2：运动鞋**
```
Winner产品名称：Nike Air Max
产品类型：running shoes
```

**示例3：咖啡机**
```
Winner产品名称：Nespresso Vertuo
产品类型：coffee machine
```

### 生成页面

1. 填写产品信息
2. （可选）上传产品图片
3. 点击"生成页面"按钮
4. 等待约60秒
5. 点击"下载结果"按钮
6. 解压ZIP文件
7. 双击打开 `index.html` 查看结果

---

## 🛑 如何停止系统

1. 关闭浏览器
2. 在两个终端窗口中按 `Control + C`
3. 关闭窗口

---

## ❓ 遇到问题？

### 问题1：脚本无法执行
**解决**：运行 `chmod +x *.sh` 给脚本添加执行权限

### 问题2：提示"command not found"
**解决**：检查Python和Node.js是否正确安装

### 问题3：浏览器无法访问
**解决**：确认两个终端窗口都在运行

### 问题4：生成失败
**解决**：检查 `.env` 文件中的API密钥是否正确

### 问题5：图片无法显示
**解决**：检查网络连接，重新生成

### 更多问题？
运行诊断工具：`./diagnose.sh`

---

## 📋 每日使用流程

```
1. 运行 ./start-services.sh
   ↓
2. 等待启动（约10秒）
   ↓
3. 打开浏览器访问 http://localhost:5174/
   ↓
4. 填写产品信息
   ↓
5. 点击"生成页面"
   ↓
6. 等待60秒
   ↓
7. 下载结果
   ↓
8. 完成！按 Control+C 停止服务
```

---

## 🎯 重要提示

✅ **必须做的**：
- 保持网络连接
- 不要关闭终端窗口
- 等待生成完成（约60秒）

❌ **不要做的**：
- 不要重复点击"生成页面"
- 不要在生成过程中关闭浏览器
- 不要修改生成的文件结构

---

## 📞 需要帮助？

1. 查看完整文档：`项目移交文档-macOS.md`
2. 运行诊断工具：`./diagnose.sh`
3. 联系技术支持

---

**版本**: v2.1.0  
**更新**: 2026年2月3日

**祝您使用愉快！** 🎉
