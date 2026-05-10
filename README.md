# Gym Management (Single Club)

基于 FastAPI + SQLAlchemy + Alembic 的单店健身房管理系统后端。

## 1. 运行环境

- Python `>=3.13`
- PostgreSQL（默认配置：`gym_management` / `postgres:123456`）

环境变量示例见：

- [/Users/xiajingsong/Documents/code/Gym_Mangement/.env.example](/Users/xiajingsong/Documents/code/Gym_Mangement/.env.example)

## 2. 本地启动

1. 安装依赖（推荐 `uv`）  
2. 执行迁移：

```bash
.venv/bin/alembic upgrade head
```

3. 启动服务：

```bash
.venv/bin/uvicorn app.main:app --reload --app-dir backend
```

默认地址：`http://127.0.0.1:8000`  
健康检查：`GET /api/v1/health`

## 3. 测试

```bash
.venv/bin/pytest -q
```

当前回归：`22 passed`（2026-05-10）。

## 4. 已实现模块

- `auth`：注册、登录、当前用户自助绑定权限
- `members`：会员主档、画像、跟进、反馈、训练记录
- `transactions`：卡种、开卡、充值、冻结/解冻、订单、支付、卡流水
- `courses`：课程分类、课程、排期、预约（含候补）
- `personal-training`：私教课包、排课、确认、消课
- `front-desk`：签到签退、手环借还
- `reports`：收入日报/月报（订单与支付聚合）
- `marketing`：活动、活动报名、通知

## 5. API 约定

统一约定见：

- [/Users/xiajingsong/Documents/code/Gym_Mangement/docs/api-conventions.md](/Users/xiajingsong/Documents/code/Gym_Mangement/docs/api-conventions.md)

## 6. 权限模型（最小版）

- 所有业务鉴权基于 Bearer Token（JWT）
- RBAC 校验依赖 `require_permission("<resource>:<action>")`
- 可通过 `POST /api/v1/auth/me/permissions` 给当前用户绑定权限（开发期便捷接口）
