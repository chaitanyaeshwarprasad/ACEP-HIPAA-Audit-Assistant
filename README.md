# 🏥 ACEP HIPAA Audit Assistant

<div align="center">

![ACEP HIPAA](https://img.shields.io/badge/ACEP-HIPAA%20Audit%20Assistant-blue?style=for-the-badge&logo=shield-check&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3+-red?style=for-the-badge&logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple?style=for-the-badge&logo=bootstrap&logoColor=white)

**Professional Healthcare Compliance & HIPAA Security Rule Assessment Tool**

*Created by A Chaitanya Eshwar Prasad*  
*Built for healthcare professionals, by cybersecurity professionals.*

[![Website](https://img.shields.io/badge/🌐_Website-chaitanyaeshwarprasad.com-blue?style=for-the-badge&logo=globe&logoColor=white)](https://chaitanyaeshwarprasad.com)
[![LinkedIn](https://img.shields.io/badge/💼_LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/chaitanya-eshwar-prasad)
[![GitHub](https://img.shields.io/badge/🐙_GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/chaitanyaeshwarprasad)

</div>

---

## 🎯 **Project Overview**

The **ACEP HIPAA Audit Assistant** is a comprehensive, healthcare compliance management system designed to streamline and automate HIPAA Security Rule assessments. Built with modern web technologies and a focus on user experience, this tool empowers healthcare organizations to achieve and maintain full HIPAA compliance through systematic evaluation, evidence management, and risk assessment.

### **🌟 Why Choose ACEP HIPAA Audit Assistant?**

- **🔒 Complete HIPAA Coverage** - All 18 Security Rule standards comprehensively addressed
- **🏢 Enterprise-Ready** - Professional interface suitable for healthcare organizations of all sizes
- **⚡ Automated Workflows** - Streamlined processes that save time and reduce human error
- **📱 Modern Interface** - Responsive design that works on all devices and platforms
- **🛡️ Security-First** - Built with cybersecurity best practices and HIPAA compliance in mind
- **📊 Real-Time Analytics** - Live compliance status and progress tracking
- **🔍 Evidence Management** - Centralized storage and organization of compliance documentation

---

## ⚙️ **System Requirements**

### **🖥️ Operating System**
- **Primary**: Kali Linux 2023.3+ (Recommended for cybersecurity professionals)
- **Alternative**: Ubuntu 20.04+, Debian 11+, CentOS 8+
- **Windows**: WSL2 with Ubuntu/Kali Linux
- **macOS**: Native support with Homebrew

### **🐍 Python Requirements**
- **Python**: 3.8+ (3.9+ Recommended for optimal performance)
- **pip**: Latest version for dependency management
- **Virtual Environment**: Highly recommended for production use

### **💾 System Resources**
- **RAM**: Minimum 2GB, Recommended 4GB+ for large datasets
- **Storage**: 500MB free space for application and database
- **Network**: Internet access for initial setup and updates
- **Browser**: Modern browser with JavaScript enabled

---

## 🔧 **Installation & Setup**

### **🚀 Quick Start Guide**

#### **Step 1: Clone Repository**
```bash
# Clone the repository
git clone https://github.com/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant.git

# Navigate to project directory
cd ACEP-HIPAA-Audit-Assistant
```

#### **Step 2: Permissions**
```bash
./chmod +x run_acep_hipaa.sh install.sh
```

#### **Step 3: **Permissions**
```bash
./install.sh
```

#### **Step 4: **Run Application**
```bash
./run_acep_hipaa.sh
```

**What you'll get:**
- ✅ Complete HIPAA compliance tool
- ✅ Professional web interface
- ✅ All dependencies installed automatically
- ✅ Application running and ready to use
- ✅ Access at http://localhost:5000
- ✅ Default login: `acep` / `acep123`

---

### **⚡ Quick Reference - Get Running in 10 Seconds**

**Already installed? Just run:**
```bash
./run_acep_hipaa.sh
```

**Need to install? One command:**
```bash
curl -sSL https://raw.githubusercontent.com/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant/main/install.sh | bash
```

**Access at:** http://localhost:5000  
**Login:** `acep` / `acep123`

---

### **📥 Method 1: One-Command Setup (Recommended - Super Easy!)**

#### **🚀 Quick Start (Linux/macOS)**
```bash
# Download and run everything in one command
curl -sSL https://raw.githubusercontent.com/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant/main/install.sh | bash
```

#### **📥 Alternative Download Method**
```bash
# Download the installation script first
wget https://raw.githubusercontent.com/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant/main/install.sh

# Make it executable and run
chmod +x install.sh
./install.sh
```

#### **🎯 What Happens Automatically:**
1. ✅ **System Check** - Detects your operating system and package manager
2. ✅ **Dependencies** - Installs system packages (git, python3, pip, etc.)
3. ✅ **Python Setup** - Installs Python 3.8+ if needed
4. ✅ **Repository Setup** - Clones from GitHub (if needed)
5. ✅ **Environment Setup** - Creates Python virtual environment
6. ✅ **Package Installation** - Installs all required Python packages
7. ✅ **Configuration** - Sets up directories, permissions, and database
8. ✅ **Testing & Validation** - Verifies everything works correctly
9. ✅ **Launch** - Starts the application automatically

**🎉 That's it! One command gets everything running.**

#### **🔍 Installation Details:**
- **Time**: Usually 2-5 minutes depending on your system
- **Internet**: Requires stable internet connection for downloads
- **Permissions**: May ask for sudo/admin privileges for system packages
- **Storage**: Uses approximately 500MB of disk space
- **Memory**: Requires 2GB+ RAM during installation

#### **📋 What You Get After Installation:**
- **`install.sh`** - Comprehensive setup script for future use
- **`run_acep_hipaa.sh`** - Easy launcher script to start the application
- **`requirements.txt`** - Python dependencies list
- **`app.py`** - Main Flask application
- **Complete web interface** - Ready to use at http://localhost:5000

---

### **📥 Method 2: Manual Setup (Advanced Users)**

#### **Step 1: Clone Repository**
```bash
# Clone the repository
git clone https://github.com/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant.git

# Navigate to project directory
cd ACEP-HIPAA-Audit-Assistant
```

#### **Step 2: Run Installation Script**
```bash
# Make installation script executable
chmod +x install.sh

# Run the comprehensive installation
./install.sh
```

**🔧 The installation script handles everything else automatically!**

---

### **📥 Method 3: Manual Setup (Expert Users)**

#### **Step 1: Install System Dependencies**
```bash
# Ubuntu/Debian/Kali Linux
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git sqlite3 curl wget

# CentOS/RHEL/Fedora
sudo yum install -y python3 python3-pip python3-venv git sqlite3 curl wget
# OR for newer systems
sudo dnf install -y python3 python3-pip python3-venv git sqlite3 curl wget

# macOS (using Homebrew)
brew install python3 git sqlite3 curl wget
```

#### **Step 2: Install Python Dependencies**
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

#### **Step 3: Run Application**
```bash
python app.py
```

---

### **🌐 Cross-Platform Compatibility**

#### **✅ Supported Operating Systems:**
- **Linux**: Ubuntu 18.04+, Debian 10+, Kali Linux, CentOS 7+, RHEL 7+
- **macOS**: 10.15+ (Catalina and newer)
- **Windows**: Windows 10+ with WSL2 (Windows Subsystem for Linux)

#### **🐍 Python Requirements:**
- **Minimum**: Python 3.8
- **Recommended**: Python 3.9 - 3.11
- **Latest**: Python 3.12+ (fully supported)

#### **💻 System Requirements:**
- **RAM**: 2GB minimum, 4GB+ recommended
- **Storage**: 500MB free space
- **Network**: Internet connection for setup
- **Browser**: Modern browser with JavaScript enabled

---

### **🔧 Post-Installation**

#### **🚀 Starting the Application:**

**Option 1: Using the Launcher Script (Recommended)**
```bash
# Make the launcher script executable
chmod +x run_acep_hipaa.sh

# Start the application
./run_acep_hipaa.sh
```

**Option 2: Manual Start**
```bash
# If using the install script, it starts automatically
# To start manually:
python app.py

# Or activate virtual environment first:
source venv/bin/activate
python app.py
```

#### **🎯 What the Launcher Script Does:**
- ✅ **Activates Virtual Environment** - Ensures all dependencies are available
- ✅ **Checks Dependencies** - Verifies Python and required packages
- ✅ **Sets Environment Variables** - Configures Flask development mode
- ✅ **Starts Web Server** - Launches on http://localhost:5000
- ✅ **Shows Access Info** - Displays login credentials and URL
- ✅ **Graceful Shutdown** - Handles Ctrl+C properly

#### **🌐 Accessing the Application:**
- **URL**: http://localhost:5000
- **Default Credentials**: `acep` / `acep123`
- **Admin Panel**: Available after login

#### **📁 Important Directories:**
- **Application**: `./` (project root)
- **Database**: `./instance/` (created automatically)
- **Uploads**: `./static/uploads/` (for file uploads)
- **Logs**: Console output (can be redirected to file)

#### **🔄 Restarting the Application:**
```bash
# Stop with Ctrl+C, then restart:
./run_acep_hipaa.sh

# Or restart manually:
source venv/bin/activate
python app.py
```

---

### **❓ Need Help?**

#### **🔍 Common Issues:**
- **Permission Denied**: Use `sudo` for system package installation
- **Python Not Found**: The install script handles this automatically
- **Port Already in Use**: Change port in `app.py` or stop conflicting services
- **Dependency Errors**: Try running `./install.sh` again

#### **📞 Support:**
- **Documentation**: Check this README first
- **Issues**: Report on GitHub Issues page
- **Community**: Check Discussions tab on GitHub

---

## ⚠️ **System Requirements & Compatibility**

### **🖥️ Operating System Support**
| OS | Status | Notes |
|----|---------|-------|
| **Kali Linux 2023.3+** | ✅ **Fully Supported** | Recommended for cybersecurity professionals |
| **Ubuntu 20.04+** | ✅ **Fully Supported** | Excellent compatibility |
| **Debian 11+** | ✅ **Fully Supported** | Stable and reliable |
| **CentOS 8+ / RHEL 8+** | ✅ **Fully Supported** | Enterprise-grade support |
| **Windows 10/11** | ✅ **Supported via WSL2** | Use Ubuntu/Kali Linux in WSL2 |
| **macOS 10.15+** | ✅ **Fully Supported** | Native support with Homebrew |

### **🐍 Python Requirements**
- **Python Version**: 3.8+ (3.9+ Recommended for optimal performance)
- **Package Manager**: pip (latest version)
- **Virtual Environment**: Highly recommended for production use
- **Architecture**: x86_64, ARM64 (Apple Silicon supported)

### **💾 System Resources**
- **RAM**: Minimum 2GB, Recommended 4GB+ for large datasets
- **Storage**: 500MB free space for application and database
- **Network**: Internet access for initial setup and updates
- **Browser**: Modern browser with JavaScript enabled (Chrome, Firefox, Safari, Edge)

### **🔧 Prerequisites**
- **Git**: Required for repository cloning
- **Python 3.8+**: Core runtime environment
- **pip**: Python package manager
- **sudo access**: For system package installation (Linux/macOS)

---

## 🎯 **Core Features**

### **🔒 HIPAA Compliance Management**
| Feature | Description | Status |
|---------|-------------|---------|
| **Security Rule Coverage** | Complete 18 HIPAA Security Rule standards | ✅ Complete |
| **Administrative Safeguards** | 9 administrative requirements with detailed guidance | ✅ Complete |
| **Physical Safeguards** | 4 physical security requirements and assessments | ✅ Complete |
| **Technical Safeguards** | 5 technical security requirements and controls | ✅ Complete |
| **Status Tracking** | Compliant, Non-Compliant, Partial, Pending with progress bars | ✅ Complete |
| **Evidence Management** | File uploads, organization, and requirement association | ✅ Complete |
| **Risk Assessment** | Comprehensive risk register with scoring and mitigation | ✅ Complete |
| **PHI Tracking** | Protected Health Information monitoring and flow analysis | ✅ Complete |
| **Business Associates** | BA relationship tracking and compliance monitoring | ✅ Complete |

### **🎨 Professional Interface**
- **Modern Dark Theme** - Professional blue and black color scheme with subtle neon accents
- **Responsive Design** - Mobile-optimized interface that works on all devices
- **Advanced Search** - Quick requirement and evidence finding with filters
- **Real-time Statistics** - Live compliance status updates and progress tracking
- **Report Generation** - Professional HTML compliance reports with executive summaries
- **Interactive Dashboard** - Modern card-based layout with status indicators
- **Mobile Optimized** - Touch-friendly controls and adaptive layouts

---

## 🏗️ **Architecture & Technology**

### **🛠️ Technology Stack**
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Backend Framework** | Flask | 2.3.3 | Lightweight, flexible web framework |
| **Authentication** | Flask-Login | 0.6.3 | Secure user session management |
| **Template Engine** | Jinja2 | 3.1.2 | Powerful templating for dynamic content |
| **Database** | SQLite | Built-in | Reliable, file-based database |
| **Frontend** | HTML5 + Bootstrap 5 | Latest | Modern, responsive UI components |
| **Styling** | Custom CSS3 | Modern | Professional dark theme with animations |
| **JavaScript** | ES6+ | Modern | Interactive features and real-time updates |

### **📁 Project Structure**
```
ACEP-HIPAA-Audit-Assistant/
├── 🐍 app.py                           # Main Flask application with routing
├── 📋 requirements.txt                 # Python dependencies and versions
├── 🚀 install.sh                      # Complete installation & launch script
├── 🚀 run_acep_hipaa.sh              # Application launcher (used by install.sh)
├── 🎨 templates/                      # HTML templates and views
│   ├── base.html                      # Base template with navigation
│   ├── dashboard.html                 # Main dashboard with statistics
│   ├── audit_checklist.html           # HIPAA compliance checklist
│   ├── evidence.html                  # Evidence management interface
│   ├── risk_register.html             # Risk assessment and tracking
│   ├── phi_tracking.html              # PHI monitoring and analysis
│   ├── business_associates.html       # Business associate management
│   ├── reports.html                   # Report generation and export
│   └── *.html                         # Additional specialized templates
├── 🎨 static/                         # Static assets and resources
│   ├── css/styles.css                 # Custom styling and animations
│   ├── js/main.js                     # JavaScript functionality
│   └── uploads/                       # Secure file storage
├── 🗄️ database/                      # SQLite database and schemas
├── 📚 PROJECT_STRUCTURE.md            # Detailed project documentation
└── 📚 README.md                       # This comprehensive guide
```

---

## 🔐 **Default Access & Security**

After successful setup, access the application:

- **🌐 URL**: `http://localhost:5000` or `http://127.0.0.1:5000`
- **👤 Username**: `acep`
- **🔑 Password**: `acep123`
- **🔒 Security Note**: **IMPORTANT** - Change default credentials immediately after first login

---

## 🔧 **Troubleshooting & Support**

### **🚨 Common Issues & Solutions**

#### **1. ModuleNotFoundError: No module named 'flask'**
```bash
# Solution: Activate virtual environment first
source acep_hipaa_venv/bin/activate  # Linux/macOS
# OR
acep_hipaa_venv\Scripts\activate     # Windows

# Then run the application
python app.py
```

#### **2. Pillow Installation Issues**
```bash
# Solution: Use flexible version constraints
pip install "Pillow>=10.0.0,<11.0.0"

# Alternative: Install system dependencies first (Linux)
sudo apt install python3-dev python3-pip  # Ubuntu/Debian
sudo yum install python3-devel python3-pip  # CentOS/RHEL
```

#### **3. python-magic Issues on Windows**
```bash
# Note: python-magic requires libmagic (not available on Windows)
# The application will work without it, but file type detection may be limited
# Use WSL2 with Ubuntu/Kali Linux for full functionality
```

#### **4. Python Version Compatibility**
```bash
# Ensure Python 3.8+ is installed
python3 --version

# If using Python 3.13+, some packages may need flexible version constraints
# The setup.sh script handles this automatically
```

#### **5. Permission Denied Errors**
```bash
# Solution: Make scripts executable
chmod +x setup.sh run_acep_hipaa.sh

# Or run with proper permissions
sudo chown -R $USER:$USER .
```

#### **6. Virtual Environment Issues**
```bash
# Remove and recreate virtual environment
rm -rf acep_hipaa_venv
python3 -m venv acep_hipaa_venv
source acep_hipaa_venv/bin/activate
pip install -r requirements.txt
```

#### **7. Network/Proxy Issues**
```bash
# If behind corporate proxy, configure pip
pip install --proxy http://proxy.company.com:8080 -r requirements.txt

# Or use alternative package index
pip install -i https://pypi.org/simple/ -r requirements.txt
```

---

### **🛡️ Security Features**
- **Session Management** - Secure user sessions with timeout
- **Input Validation** - XSS and injection protection
- **File Upload Security** - Type validation and size restrictions
- **Authentication** - User login and access control
- **Data Encryption** - Sensitive data protection
- **Audit Logging** - Complete activity tracking for compliance

---

## 📱 **User Experience & Interface**

### **🏠 Dashboard Overview**
- **Real-time Compliance Statistics** - Live updates on compliance status
- **Quick Access Modules** - One-click navigation to all features
- **Status Indicators** - Visual progress bars and compliance scores
- **Recent Activity** - Latest updates and pending tasks

### **📋 Requirements Assessment**
- **Interactive Checklist** - Easy-to-use compliance evaluation interface
- **Status Updates** - Real-time status changes and comments
- **Requirement Categorization** - Organized by safeguard type
- **Progress Tracking** - Visual indicators of completion status

### **📁 Evidence Management**
- **File Upload Support** - PDF, DOCX, JPG, PNG with validation
- **Requirement Association** - Link evidence to specific requirements
- **Search and Filter** - Advanced search capabilities
- **Secure Storage** - Protected file storage and access control

### **⚠️ Risk Assessment**
- **Risk Register** - Comprehensive risk identification and scoring
- **Mitigation Strategies** - Track risk reduction efforts
- **Priority-based Sorting** - Focus on high-impact risks first
- **Risk Reporting** - Detailed analytics and trend analysis

---

## 🛠️ **Development & Customization**

### **🔧 Development Environment Setup**
```bash
# Set development mode
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run with auto-reload
python app.py
```

### **🗄️ Database Management**
```bash
# Reset database (if needed)
rm database/hipaa_audit.db
python app.py

# Backup database
cp database/hipaa_audit.db database/hipaa_audit_backup.db
```

### **🧪 Testing & Quality Assurance**
```bash
# Run basic tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app

# Code formatting
black .
flake8 .
```

---

## 🔒 **HIPAA Compliance Features**

### **🛡️ Built-in Compliance Tools**
- **Security Rule Mapping** - Direct alignment with HIPAA requirements
- **Evidence Collection** - Systematic documentation gathering
- **Risk Assessment** - Comprehensive security risk evaluation
- **Audit Trail** - Complete activity logging for compliance audits
- **Report Generation** - Professional compliance reports
- **Business Associate Tracking** - BA relationship management

### **🔐 Data Protection**
- **PHI Monitoring** - Protected Health Information tracking
- **Access Controls** - Role-based permissions and restrictions
- **Data Encryption** - Secure storage and transmission
- **Privacy Impact Assessment** - Systematic privacy evaluation
- **Breach Notification** - Incident tracking and reporting

---

## 📊 **Performance & Scalability**

### **⚡ Performance Features**
- **Lightweight Design** - Minimal resource usage and fast loading
- **Efficient Database** - Optimized SQLite queries and indexing
- **Smart Caching** - Intelligent data caching for performance
- **Async Operations** - Non-blocking operations for responsiveness

### **📈 Scalability Options**
- **Database Migration** - Easy transition to PostgreSQL/MySQL
- **Load Balancing** - Ready for production deployment
- **Microservices** - Modular architecture for scaling
- **Cloud Ready** - AWS, Azure, and GCP deployment support

---

## 🚀 **Deployment & Production**

### **🏠 Production Deployment**
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With systemd service
sudo systemctl enable acep-hipaa
sudo systemctl start acep-hipaa
```

### **🐳 Docker Deployment**
```bash
# Build and run
docker-compose up -d

# Scale services
docker-compose up -d --scale web=3
```

---

## 👨‍💻 **Creator & Maintainer**

### **👤 Chaitanya Eshwar Prasad**
**Cybersecurity Professional & HIPAA Compliance Expert**

> *"Empowering healthcare organizations with modern, efficient compliance tools that protect patient privacy and ensure regulatory adherence."*

### **�� Connect & Follow**
| Platform | Link | Description |
|----------|------|-------------|
| **🌐 Website** | [chaitanyaeshwarprasad.com](https://chaitanyaeshwarprasad.com) | Personal portfolio and blog |
| **💼 LinkedIn** | [linkedin.com/in/chaitanya-eshwar-prasad](https://linkedin.com/in/chaitanya-eshwar-prasad) | Professional network and updates |
| **🐙 GitHub** | [github.com/chaitanyaeshwarprasad](https://github.com/chaitanyaeshwarprasad) | Open source projects and code |
| **🎥 YouTube** | [youtube.com/@chaitanya.eshwar.prasad](https://youtube.com/@chaitanya.eshwar.prasad) | Tech tutorials and insights |
| **📸 Instagram** | [instagram.com/acep.tech.in.telugu](https://instagram.com/acep.tech.in.telugu) | Tech insights and updates |
| **🛡️ YesWeHack** | [yeswehack.com/hunters/chaitanya-eshwar-prasad](https://yeswehack.com/hunters/chaitanya-eshwar-prasad) | Bug bounty and security research |

---

## 🤝 **Contributing & Community**

We welcome contributions from the cybersecurity and healthcare communities! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **🔧 How to Contribute**
1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### **🌟 Community Benefits**
- **Recognition** - Name in contributors list
- **Experience** - Real-world HIPAA compliance project
- **Networking** - Connect with healthcare professionals
- **Learning** - Deep dive into healthcare security
- **Portfolio** - Showcase your compliance expertise

---

## 📞 **Support & Getting Help**

### **🆘 Getting Help**
- **📖 Documentation** - Check this README first
- **🐛 Issues** - Report bugs on GitHub Issues
- **💬 Discussions** - Join GitHub Discussions
- **📧 Contact** - Reach out via LinkedIn

### **🌟 Star & Share**
If this project helps you, please:
- ⭐ **Star** the repository
- 🔄 **Share** with healthcare colleagues
- 📢 **Mention** in your compliance projects
- 🏥 **Deploy** in your healthcare organization

---

## 🎉 **Thank You & Mission**

**Thank you for choosing ACEP HIPAA AUDIT ASSISTANT!**

Our mission is to **democratize healthcare compliance** by providing professional-grade tools that make HIPAA compliance accessible, efficient, and effective for healthcare organizations of all sizes.

*Empowering healthcare professionals with modern, efficient HIPAA compliance tools since 2024.*

---

<div align="center">

**🏥 Built with ❤️ for Healthcare Compliance**

**🔒 Secure • Professional • Reliable • Compliant**

[![GitHub stars](https://img.shields.io/github/stars/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant?style=social)](https://github.com/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant)
[![GitHub forks](https://img.shields.io/github/forks/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant?style=social)](https://github.com/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant)
[![GitHub issues](https://img.shields.io/github/issues/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant)](https://github.com/chaitanyaeshwarprasad/ACEP-HIPAA-Audit-Assistant)

**🌟 Join thousands of healthcare professionals using ACEP HIPAA Audit Assistant!**

</div>
