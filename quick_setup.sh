#!/bin/bash

# ACEP HIPAA AUDIT ASSISTANT - Quick One-Command Setup
# Created by Chaitanya Eshwar Prasad
# This script automates the entire setup process

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
echo "║                 Quick One-Command Setup                      ║"
echo "║                                                              ║"
echo "║  This script will automatically:                             ║"
echo "║  1. Clone the repository                                     ║"
echo "║  2. Make scripts executable                                  ║"
echo "║  3. Run automated setup                                      ║"
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
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

print_success "System requirements check passed!"

# Step 1: Clone Repository (if not already in the directory)
if [ ! -f "app.py" ] || [ ! -f "requirements.txt" ]; then
    print_status "Step 1: Cloning repository..."
    
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

# Step 2: Make Scripts Executable
print_status "Step 2: Making scripts executable..."
chmod +x acep_hipaa_auto_setup.sh run_acep_hipaa.sh setup_linux.sh
print_success "Scripts made executable!"

# Step 3: Run Automated Setup
print_status "Step 3: Running automated setup..."
./acep_hipaa_auto_setup.sh

# Step 4: Launch Application
print_status "Step 4: Launching application..."
print_success "Setup completed! Launching ACEP HIPAA Audit Assistant..."
echo ""
echo "🚀 The application will start in 3 seconds..."
echo "📱 Access at: http://localhost:5000"
echo "🔑 Login: acep / acep123"
echo ""

sleep 3

# Launch the application
./run_acep_hipaa.sh
