#!/bin/bash
# scrape.sh — 从 Liquipedia 爬取选手数据
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

if [ $# -eq 0 ]; then
    echo "用法: bash scripts/scrape.sh <player_id> [player_id ...]"
    echo "示例: bash scripts/scrape.sh s1mple zywoo donk"
    exit 1
fi

echo "=== 开始爬取选手数据 ==="
PYTHONIOENCODING=utf-8 python -m src.scrapers.liquipedia "$@"
echo "=== 爬取完成 ==="