#!/bin/bash
# build_index.sh — 重建 data/index.json 索引文件
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# 激活虚拟环境
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# 确保依赖已安装
uv sync --quiet 2>/dev/null || true

echo "=== 开始重建索引 ==="
PYTHONIOENCODING=utf-8 python -m src.validators.build_index "$@"
echo "=== 索引重建完成 ==="