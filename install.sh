#!/usr/bin/env bash
set -e

# Legal Script Kit — 一键安装脚本
# 用法: bash install.sh

INSTALL_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
REPO_URL="https://github.com/lebiai/legal-script-kit.git"
TMP_DIR=$(mktemp -d)

echo "📦 正在下载 legal-script-kit..."
git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>/dev/null

echo "📂 安装到 $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
# 这个 repo 的 SKILL.md 在根目录，整体作为一个 skill
SKILL_NAME="legal-script-kit"
rsync -a --exclude='.git' "$TMP_DIR/" "$INSTALL_DIR/$SKILL_NAME/"
rm -rf "$TMP_DIR"

echo ""
echo "✅ 安装完成！已安装：$SKILL_NAME"
echo "   $INSTALL_DIR/$SKILL_NAME/SKILL.md"
echo ""
echo "💡 重启 Codex 后即可使用。"
echo ""
echo "🔄 后续更新："
echo "   cd $INSTALL_DIR/$SKILL_NAME && git pull"
