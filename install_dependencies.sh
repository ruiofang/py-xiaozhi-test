#!/bin/bash

# 小智助手依赖安装脚本
# 适用于 Ubuntu/Debian 系统

set -e  # 遇到错误时停止执行

echo "========================================="
echo "小智助手依赖安装脚本"
echo "========================================="

# 检查是否为 root 用户或具有 sudo 权限
if ! command -v sudo &> /dev/null && [ "$EUID" -ne 0 ]; then
    echo "错误: 需要 sudo 权限或 root 用户来安装依赖"
    exit 1
fi

echo "正在更新软件包列表..."
sudo apt-get update

echo "正在安装系统依赖..."

# 基础开发工具
sudo apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    git

# Python 相关依赖
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv

# 音频处理依赖
sudo apt-get install -y \
    libportaudio2 \
    portaudio19-dev \
    libasound2-dev \
    libpulse-dev \
    libsndfile1-dev

# # Qt/GUI 相关依赖 (如果需要图形界面)
# sudo apt-get install -y \
#     qt6-base-dev \
#     qt6-declarative-dev \
#     qt6-multimedia-dev \
#     libqt6multimedia6 \
#     qml6-module-qtquick \
#     qml6-module-qtquick-controls \
#     qml6-module-qtquick-layouts

# 网络和通信依赖
sudo apt-get install -y \
    libssl-dev \
    libffi-dev \
    curl \
    wget

# MQTT 客户端工具 (可选)
#sudo apt-get install -y mosquitto-clients

# 其他可能需要的依赖
sudo apt-get install -y \
    ffmpeg \
    libopus-dev \
    libopus0

echo "========================================="
echo "系统依赖安装完成!"
echo "========================================="

# 检查 Python 环境
echo "检查 Python 环境..."
python3 --version
pip3 --version

echo "建议接下来运行以下命令安装 Python 依赖:"
echo "pip3 install -r requirements.txt"

echo "========================================="
echo "安装脚本执行完成!"
echo "========================================="