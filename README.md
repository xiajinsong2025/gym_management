# 健身房管理系统

基于 FastAPI + SQLAlchemy + Vue 3 + Element Plus 的单店健身房管理系统。

## 项目结构

```
Gym_Mangement/
├── backend/           # 后端服务 (FastAPI)
│   ├── app/
│   │   ├── api/      # API 路由
│   │   ├── models/   # 数据模型
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── core/     # 核心配置
│   │   └── services/ # 业务服务
│   ├── tests/        # 测试文件
│   └── alembic/      # 数据库迁移
├── frontend/          # 前端应用 (Vue 3)
│   ├── src/
│   │   ├── api/      # API 接口
│   │   ├── views/    # 页面组件
│   │   ├── stores/   # 状态管理
│   │   └── router/   # 路由配置
│   └── public/       # 静态资源
└── docs/             # 项目文档
```

## 技术栈

### 后端
- Python 3.13+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic (数据库迁移)
- JWT 认证

### 前端
- Vue 3
- Vite
- Element Plus
- TypeScript
- Pinia (状态管理)
- Vue Router
- Axios

## Docker 部署（推荐服务器使用）

项目已提供：

- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `frontend/nginx.conf`

一键启动：

```bash
docker compose up -d --build
```

详细步骤见：

- [docs/deploy-docker.md](/Users/xiajingsong/Documents/code/Gym_Mangement/docs/deploy-docker.md)

## 快速开始

### 后端启动

```bash
# 安装依赖 (推荐使用 uv)
cd backend
uv install

# 数据库迁移
.venv/bin/alembic upgrade head

# 启动服务
.venv/bin/uvicorn app.main:app --reload --app-dir backend
```

后端地址：http://127.0.0.1:8000

### 前端启动

```bash
# 安装依赖
cd frontend
npm install

# 启动开发服务器
npm run dev
```

前端地址：http://localhost:3000

## 功能模块

### 已实现

1. **认证管理**
   - 用户注册、登录
   - JWT Token 认证
   - RBAC 权限控制

2. **会员管理**
   - 会员主档、画像
   - 跟进记录、反馈
   - 训练记录

3. **卡务交易**
   - 卡种管理（时间卡/次卡/储值卡/私教卡）
   - 会员卡管理（开卡/充值/冻结/解冻）
   - 订单、支付、退款
   - 卡流水记录

4. **课程管理**
   - 课程分类、课程信息
   - 排期管理
   - 预约系统（含候补）
   - 签到记录

5. **私教管理**
   - 私教课包管理
   - 排课、确认、消课

6. **前台管理**
   - 签到签退
   - 手环借还

7. **报表统计**
   - 收入日报/月报

8. **营销活动**
   - 活动管理
   - 活动报名
   - 通知系统

## API 文档

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 测试

### 后端测试

```bash
cd backend
.venv/bin/pytest -q
```

当前测试覆盖：22 passed

## 环境变量

后端环境变量示例见 `.env.example`：

```env
DATABASE_URL=postgresql+psycopg://postgres:123456@localhost:5432/gym_management
SECRET_KEY=change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

## 开发进度

- [x] 后端 API 开发
- [x] 后端测试
- [x] 前端框架搭建
- [x] 登录认证
- [x] 会员管理模块
- [x] 卡务交易模块（基础展示）
- [x] 课程管理模块（基础展示）
- [x] 私教管理模块（基础展示）
- [ ] 完善所有模块的 CRUD 功能
- [ ] 前台管理模块
- [ ] 报表统计模块
- [ ] 营销活动模块
- [ ] 前端测试

## License

MIT
