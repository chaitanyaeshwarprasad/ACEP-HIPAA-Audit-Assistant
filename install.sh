#!/bin/bash

# ACEP HIPAA AUDIT ASSISTANT - Complete Installation Script
# Created by Chaitanya Eshwar Prasad
# This script handles everything: system setup, Python installation, and app setup

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ACEP HIPAA Audit Assistant                ║"
echo "║                 Complete Installation Script                 ║"
echo "║                                                              ║"
echo "║  This script will automatically:                             ║"
echo "║  1. Install system dependencies                              ║"
echo "║  2. Install Python if needed                                 ║"
echo "║  3. Clone the repository                                     ║"
echo "║  4. Set up the environment                                   ║"
echo "║  5. Install Python dependencies                              ║"
echo "║  6. Launch the application                                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_warning "This script should not be run as root. Please run as a regular user."
   exit 1
fi

# Detect OS and package manager
print_step "Step 1: Detecting operating system and package manager..."
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
    print_status "Detected OS: $OS $VER"
else
    print_error "Cannot detect OS. This script is designed for Linux distributions."
    exit 1
fi

# Determine package manager
if command -v apt &> /dev/null; then
    PKG_MANAGER="apt"
    PKG_INSTALL="sudo apt install -y"
    PKG_UPDATE="sudo apt update"
    PYTHON_PKG="python3 python3-pip python3-venv python3-dev"
elif command -v yum &> /dev/null; then
    PKG_MANAGER="yum"
    PKG_INSTALL="sudo yum install -y"
    PKG_UPDATE="sudo yum update -y"
    PYTHON_PKG="python3 python3-pip python3-venv python3-devel"
elif command -v dnf &> /dev/null; then
    PKG_MANAGER="dnf"
    PKG_INSTALL="sudo dnf install -y"
    PKG_UPDATE="sudo dnf update -y"
    PYTHON_PKG="python3 python3-pip python3-venv python3-devel"
else
    print_error "No supported package manager found. Please install Python 3.8+ manually."
    exit 1
fi

print_success "Package manager detected: $PKG_MANAGER"

# Install system dependencies
print_step "Step 2: Installing system dependencies..."
print_status "Updating package lists..."
$PKG_UPDATE

print_status "Installing system packages..."
$PKG_INSTALL $PYTHON_PKG git sqlite3 curl wget

# Check if Python 3 is installed and get version
print_step "Step 3: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Found Python $PYTHON_VERSION"
    
    # Check if version is 3.8 or higher
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        print_success "Python version is compatible (3.8+)"
    else
        print_warning "Python version $PYTHON_VERSION is below 3.8. Attempting to install newer version..."
        if [[ "$PKG_MANAGER" == "apt" ]]; then
            sudo add-apt-repository ppa:deadsnakes/ppa -y
            $PKG_UPDATE
            $PKG_INSTALL python3.9 python3.9-pip python3.9-venv python3.9-dev
            # Create symlink for python3
            sudo ln -sf /usr/bin/python3.9 /usr/bin/python3
        else
            print_error "Please install Python 3.8+ manually for your distribution."
            exit 1
        fi
    fi
else
    print_error "Python 3 is not installed. Please install Python 3.8+ manually."
    exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Installing git..."
    $PKG_INSTALL git
fi

print_success "System dependencies installed successfully!"

# Clone repository (if not already in the directory)
print_step "Step 4: Setting up repository..."
if [ ! -f "app.py" ] || [ ! -f "requirements.txt" ]; then
    print_status "Repository not found. Cloning from GitHub..."
    
    # Get the current directory name
    CURRENT_DIR=$(basename "$PWD")
    
    if [ "$CURRENT_DIR" = "ACEP-HIPAA-Audit-Assistant" ]; then
        print_warning "Already in ACEP-HIPAA-Audit-Assistant directory. Skipping clone."
    else
        # Clone to a new directory
        git clone https://github.com/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant.git
        cd ACEP-HIPAA-Audit-Assistant
        print_success "Repository cloned successfully!"
    fi
else
    print_success "Already in ACEP-HIPAA-Audit-Assistant directory. Skipping clone."
fi

# Environment Setup
print_step "Step 5: Setting up Python environment..."

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

# Install Python requirements
print_step "Step 6: Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    print_status "Installing Python packages..."
    pip install -r requirements.txt
    print_success "Python dependencies installed successfully."
else
    print_error "requirements.txt not found. Please ensure you're in the correct directory."
    exit 1
fi

# Setup Application
print_step "Step 7: Setting up application..."

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
echo "║                    INSTALLATION COMPLETED SUCCESSFULLY!     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

print_success "ACEP HIPAA AUDIT ASSISTANT is ready to use!"
echo ""

# Launch Application
print_step "Step 8: Launching application..."
print_success "Installation completed! Launching ACEP HIPAA Audit Assistant..."
echo ""
echo "🚀 The application will start in 3 seconds..."
echo "📱 Access at: http://localhost:5000"
echo "🔑 Login: acep / acep123"
echo ""

sleep 3

# Clean up virtual environment activation for the run script
deactivate

# Launch the application
./run_acep_hipaa.sh
