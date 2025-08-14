#!/bin/bash

# ACEP HIPAA AUDIT ASSISTANT - Quick Launcher
# Created by Chaitanya Eshwar Prasad

echo "🏥 Starting ACEP HIPAA AUDIT ASSISTANT..."

# Check if virtual environment exists
if [ ! -d "acep_hipaa_venv" ]; then
    echo "❌ Virtual environment not found. Please run the setup script first."
    echo "   Run: ./acep_hipaa_auto_setup.sh"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source acep_hipaa_venv/bin/activate

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please ensure you're in the correct directory."
    exit 1
fi

# Start the application
echo "🚀 Starting HIPAA Audit Assistant..."
echo "📱 Access the application at: http://localhost:5000"
echo "🔑 Default credentials: acep / acep123"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

python3 app.py
