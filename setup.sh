#!/bin/bash

# ACEP HIPAA AUDIT ASSISTANT - Complete Setup & Launch Script
# Created by Chaitanya Eshwar Prasad
# This script handles everything: cloning, setup, and launching

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
echo "║                 Complete Setup & Launch Script               ║"
echo "║                                                              ║"
echo "║  This script will automatically:                             ║"
echo "║  1. Clone the repository                                     ║"
echo "║  2. Set up the environment                                   ║"
echo "║  3. Install dependencies                                     ║"
echo "║  4. Launch the application                                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_warning "This script should not be run as root. Please run as a regular user."
   exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    print_status "On Ubuntu/Debian/Kali: sudo apt install git"
    print_status "On CentOS/RHEL: sudo yum install git"
    print_status "On macOS: brew install git"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    print_status "On Ubuntu/Debian/Kali: sudo apt install python3 python3-pip python3-venv"
    print_status "On CentOS/RHEL: sudo yum install python3 python3-pip python3-venv"
    print_status "On macOS: brew install python3"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

print_success "System requirements check passed! Python $PYTHON_VERSION detected."

# Step 1: Clone Repository (if not already in the directory)
print_step "Step 1: Setting up repository..."
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

# Step 2: Environment Setup
print_step "Step 2: Setting up Python environment..."

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

# Step 3: Install Dependencies
print_step "Step 3: Installing dependencies..."

# Install system dependencies (for Linux)
if command -v apt &> /dev/null; then
    print_status "Installing system dependencies (Ubuntu/Debian/Kali)..."
    sudo apt update
    sudo apt install -y python3-dev python3-pip python3-venv sqlite3
    print_success "System dependencies installed."
elif command -v yum &> /dev/null; then
    print_status "Installing system dependencies (CentOS/RHEL)..."
    sudo yum install -y python3-devel python3-pip python3-venv sqlite
    print_success "System dependencies installed."
elif command -v dnf &> /dev/null; then
    print_status "Installing system dependencies (Fedora)..."
    sudo dnf install -y python3-devel python3-pip python3-venv sqlite
    print_success "System dependencies installed."
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

# Step 4: Setup Application
print_step "Step 4: Setting up application..."

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
echo "║                    SETUP COMPLETED SUCCESSFULLY!            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

print_success "ACEP HIPAA AUDIT ASSISTANT is ready to use!"
echo ""

# Step 5: Launch Application
print_step "Step 5: Launching application..."
print_success "Setup completed! Launching ACEP HIPAA Audit Assistant..."
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
