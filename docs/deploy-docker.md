# Docker 部署指南（服务器）

本文档提供本项目在 Linux 服务器上的标准部署步骤，默认使用 Docker Compose，一次启动：

- `PostgreSQL`
- `FastAPI Backend`
- `Vue Frontend + Nginx`

## 1. 服务器准备

1. 安装 Docker 与 Compose 插件：

```bash
docker --version
docker compose version
```

如果命令不存在，请先安装 Docker Engine（Ubuntu 可使用官方安装脚本或 apt 仓库）。

2. 开放端口：

- `80/tcp`（前端与 API 对外入口）

## 2. 拉取代码

```bash
git clone <你的仓库地址> Gym_Mangement
cd Gym_Mangement
```

## 3. 按需修改配置

默认 `docker-compose.yml` 已包含可运行配置：

- PostgreSQL: `postgres/123456`
- DB 名称: `gym_management`
- 前端对外端口: `80`

建议上线前至少修改：

- `docker-compose.yml` 中 `db.environment.POSTGRES_PASSWORD`
- `docker-compose.yml` 中 `backend.environment.SECRET_KEY`

## 4. 构建并启动

```bash
docker compose up -d --build
```

## 5. 检查运行状态

```bash
docker compose ps
docker compose logs -f backend
```

验证：

- 前端首页：`http://<服务器IP>/`
- 健康检查：`http://<服务器IP>/api/v1/health`
- 后端文档：`http://<服务器IP>/docs`（由 Nginx 反代到 backend）

## 6. 常用运维命令

停止服务：

```bash
docker compose down
```

重启服务：

```bash
docker compose restart
```

更新代码后重建：

```bash
git pull
docker compose up -d --build
```

查看数据库容器日志：

```bash
docker compose logs -f db
```

## 7. 数据持久化说明

数据库使用命名卷：

- `pgdata:/var/lib/postgresql/data`

`docker compose down` 不会删除该卷；若需彻底删除数据：

```bash
docker compose down -v
```

## 8. 首次登录说明

系统没有内置固定管理员账号，请先在登录页注册。

注册完成后可直接登录，前端会初始化当前账号权限用于开发环境体验。
