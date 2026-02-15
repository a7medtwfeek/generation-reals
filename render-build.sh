#!/usr/bin/env bash
# Render build script

echo "🔧 Installing system dependencies..."

# Update package list
apt-get update

# Install FFmpeg (already available on Render)
echo "✅ FFmpeg is pre-installed on Render"

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build completed successfully!"
