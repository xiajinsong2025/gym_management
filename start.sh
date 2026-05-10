#!/bin/bash

# 健身房管理系统启动脚本
# 用途：一键启动后端和前端服务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="/Users/xiajingsong/Documents/code/Gym_Mangement"
BACKEND_DIR="$PROJECT_ROOT"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# 日志文件
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"
BACKEND_LOG="$LOG_DIR/backend.log"
FRONTEND_LOG="$LOG_DIR/frontend.log"

# PID 文件
PID_DIR="$PROJECT_ROOT/.pids"
mkdir -p "$PID_DIR"
BACKEND_PID_FILE="$PID_DIR/backend.pid"
FRONTEND_PID_FILE="$PID_DIR/frontend.pid"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # 端口被占用
    else
        return 1  # 端口空闲
    fi
}

# 等待端口就绪
wait_for_port() {
    local port=$1
    local service=$2
    local max_attempts=30
    local attempt=1

    print_info "等待 $service 启动 (端口 $port)..."

    while [ $attempt -le $max_attempts ]; do
        if check_port $port; then
            print_success "$service 已启动 (端口 $port)"
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
    done

    print_error "$service 启动超时"
    return 1
}

# 启动后端
start_backend() {
    print_info "启动后端服务..."

    # 检查端口
    if check_port 8000; then
        print_warning "端口 8000 已被占用"
        read -p "是否停止现有服务并重启？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            stop_backend
        else
            print_info "跳过后端启动"
            return 0
        fi
    fi

    cd "$BACKEND_DIR"

    # 检查虚拟环境
    if [ ! -d ".venv" ]; then
        print_error "虚拟环境不存在，请先运行: uv install"
        exit 1
    fi

    # 启动后端（后台运行）
    nohup .venv/bin/uvicorn app.main:app --reload --app-dir backend > "$BACKEND_LOG" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$BACKEND_PID_FILE"

    print_info "后端 PID: $BACKEND_PID"

    # 等待启动
    if wait_for_port 8000 "后端"; then
        print_success "后端服务已启动"
        print_info "API 地址: http://127.0.0.1:8000"
        print_info "API 文档: http://127.0.0.1:8000/docs"
    else
        print_error "后端启动失败，请查看日志: $BACKEND_LOG"
        exit 1
    fi
}

# 启动前端
start_frontend() {
    print_info "启动前端服务..."

    # 检查端口
    if check_port 3000; then
        print_warning "端口 3000 已被占用"
        read -p "是否停止现有服务并重启？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            stop_frontend
        else
            print_info "跳过前端启动"
            return 0
        fi
    fi

    cd "$FRONTEND_DIR"

    # 检查 node_modules
    if [ ! -d "node_modules" ]; then
        print_warning "依赖未安装，正在安装..."
        npm install
    fi

    # 启动前端（后台运行）
    nohup npm run dev > "$FRONTEND_LOG" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$FRONTEND_PID_FILE"

    print_info "前端 PID: $FRONTEND_PID"

    # 等待启动
    if wait_for_port 3000 "前端"; then
        print_success "前端服务已启动"
        print_info "前端地址: http://localhost:3000"
    else
        print_error "前端启动失败，请查看日志: $FRONTEND_LOG"
        exit 1
    fi
}

# 停止后端
stop_backend() {
    print_info "停止后端服务..."

    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill $BACKEND_PID
            print_success "后端服务已停止 (PID: $BACKEND_PID)"
        fi
        rm -f "$BACKEND_PID_FILE"
    fi

    # 确保端口释放
    if check_port 8000; then
        lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    fi
}

# 停止前端
stop_frontend() {
    print_info "停止前端服务..."

    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill $FRONTEND_PID
            print_success "前端服务已停止 (PID: $FRONTEND_PID)"
        fi
        rm -f "$FRONTEND_PID_FILE"
    fi

    # 确保端口释放
    if check_port 3000; then
        lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    fi
}

# 查看状态
show_status() {
    print_info "服务状态："
    echo

    # 后端状态
    if check_port 8000; then
        print_success "后端: 运行中 (http://127.0.0.1:8000)"
        if [ -f "$BACKEND_PID_FILE" ]; then
            echo "  PID: $(cat $BACKEND_PID_FILE)"
        fi
    else
        print_warning "后端: 未运行"
    fi

    # 前端状态
    if check_port 3000; then
        print_success "前端: 运行中 (http://localhost:3000)"
        if [ -f "$FRONTEND_PID_FILE" ]; then
            echo "  PID: $(cat $FRONTEND_PID_FILE)"
        fi
    else
        print_warning "前端: 未运行"
    fi
}

# 查看日志
show_logs() {
    print_info "日志文件位置："
    echo "  后端日志: $BACKEND_LOG"
    echo "  前端日志: $FRONTEND_LOG"
    echo

    if [ "$1" == "backend" ]; then
        print_info "后端日志 (Ctrl+C 退出):"
        tail -f "$BACKEND_LOG"
    elif [ "$1" == "frontend" ]; then
        print_info "前端日志 (Ctrl+C 退出):"
        tail -f "$FRONTEND_LOG"
    else
        print_info "使用方法: $0 logs [backend|frontend]"
    fi
}

# 显示帮助
show_help() {
    echo "健身房管理系统启动脚本"
    echo
    echo "使用方法:"
    echo "  $0 start       启动所有服务"
    echo "  $0 stop        停止所有服务"
    echo "  $0 restart     重启所有服务"
    echo "  $0 status      查看服务状态"
    echo "  $0 logs        查看日志文件位置"
    echo "  $0 logs backend     查看后端日志"
    echo "  $0 logs frontend   查看前端日志"
    echo "  $0 help        显示帮助信息"
    echo
    echo "示例:"
    echo "  $0 start       # 启动后端和前端"
    echo "  $0 status       # 查看运行状态"
    echo "  $0 stop         # 停止所有服务"
}

# 主函数
main() {
    case "${1:-}" in
        start)
            print_info "启动健身房管理系统..."
            start_backend
            start_frontend
            print_success "所有服务已启动！"
            echo
            print_info "访问地址："
            echo "  前端: http://localhost:3000"
            echo "  后端: http://127.0.0.1:8000"
            echo "  API文档: http://127.0.0.1:8000/docs"
            echo
            print_info "停止服务: $0 stop"
            print_info "查看状态: $0 status"
            ;;
        stop)
            print_info "停止健身房管理系统..."
            stop_frontend
            stop_backend
            print_success "所有服务已停止"
            ;;
        restart)
            print_info "重启健身房管理系统..."
            $0 stop
            sleep 2
            $0 start
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs "${2:-}"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令: ${1:-}"
            echo
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
