#!/bin/bash
# setup.sh — 初始化 cs-pro-data 开发环境
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== 初始化 CS 职业选手资料库 ==="

cd "$PROJECT_DIR"

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo ">>> 创建 Python 虚拟环境..."
    uv venv .venv
fi

# 激活虚拟环境
source .venv/Scripts/activate

# 安装依赖
echo ">>> 安装项目依赖..."
uv sync

# 创建日志目录
mkdir -p logs

echo "=== 初始化完成 ==="
echo "运行校验: bash scripts/validate.sh"