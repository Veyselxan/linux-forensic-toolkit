#!/usr/bin/env python3
import psutil
import socket
import time
from datetime import datetime
import os
import sys
import hashlib
import subprocess
import json
from prettytable import PrettyTable

# ANSI codes for colored output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    END = '\033[0m'

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def get_size(bytes):
    """Convert bytes to human-readable format"""
    for unit in ['', 'K', 'M', 'G', 'T']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def get_system_info():
    """Get system resource usage information"""
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=False)
    cpu_load = f"{cpu_percent}% ({cpu_count} cores)"

    # Memory
    mem = psutil.virtual_memory()
    mem_usage = f"{get_size(mem.used)}/{get_size(mem.total)} ({mem.percent}%)"

    # Disk
    disk = psutil.disk_usage('/')
    disk_usage = f"{get_size(disk.used)}/{get_size(disk.total)} ({disk.percent}%)"

    # Network
    net_io = psutil.net_io_counters()
    net_usage = f"▲{get_size(net_io.bytes_sent)} ▼{get_size(net_io.bytes_recv)}"

    return {
        'CPU': cpu_load,
        'RAM': mem_usage,
        'Disk': disk_usage,
        'Network': net_usage,
        'Uptime': str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
    }

def get_connections():
    """Get network connections and process information"""
    connections = []
    proc_names = {p.pid: p.name() for p in psutil.process_iter(['pid', 'name'])}

    for c in psutil.net_connections(kind='inet'):
        try:
            laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
            raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ""

            # Process information
            pid = c.pid or 0
            name = proc_names.get(pid, "?")[:15]
            cmdline = " ".join(psutil.Process(pid).cmdline())[:50] if pid else ""

            # Color based on connection type
            conn_color = Colors.GREEN if c.status == 'ESTABLISHED' else Colors.YELLOW

            connections.append({
                'proto': 'TCP' if c.type == socket.SOCK_STREAM else 'UDP',
                'laddr': laddr,
                'raddr': raddr,
                'status': f"{conn_color}{c.status}{Colors.END}",
                'pid': pid,
                'name': name,
                'cmdline': cmdline
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return connections

def display_dashboard():
    """Display system monitoring dashboard"""
    system_info = get_system_info()
    connections = get_connections()

    clear_screen()

    # System information table
    sys_table = PrettyTable()
    sys_table.field_names = [f"{Colors.CYAN}System Resource{Colors.END}", f"{Colors.CYAN}Usage{Colors.END}"]
    sys_table.align = "l"

    for key, value in system_info.items():
        sys_table.add_row([f"{Colors.PURPLE}{key}{Colors.END}", value])

    # Network connections table
    net_table = PrettyTable()
    net_table.field_names = [
        f"{Colors.CYAN}Proto{Colors.END}",
        f"{Colors.CYAN}Local{Colors.END}",
        f"{Colors.CYAN}Remote{Colors.END}",
        f"{Colors.CYAN}Status{Colors.END}",
        f"{Colors.CYAN}PID{Colors.END}",
        f"{Colors.CYAN}Process{Colors.END}",
        f"{Colors.CYAN}Command{Colors.END}"
    ]
    net_table.align = "l"

    for conn in connections[:20]:  # Show last 20 connections
        net_table.add_row([
            conn['proto'],
            conn['laddr'],
            conn['raddr'],
            conn['status'],
            conn['pid'],
            conn['name'],
            conn['cmdline']
        ])

    # Header
    print(f"{Colors.BLUE}=== SYSTEM MONITOR (Update: {datetime.now().strftime('%H:%M:%S')}) ==={Colors.END}")
    print(sys_table)
    print(f"\n{Colors.BLUE}=== ACTIVE NETWORK CONNECTIONS ==={Colors.END}")
    print(net_table)
    print(f"\n{Colors.YELLOW}Total connections: {len(connections)} | Press CTRL+C to exit{Colors.END}")

def get_running_processes():
    """Get detailed information about running processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status', 'create_time']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'user': proc.info['username'],
                'cpu': proc.info['cpu_percent'],
                'memory': proc.info['memory_percent'],
                'status': proc.info['status'],
                'start_time': datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort by memory usage
    processes = sorted(processes, key=lambda p: p['memory'], reverse=True)
    return processes[:50]  # Return top 50 processes

def display_processes(processes):
    """Display running processes in a table"""
    clear_screen()
    table = PrettyTable()
    table.field_names = [
        f"{Colors.CYAN}PID{Colors.END}",
        f"{Colors.CYAN}Name{Colors.END}",
        f"{Colors.CYAN}User{Colors.END}",
        f"{Colors.CYAN}CPU%{Colors.END}",
        f"{Colors.CYAN}Mem%{Colors.END}",
        f"{Colors.CYAN}Status{Colors.END}",
        f"{Colors.CYAN}Start Time{Colors.END}"
    ]

    for proc in processes:
        table.add_row([
            proc['pid'],
            proc['name'][:20],
            proc['user'],
            f"{proc['cpu']:.1f}",
            f"{proc['memory']:.1f}",
            proc['status'],
            proc['start_time']
        ])

    print(f"{Colors.BLUE}=== RUNNING PROCESSES (Top 50 by Memory Usage) ==={Colors.END}")
    print(table)

def calculate_hash(file_path):
    """Calculate MD5, SHA1, and SHA256 hashes of a file"""
    hash_md5 = hashlib.md5()
    hash_sha1 = hashlib.sha1()
    hash_sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
                hash_sha1.update(chunk)
                hash_sha256.update(chunk)

        return {
            'file': file_path,
            'md5': hash_md5.hexdigest(),
            'sha1': hash_sha1.hexdigest(),
            'sha256': hash_sha256.hexdigest()
        }
    except IOError as e:
        return {'error': str(e)}

def file_analysis_menu():
    """File analysis submenu"""
    while True:
        clear_screen()
        print(f"{Colors.BLUE}=== FILE ANALYSIS MENU ==={Colors.END}")
        print("1. Calculate file hashes")
        print("2. Find suspicious files (SUID/SGID)")
        print("3. Check file metadata")
        print("4. Keyword-based File Search")
        print("5. Back to main menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            file_path = input("Enter file path: ")
            result = calculate_hash(file_path)
            if 'error' in result:
                print(f"{Colors.RED}Error: {result['error']}{Colors.END}")
            else:
                print(f"\n{Colors.GREEN}Hash results for {file_path}:{Colors.END}")
                print(f"MD5:    {result['md5']}")
                print(f"SHA1:   {result['sha1']}")
                print(f"SHA256: {result['sha256']}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            find_special_files()
            input("\nPress Enter to continue...")

        elif choice == "3":
            file_path = input("Enter file path: ")
            display_file_metadata(file_path)
            input("\nPress Enter to continue...")

        elif choice == "4":
            directory = input("Enter directory to search in: ")
            keyword = input("Enter keyword to search: ")
            matches = keyword_file_search(directory, keyword)
            display_keyword_search(matches)
            input("\nPress Enter to continue...")

        elif choice == "5":
            break

        else:
            print(f"{Colors.RED}Invalid choice!{Colors.END}")
            time.sleep(1)
def keyword_file_search(directory, keyword):
    """Search files in directory for keyword matches"""
    matches = []
    if not os.path.isdir(directory):
        return {'error': f"Directory not found: {directory}"}

    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if keyword in line:
                                matches.append({
                                    'file': file_path,
                                    'line': line_num,
                                    'text': line.strip()
                                })
                except (IOError, PermissionError, UnicodeDecodeError):
                    continue
        return matches
    except Exception as e:
        return {'error': str(e)}

def display_keyword_search(results):
    """Display keyword search results"""
    clear_screen()
    print(f"{Colors.BLUE}=== KEYWORD SEARCH RESULTS ==={Colors.END}")

    if isinstance(results, dict) and 'error' in results:
        print(f"{Colors.RED}Error: {results['error']}{Colors.END}")
        return

    if not results:
        print(f"{Colors.YELLOW}No matches found.{Colors.END}")
        return

    table = PrettyTable()
    table.field_names = [
        f"{Colors.CYAN}File{Colors.END}",
        f"{Colors.CYAN}Line{Colors.END}",
        f"{Colors.CYAN}Content{Colors.END}"
    ]

    for match in results[:100]:  # Show first 100 matches
        table.add_row([
            match['file'],
            match['line'],
            match['text'][:100]  # Truncate long lines
        ])

    print(table)
    print(f"\n{Colors.YELLOW}Found {len(results)} matches. Showing first 100 results.{Colors.END}")
def find_special_files():
    """Find SUID/SGID files"""
    clear_screen()
    print(f"{Colors.BLUE}=== FINDING SUID/SGID FILES ==={Colors.END}")

    try:
        # Find SUID files
        suid_cmd = "find / -type f -perm -4000 -exec ls -la {} + 2>/dev/null"
        suid_files = subprocess.check_output(suid_cmd, shell=True).decode().split('\n')

        # Find SGID files
        sgid_cmd = "find / -type f -perm -2000 -exec ls -la {} + 2>/dev/null"
        sgid_files = subprocess.check_output(sgid_cmd, shell=True).decode().split('\n')

        print(f"\n{Colors.YELLOW}SUID Files:{Colors.END}")
        for file in suid_files:
            if file.strip():
                print(file)

        print(f"\n{Colors.YELLOW}SGID Files:{Colors.END}")
        for file in sgid_files:
            if file.strip():
                print(file)

    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error finding special files: {e}{Colors.END}")

def display_file_metadata(file_path):
    """Display file metadata"""
    try:
        stat = os.stat(file_path)
        print(f"\n{Colors.GREEN}Metadata for {file_path}:{Colors.END}")
        print(f"Size:         {get_size(stat.st_size)}")
        print(f"Permissions:  {oct(stat.st_mode & 0o777)}")
        print(f"Owner UID:    {stat.st_uid}")
        print(f"Group GID:    {stat.st_gid}")
        print(f"Created:      {datetime.fromtimestamp(stat.st_ctime)}")
        print(f"Modified:     {datetime.fromtimestamp(stat.st_mtime)}")
        print(f"Accessed:     {datetime.fromtimestamp(stat.st_atime)}")
    except OSError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")

def network_analysis_menu():
    """Network analysis submenu"""
    while True:
        clear_screen()
        print(f"{Colors.BLUE}=== NETWORK ANALYSIS MENU ==={Colors.END}")
        print("1. Show active connections")
        print("2. Show listening ports")
        print("3. Show routing table")
        print("4. Show ARP cache")
        print("5. Back to main menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            display_connections_table(get_connections())
            input("\nPress Enter to continue...")

        elif choice == "2":
            show_listening_ports()
            input("\nPress Enter to continue...")

        elif choice == "3":
            show_routing_table()
            input("\nPress Enter to continue...")

        elif choice == "4":
            show_arp_cache()
            input("\nPress Enter to continue...")

        elif choice == "5":
            break

        else:
            print(f"{Colors.RED}Invalid choice!{Colors.END}")
            time.sleep(1)

def display_connections_table(connections):
    """Display connections in a table"""
    table = PrettyTable()
    table.field_names = [
        f"{Colors.CYAN}Proto{Colors.END}",
        f"{Colors.CYAN}Local{Colors.END}",
        f"{Colors.CYAN}Remote{Colors.END}",
        f"{Colors.CYAN}Status{Colors.END}",
        f"{Colors.CYAN}PID{Colors.END}",
        f"{Colors.CYAN}Process{Colors.END}"
    ]

    for conn in connections:
        table.add_row([
            conn['proto'],
            conn['laddr'],
            conn['raddr'],
            conn['status'],
            conn['pid'],
            conn['name']
        ])

    print(table)

def show_listening_ports():
    """Show all listening ports"""
    clear_screen()
    print(f"{Colors.BLUE}=== LISTENING PORTS ==={Colors.END}")

    try:
        netstat_cmd = "netstat -tulnp 2>/dev/null | grep LISTEN"
        listening_ports = subprocess.check_output(netstat_cmd, shell=True).decode()
        print(listening_ports)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")

def show_routing_table():
    """Show system routing table"""
    clear_screen()
    print(f"{Colors.BLUE}=== ROUTING TABLE ==={Colors.END}")

    try:
        route_cmd = "ip route show"
        routes = subprocess.check_output(route_cmd, shell=True).decode()
        print(routes)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")

def show_arp_cache():
    """Show ARP cache"""
    clear_screen()
    print(f"{Colors.BLUE}=== ARP CACHE ==={Colors.END}")

    try:
        arp_cmd = "arp -a"
        arp_cache = subprocess.check_output(arp_cmd, shell=True).decode()
        print(arp_cache)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")

def memory_analysis_menu():
    """Memory analysis submenu"""
    while True:
        clear_screen()
        print(f"{Colors.BLUE}=== MEMORY ANALYSIS MENU ==={Colors.END}")
        print("1. Show memory usage by process")
        print("2. Show shared memory segments")
        print("3. Show memory maps for a process")
        print("4. Back to main menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            display_processes(get_running_processes())
            input("\nPress Enter to continue...")

        elif choice == "2":
            show_shared_memory()
            input("\nPress Enter to continue...")

        elif choice == "3":
            pid = input("Enter PID: ")
            show_memory_maps(pid)
            input("\nPress Enter to continue...")

        elif choice == "4":
            break

        else:
            print(f"{Colors.RED}Invalid choice!{Colors.END}")
            time.sleep(1)

def show_shared_memory():
    """Show shared memory segments"""
    clear_screen()
    print(f"{Colors.BLUE}=== SHARED MEMORY SEGMENTS ==={Colors.END}")

    try:
        ipcs_cmd = "ipcs -m"
        shared_mem = subprocess.check_output(ipcs_cmd, shell=True).decode()
        print(shared_mem)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")

def show_memory_maps(pid):
    """Show memory maps for a specific process"""
    clear_screen()
    print(f"{Colors.BLUE}=== MEMORY MAPS FOR PID {pid} ==={Colors.END}")

    try:
        maps_file = f"/proc/{pid}/maps"
        with open(maps_file, 'r') as f:
            print(f.read())
    except IOError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")

def system_info_menu():
    """System information submenu"""
    while True:
        clear_screen()
        print(f"{Colors.BLUE}=== SYSTEM INFORMATION MENU ==={Colors.END}")
        print("1. Show system resources")
        print("2. Show mounted filesystems")
        print("3. Show kernel modules")
        print("4. Show environment variables")
        print("5. User Login History")
        print("6. Back to main menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            display_dashboard()
            input("\nPress Enter to continue...")

        elif choice == "2":
            show_mounted_filesystems()
            input("\nPress Enter to continue...")

        elif choice == "3":
            show_kernel_modules()
            input("\nPress Enter to continue...")

        elif choice == "4":
            show_environment_variables()
            input("\nPress Enter to continue...")

        elif choice == "5":
            display_login_history()
            input("\nPress Enter to continue...")

        elif choice == "6":
            break

        else:
            print(f"{Colors.RED}Invalid choice!{Colors.END}")
            time.sleep(1)


def display_login_history():
    """Display user login history"""
    clear_screen()
    print(f"{Colors.BLUE}=== USER LOGIN HISTORY ==={Colors.END}")
    try:
        logins = subprocess.check_output(
            ["last", "-F"],
            stderr=subprocess.STDOUT,
            text=True
        )
        print(logins)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error retrieving login history: {e.output}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")



def show_mounted_filesystems():
    """Show mounted filesystems"""
    clear_screen()
    print(f"{Colors.BLUE}=== MOUNTED FILESYSTEMS ==={Colors.END}")

    try:
        mount_cmd = "mount"
        mounts = subprocess.check_output(mount_cmd, shell=True).decode()
        print(mounts)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")

def show_kernel_modules():
    """Show loaded kernel modules"""
    clear_screen()
    print(f"{Colors.BLUE}=== LOADED KERNEL MODULES ==={Colors.END}")

    try:
        lsmod_cmd = "lsmod"
        modules = subprocess.check_output(lsmod_cmd, shell=True).decode()
        print(modules)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")

def show_environment_variables():
    """Show environment variables"""
    clear_screen()
    print(f"{Colors.BLUE}=== ENVIRONMENT VARIABLES ==={Colors.END}")

    for key, value in os.environ.items():
        print(f"{key}={value}")

def main_menu():
    """Main menu"""
    while True:
        clear_screen()
        print(f"{Colors.BLUE}=== LINUX FORENSIC TOOLKIT ==={Colors.END}")
        print("1. System Monitoring Dashboard")
        print("2. Process Analysis")
        print("3. File Analysis")
        print("4. Network Analysis")
        print("5. Memory Analysis")
        print("6. System Information")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            try:
                while True:
                    display_dashboard()
                    time.sleep(3)
            except KeyboardInterrupt:
                pass

        elif choice == "2":
            display_processes(get_running_processes())
            input("\nPress Enter to continue...")

        elif choice == "3":
            file_analysis_menu()

        elif choice == "4":
            network_analysis_menu()

        elif choice == "5":
            memory_analysis_menu()

        elif choice == "6":
            system_info_menu()

        elif choice == "7":
            print(f"\n{Colors.GREEN}Exiting...{Colors.END}")
            sys.exit(0)

        else:
            print(f"{Colors.RED}Invalid choice!{Colors.END}")
            time.sleep(1)

def main():
    # Dependency check
    try:
        import psutil
        from prettytable import PrettyTable
    except ImportError as e:
        print(f"{Colors.RED}Error: Required library missing - {e}{Colors.END}")
        print("Install with: pip3 install psutil prettytable")
        sys.exit(1)

    # Run main menu
    main_menu()

if __name__ == "__main__":
    main()