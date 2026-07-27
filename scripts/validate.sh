#!/bin/bash
# validate.sh — 校验所有数据文件的格式和一致性
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

echo "=== 开始数据校验 ==="
PYTHONIOENCODING=utf-8 python -m src.validators.validate_all "$@"
echo "=== 校验完成 ==="