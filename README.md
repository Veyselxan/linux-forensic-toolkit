# Linux Forensic Toolkit (LFT)


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

## 📦 Installation

### Requirements
- Python 3.6+
- Linux system
- Root access (recommended for full functionality)
- Recommended packages: `net-tools`, `psutil`, `prettytable`
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

