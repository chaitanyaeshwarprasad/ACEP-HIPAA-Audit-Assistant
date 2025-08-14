#!/bin/bash

# ACEP HIPAA AUDIT ASSISTANT - Automated Setup Script
# Created by Chaitanya Eshwar Prasad
# This script automates the setup of the HIPAA Audit Assistant on Kali Linux

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ACEP HIPAA Audit Assistant                ║"
echo "║                 Automated Setup Script                       ║"
echo "║                                                              ║"
echo "║  Built for healthcare compliance professionals               ║"
echo "║  HIPAA Security Rule compliance made simple                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

print_status "Starting automated setup for ACEP HIPAA AUDIT ASSISTANT..."

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_warning "This script should not be run as root. Please run as a regular user."
   exit 1
fi

# Detect OS
print_status "Detecting operating system..."
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    print_error "Cannot detect OS. This script is designed for Kali Linux."
    exit 1
fi

print_status "Detected OS: $OS $VER"

# Check if it's Kali Linux
if [[ "$OS" != *"Kali"* ]]; then
    print_warning "This script is optimized for Kali Linux. Other distributions may work but are not tested."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Python version
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Found Python $PYTHON_VERSION"
    
    # Check if version is 3.8 or higher
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        print_success "Python version is compatible (3.8+)"
    else
        print_error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment already exists
if [ -d "acep_hipaa_venv" ]; then
    print_warning "Virtual environment 'acep_hipaa_venv' already exists."
    read -p "Remove existing virtual environment and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Removing existing virtual environment..."
        rm -rf acep_hipaa_venv
        print_success "Existing virtual environment removed."
    else
        print_status "Using existing virtual environment..."
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "acep_hipaa_venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv acep_hipaa_venv
    print_success "Virtual environment created successfully."
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source acep_hipaa_venv/bin/activate
print_success "Virtual environment activated."

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip
print_success "Pip upgraded successfully."

# Install system dependencies (for Kali Linux)
print_status "Installing system dependencies..."
if command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y python3-dev python3-pip python3-venv sqlite3
    print_success "System dependencies installed."
else
    print_warning "Package manager 'apt' not found. Please install required dependencies manually."
fi

# Install Python requirements
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Python dependencies installed successfully."
else
    print_error "requirements.txt not found. Please ensure you're in the correct directory."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p database
mkdir -p static/uploads
mkdir -p static/css
mkdir -p static/js
mkdir -p templates
print_success "Directories created successfully."

# Set proper permissions
print_status "Setting file permissions..."
chmod +x run_acep_hipaa.sh
chmod -R 755 .
print_success "Permissions set successfully."

# Test the application
print_status "Testing the application..."
if python3 -c "import flask; print('Flask imported successfully')" 2>/dev/null; then
    print_success "Flask dependency test passed."
else
    print_error "Flask dependency test failed."
    exit 1
fi

# Create quick launcher script
print_status "Creating quick launcher script..."
cat > run_acep_hipaa.sh << 'EOF'
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
EOF

chmod +x run_acep_hipaa.sh
print_success "Quick launcher script created."

# Final setup test
print_status "Running final setup test..."
if python3 -c "
import sys
sys.path.insert(0, '.')
try:
    import app
    print('✅ Application import test passed')
except Exception as e:
    print(f'❌ Application import test failed: {e}')
    sys.exit(1)
" 2>/dev/null; then
    print_success "Final setup test passed."
else
    print_error "Final setup test failed. Please check the error messages above."
    exit 1
fi

# Success message
echo ""
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    SETUP COMPLETED SUCCESSFULLY!            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

print_success "ACEP HIPAA AUDIT ASSISTANT is ready to use!"
echo ""
echo "🚀 To start the application, run:"
echo "   ./run_acep_hipaa.sh"
echo ""
echo "🌐 Access the application at: http://localhost:5000"
echo "🔑 Default login credentials: acep / acep123"
echo ""
echo "📚 For more information, see README.md"
echo ""
echo "🏥 Happy HIPAA auditing!"

# Clean up
deactivate

echo ""
print_status "Setup completed! You can now run the application."
