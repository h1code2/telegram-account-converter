#!/bin/bash

# ========== 配置参数 ==========
APP_NAME="TelegramAccountConverter"
MAIN_SCRIPT="main.py"
ICON_FILE="telegram.icns"

# ========== 清理旧文件 ==========
echo "🧹 正在清理旧的构建文件..."
rm -rf ./dist ./build "$APP_NAME".spec
if [ -f "$APP_NAME.app" ]; then
    rm -rf "$APP_NAME.app"
fi

# ========== 检查依赖 ==========
echo "🔍 正在检查依赖..."
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller 未安装，请先运行: pip install pyinstaller"
    exit 1
fi

if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "❌ 主程序文件 $MAIN_SCRIPT 不存在！请确认路径是否正确。"
    exit 1
fi

if [ ! -f "$ICON_FILE" ]; then
    echo "⚠️ 图标文件 $ICON_FILE 不存在，将继续打包但不使用图标"
    ICON_FLAG=""
else
    ICON_FLAG="--icon=$ICON_FILE"
fi

# ========== 执行打包 ==========
echo "📦 开始打包应用程序..."
pyinstaller \
    --name="$APP_NAME" \
    --windowed \
    $ICON_FLAG \
    --add-data="gui.py:." \
    --add-data="converter.py:." \
    "$MAIN_SCRIPT"

# ========== 移动 .app 文件到当前目录 ==========
DIST_PATH="dist/$APP_NAME.app"
if [ -d "$DIST_PATH" ]; then
    echo "🚚 正在移动生成的 .app 文件到当前目录..."
    cp -R "$DIST_PATH" .
    echo "✅ 打包完成: $(pwd)/$APP_NAME.app"
    
    # 可选：自动打开应用
    echo "🚀 是否现在运行应用程序？(y/n)"
    read -r open_now
    if [[ "$open_now" == "y" || "$open_now" == "Y" ]]; then
        open "./$APP_NAME.app"
    fi
else
    echo "❌ 打包失败，未找到生成的 .app 文件"
    exit 1
fi