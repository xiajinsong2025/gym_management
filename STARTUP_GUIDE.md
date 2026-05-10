# 启动脚本使用指南

本指南帮助你快速启动健身房管理系统。

## 📁 脚本文件

项目提供了两个启动脚本：

1. **start.sh** - 完整功能脚本（推荐）
   - 支持启动、停止、重启、查看状态
   - 后台运行服务
   - 适合生产环境和长期运行

2. **dev.sh** - 开发快速启动脚本
   - 一键启动所有服务
   - 前台运行，方便查看日志
   - 适合开发调试

---

## 🚀 快速开始

### 方式1：使用完整脚本（推荐）

#### 启动服务

```bash
cd /Users/xiajingsong/Documents/code/Gym_Mangement
./start.sh start
```

**输出示例：**
```
[INFO] 启动健身房管理系统...
[INFO] 启动后端服务...
[INFO] 等待后端启动 (端口 8000)...
[SUCCESS] 后端服务已启动
[INFO] API 地址: http://127.0.0.1:8000
[INFO] API 文档: http://127.0.0.1:8000/docs
[INFO] 启动前端服务...
[INFO] 等待前端启动 (端口 3000)...
[SUCCESS] 前端服务已启动
[SUCCESS] 所有服务已启动！

访问地址：
  前端: http://localhost:3000
  后端: http://127.0.0.1:8000
  API文档: http://127.0.0.1:8000/docs
```

#### 停止服务

```bash
./start.sh stop
```

#### 重启服务

```bash
./start.sh restart
```

#### 查看状态

```bash
./start.sh status
```

**输出示例：**
```
[INFO] 服务状态：

[SUCCESS] 后端: 运行中 (http://127.0.0.1:8000)
  PID: 12345
[SUCCESS] 前端: 运行中 (http://localhost:3000)
  PID: 12346
```

#### 查看日志

```bash
# 查看日志文件位置
./start.sh logs

# 查看后端日志（实时）
./start.sh logs backend

# 查看前端日志（实时）
./start.sh logs frontend
```

#### 显示帮助

```bash
./start.sh help
```

---

### 方式2：使用开发脚本

```bash
cd /Users/xiajingsong/Documents/code/Gym_Mangement
./dev.sh
```

**特点：**
- 一键启动，无需参数
- 前台运行，日志直接显示在终端
- 按 `Ctrl+C` 停止所有服务
- 适合开发调试

**输出示例：**
```
🚀 启动健身房管理系统（开发模式）

启动后端服务...
启动前端服务...

✅ 服务已启动！

访问地址：
  前端: http://localhost:3000
  后端: http://127.0.0.1:8000
  API文档: http://127.0.0.1:8000/docs

按 Ctrl+C 停止所有服务
```

---

## 📝 完整命令参考

### start.sh 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `start` | 启动所有服务 | `./start.sh start` |
| `stop` | 停止所有服务 | `./start.sh stop` |
| `restart` | 重启所有服务 | `./start.sh restart` |
| `status` | 查看服务状态 | `./start.sh status` |
| `logs` | 查看日志位置 | `./start.sh logs` |
| `logs backend` | 查看后端日志 | `./start.sh logs backend` |
| `logs frontend` | 查看前端日志 | `./start.sh logs frontend` |
| `help` | 显示帮助信息 | `./start.sh help` |

---

## 🔧 高级用法

### 1. 只启动后端

```bash
# 修改 start.sh，注释掉 start_frontend 调用
# 或者手动启动
cd /Users/xiajingsong/Documents/code/Gym_Mangement
.venv/bin/uvicorn app.main:app --reload --app-dir backend
```

### 2. 只启动前端

```bash
cd /Users/xiajingsong/Documents/code/Gym_Mangement/frontend
npm run dev
```

### 3. 修改端口

**后端端口：**
```bash
.venv/bin/uvicorn app.main:app --reload --app-dir backend --port 8001
```

**前端端口：**
```bash
npm run dev -- --port 3001
```

### 4. 后台运行（生产环境）

```bash
# 使用 start.sh（推荐）
./start.sh start

# 或使用 nohup
nohup .venv/bin/uvicorn app.main:app --app-dir backend > logs/backend.log 2>&1 &
```

---

## 📂 日志文件位置

```
Gym_Mangement/
├── logs/
│   ├── backend.log    # 后端日志
│   └── frontend.log   # 前端日志
└── .pids/
    ├── backend.pid    # 后端进程ID
    └── frontend.pid   # 前端进程ID
```

---

## ⚠️ 常见问题

### 1. 权限被拒绝

```bash
chmod +x start.sh dev.sh
```

### 2. 端口被占用

```bash
# 查看端口占用
lsof -i :8000  # 后端
lsof -i :3000  # 前端

# 停止服务
./start.sh stop

# 或强制杀死进程
kill -9 <PID>
```

### 3. 虚拟环境不存在

```bash
# 安装依赖
cd /Users/xiajingsong/Documents/code/Gym_Mangement
uv install
```

### 4. 前端依赖未安装

```bash
cd frontend
npm install
```

### 5. 数据库未创建

```bash
# 创建数据库
createdb gym_management

# 运行迁移
.venv/bin/alembic upgrade head
```

---

## 🎯 推荐工作流

### 开发环境

```bash
# 1. 启动服务
./dev.sh

# 2. 开发代码...

# 3. 按 Ctrl+C 停止
```

### 生产环境

```bash
# 1. 启动服务（后台运行）
./start.sh start

# 2. 查看状态
./start.sh status

# 3. 查看日志
./start.sh logs backend

# 4. 停止服务
./start.sh stop
```

---

## 📊 服务健康检查

启动后，可以通过以下方式验证服务是否正常：

### 后端健康检查

```bash
curl http://127.0.0.1:8000/api/v1/health
```

**预期输出：**
```json
{"code":0,"message":"ok","data":{"status":"ok"}}
```

### 前端访问

浏览器打开：http://localhost:3000

---

## 🎉 快速启动清单

- [ ] 确保已安装依赖（后端：`uv install`，前端：`npm install`）
- [ ] 确保数据库已创建并迁移
- [ ] 运行启动脚本：`./start.sh start` 或 `./dev.sh`
- [ ] 访问前端：http://localhost:3000
- [ ] 注册用户并登录

---

现在你可以使用这些脚本快速启动系统了！🚀
