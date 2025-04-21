# Linux Forensic Toolkit (LFT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue)](https://python.org)
[![PyPI](https://img.shields.io/badge/pip-1.0.0-blue)](https://pypi.org/project/linux-forensic-toolkit)


A comprehensive command-line tool for Linux system monitoring, forensic analysis, and diagnostics with a user-friendly interface.

## Features

### 🖥️ System Monitoring
- Real-time system resource dashboard
- CPU/RAM/Disk/Network usage statistics
- Active network connections monitoring
- System uptime tracking

### 🔍 Forensic Analysis
- **File Analysis**
  - File hash generation (MD5, SHA1, SHA256)
  - SUID/SGID file detection
  - File metadata inspection
  - **Keyword-based file search**
  
- **Process Analysis**
  - Real-time process monitoring
  - Process sorting by resource usage
  - Process memory maps inspection

### 🌐 Network Analysis
- Active connection monitoring
- Listening port display
- Routing table inspection
- ARP cache analysis

### 📊 System Diagnostics
- Mounted filesystems list
- Kernel module inspection
- Environment variables display
- **User login history**

### � Memory Analysis
- Memory usage by process
- Shared memory segments
- Process memory maps
🚀 Usage
Quick Start
bash
# Install package
```
pip install linux-forensic-toolkit

# Run the tool

lft
```
# Interactive Menu System
```
=== LINUX FORENSIC TOOLKIT ===
1. System Monitoring Dashboard  [Realtime metrics]
2. Process Analysis             [Top 50 processes]
3. File Analysis                [Hashes/SUID/Search]
4. Network Analysis             [Connections/Routing]
5. Memory Analysis              [Shared memory]
6. System Information           [Login history/Kernel]
7. Exit
```
# Practical Examples

# Search files containing "password"
```
lft → 3 → 4
Enter directory: /home/user/documents
Keyword: password
```

# Check user login history
```
lft → 6 → 5
```

# Analyze network connections
```
lft → 4 → 1
```
### 🔑 Key Features
```
Feature	Command Path	Description
Real-time Monitoring	Main Menu     → 1	Live CPU/RAM/Disk/Network stats with color-coded alerts
Forensic File Search	File Analysis → 4	Recursive content search with line numbers and context
Security Audit	      File Analysis → 2	Detect suspicious SUID/SGID executables
Network Recon	Network Analysis      → 1-4	Complete network mapping (connections/ports/routes)
```
# Advanced Features
```
► User Login Timeline
  Path: System Info → 5
  Shows: Login/logout times, IP addresses, durations

► Process Memory Inspection
  Path: Memory Analysis → 3
  Features: View memory maps for any running process

► File Fingerprinting
  Path: File Analysis → 1
  Algorithms: MD5, SHA1, SHA256 hash generation

► Environment Audit
  Path: System Info → 4
  Displays: All environment variables with values
```
### 📦 Installation

### Requirements
- Python 3.6+
- Linux system
- Root access (recommended for full functionality)
- Recommended packages: `net-tools`, `psutil`, `prettytable`

- 
### Install via pip
```bash
pip install linux-forensic-toolkit
```

###Install from source

```
bash
git clone https://github.com/Veyselxan/linux-forensic-toolkit.git
cd linux-forensic-toolkit
pip install .
```

### 📌 Notes
Requires psutil and prettytable packages

Some features require root privileges

File search may take time on large directories

Network features depend on net-tools package

### 🤝 Contributing
Pull requests welcome! Please follow PEP8 guidelines and include tests for new features.

### 📄 License
MIT License - See LICENSE for details

