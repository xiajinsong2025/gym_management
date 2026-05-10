#!/bin/bash

# 快速启动脚本（前台运行，适合开发调试）
# 用途：在一个终端窗口中同时运行后端和前端

set -e

PROJECT_ROOT="/Users/xiajingsong/Documents/code/Gym_Mangement"
BACKEND_DIR="$PROJECT_ROOT"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo "🚀 启动健身房管理系统（开发模式）"
echo

# 启动后端（后台）
echo "启动后端服务..."
cd "$BACKEND_DIR"
.venv/bin/uvicorn app.main:app --reload --app-dir backend &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端（前台）
echo "启动前端服务..."
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!

echo
echo "✅ 服务已启动！"
echo
echo "访问地址："
echo "  前端: http://localhost:3000"
echo "  后端: http://127.0.0.1:8000"
echo "  API文档: http://127.0.0.1:8000/docs"
echo
echo "按 Ctrl+C 停止所有服务"
echo

# 捕获中断信号，停止所有服务
trap "echo '\n停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# 等待
wait