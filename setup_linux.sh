#!/bin/bash

echo "🏥 Setting up ACEP HIPAA AUDIT ASSISTANT for Linux..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "acep_hipaa_venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv acep_hipaa_venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source acep_hipaa_venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install system dependencies for python-magic (if available)
if command -v apt-get &> /dev/null; then
    echo "📦 Installing system dependencies (Ubuntu/Debian)..."
    sudo apt-get update
    sudo apt-get install -y libmagic1 python3-dev
elif command -v yum &> /dev/null; then
    echo "📦 Installing system dependencies (CentOS/RHEL)..."
    sudo yum install -y file-devel python3-devel
elif command -v dnf &> /dev/null; then
    echo "📦 Installing system dependencies (Fedora)..."
    sudo dnf install -y file-devel python3-devel
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup completed successfully!"
echo "🚀 To run the application:"
echo "   source acep_hipaa_venv/bin/activate"
echo "   python app.py"
echo ""
echo "📱 Access the application at: http://localhost:5000"
echo "🔑 Default credentials: acep / acep123"
