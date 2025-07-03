#!/bin/bash

# Infrastructure Issue Reporter - Linux/macOS Setup Script
# This script automates the setup process for Unix-like systems

set -e  # Exit on any error

echo "========================================"
echo "Infrastructure Issue Reporter Setup"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  macOS: brew install python"
    exit 1
fi

print_status "Python found: $(python3 --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed"
    echo "Please install pip3:"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3-pip"
    echo "  macOS: pip3 should be included with Python"
    exit 1
fi

print_status "pip found: $(pip3 --version)"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found"
    echo "Please run this script from the infrastructure-reporter directory"
    exit 1
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create uploads directory
print_status "Creating uploads directory..."
mkdir -p src/static/uploads

# Set proper permissions
print_status "Setting directory permissions..."
chmod 755 src/static/uploads

# Create demo data
print_status "Creating demo data and admin user..."
python create_demo_data.py

echo
echo "========================================"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo "========================================"
echo
echo "Admin Login Credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start application: python src/main.py"
echo "  3. Open browser to: http://localhost:5001"
echo
echo "For network access and production deployment, see DEPLOYMENT.md"
echo

# Ask if user wants to start the application now
read -p "Start the application now? (y/n): " start_now
if [[ $start_now =~ ^[Yy]$ ]]; then
    echo
    print_status "Starting Infrastructure Issue Reporter..."
    echo "Press Ctrl+C to stop the application"
    echo
    python src/main.py
fi

