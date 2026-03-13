#!/bin/bash
# 清理并选择性上传文件到GitHub

set -e

echo "🧹 清理Git仓库并选择性上传..."

# 检查Git仓库状态
if [ ! -d ".git" ]; then
    echo "❌ 不是Git仓库，请先运行初始化"
    exit 1
fi

# 停止追踪所有文件，重新开始
echo "🔄 重置Git仓库..."
rm -rf .git
git init

# 配置SSH远程仓库
SSH_URL="git@github.com:AMDvsTMD/bank-stock-analysis.git"
git remote add origin "$SSH_URL"

# 添加.gitignore
echo "📋 添加.gitignore文件..."
git add .gitignore

# 核心文件列表
CORE_FILES=(
    "bank_stock_dividend_analysis.py"
    "README.md"
    "公众号文章_Python分析银行股分红.md"
    "示例数据说明.md"
)

# 添加核心文件
echo "➕ 添加核心文件..."
for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
        git add "$file"
    else
        echo "  ✗ $file (未找到)"
    fi
done

# 添加二维码（如果存在）
if [ -f "qrcode.jpg" ]; then
    echo "  ✓ qrcode.jpg"
    git add qrcode.jpg
elif [ -f "qrcode.png" ]; then
    echo "  ✓ qrcode.png"
    git add qrcode.png
else
    echo "  ⚠️  未找到二维码文件"
fi

# 提交
echo "💾 提交更改..."
git commit -m "更新：银行股分红分析工具 v1.0

包含：
- 核心Python分析脚本
- 完整的README文档
- 公众号教程文章
- 示例数据说明
- 公众号二维码

移除了临时和不相关文件"

# 强制推送到GitHub（覆盖历史）
echo "🚀 推送到GitHub..."
git branch -M main
git push -u origin main --force

echo ""
echo "✅ 清理上传完成！"
echo "🌐 仓库地址：https://github.com/AMDvsTMD/bank-stock-analysis"
echo ""
echo "📋 上传的文件："
git ls-files | while read file; do
    echo "  • $file"
done
echo ""
echo "⚠️  注意：本次使用了 --force 推送，覆盖了远程仓库历史"
echo "📁 未上传的辅助文件："
find . -maxdepth 1 -type f -name "*.sh" -o -name "*.md" ! -name "README.md" ! -name "示例数据说明.md" ! -name "公众号文章_Python分析银行股分红.md" 2>/dev/null | grep -v ".git" | while read file; do
    if [ "$file" != "./.gitignore" ] && ! git ls-files --error-unmatch "$file" >/dev/null 2>&1; then
        echo "  • $(basename "$file")"
    fi
done