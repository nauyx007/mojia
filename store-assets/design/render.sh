#!/bin/zsh
# macOS / Linux 下的便捷入口，实际渲染逻辑在 render.py。
# 用法：zsh store-assets/design/render.sh
set -e
cd "${0:A:h}"
python3 render.py
