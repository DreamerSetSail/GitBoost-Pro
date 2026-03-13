# -*- coding: utf-8 -*-
"""
GitBoost Pro - All-in-One GitHub Accelerator
Integrated: Background Monitor, IP Tester, Auto-Update, AutoStart
"""

import os
import sys
import socket
import time
import datetime
import ctypes
import shutil
import subprocess
import json
from pathlib import Path

# ================= Configuration =================
VERSION = "2.0.0"
CONFIG_FILE = Path(__file__).parent / "gitboost_config.json"
LOG_FILE = Path(__file__).parent / "gitboost_log.txt"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
CHECK_INTERVAL = 300  # 5 minutes

GITHUB_DOMAINS = {
    'github.com': [
        '185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153',
        '20.205.243.166', '20.205.243.167', '20.205.243.168',
        '140.82.113.3', '140.82.113.4', '140.82.114.3', '140.82.114.4',
    ],
    'api.github.com': [
        '185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153',
        '20.205.243.166', '20.205.243.167', '20.205.243.168',
    ],
    'raw.githubusercontent.com': [
        '185.199.108.133', '185.199.109.133', '185.199.110.133', '185.199.111.133',
    ],
    'avatars.githubusercontent.com': [
        '185.199.108.133', '185.199.109.133', '185.199.110.133', '185.199.111.133',
    ],
    'gist.github.com': ['20.205.243.166', '20.205.243.167'],
    'collector.github.com': ['140.82.113.21', '140.82.114.21'],
    'alive.github.com': ['140.82.114.26', '140.82.113.26'],
}

# ================= Language Pack =================
TEXT = {
    'zh': {
        'title': f"GitBoost Pro v{VERSION} - GitHub 全能加速器",
        'menu_title': "=== 功能菜单 ===",
        'menu_1': "[1] 启动后台实时监控（每 5 分钟自动更新）",
        'menu_2': "[2] 测试当前 GitHub IP 速度",
        'menu_3': "[3] 立即更新 Hosts 文件",
        'menu_4': "[4] 设置开机自启动",
        'menu_5': "[5] 取消开机自启动",
        'menu_6': "[6] 查看运行日志",
        'menu_7': "[7] 刷新 DNS 缓存",
        'menu_0': "[0] 退出程序",
        'select': "请选择功能 (0-7): ",
        'invalid': "无效选择，请重新输入",
        'press_enter': "按回车键继续...",
        'admin_required': "需要管理员权限！",
        'admin_hint': "请右键程序以管理员身份运行",
        'starting_monitor': "正在启动后台监控...",
        'monitor_started': "监控服务已启动",
        'testing_speed': "正在测试 IP 速度...",
        'updating_hosts': "正在更新 Hosts...",
        'install_autostart': "正在安装开机自启动...",
        'remove_autostart': "正在移除开机自启动...",
        'viewing_log': "打开日志文件...",
        'flushing_dns': "正在刷新 DNS...",
        'success': "成功",
        'failed': "失败",
        'exiting': "退出程序",
    },
    'en': {
        'title': f"GitBoost Pro v{VERSION} - GitHub Accelerator",
        'menu_title': "=== Function Menu ===",
        'menu_1': "[1] Start Background Monitor (Auto-update every 5 min)",
        'menu_2': "[2] Test Current GitHub IP Speed",
        'menu_3': "[3] Update Hosts File Now",
        'menu_4': "[4] Enable AutoStart on Boot",
        'menu_5': "[5] Disable AutoStart",
        'menu_6': "[6] View Log File",
        'menu_7': "[7] Flush DNS Cache",
        'menu_0': "[0] Exit",
        'select': "Select function (0-7): ",
        'invalid': "Invalid selection",
        'press_enter': "Press Enter to continue...",
        'admin_required': "Administrator privileges required!",
        'admin_hint': "Please run as administrator",
        'starting_monitor': "Starting background monitor...",
        'monitor_started': "Monitor service started",
        'testing_speed': "Testing IP speed...",
        'updating_hosts': "Updating Hosts...",
        'install_autostart': "Installing AutoStart...",
        'remove_autostart': "Removing AutoStart...",
        'viewing_log': "Opening log file...",
        'flushing_dns': "Flushing DNS...",
        'success': "Success",
        'failed': "Failed",
        'exiting': "Exiting",
    }
}

def detect_language():
    lang = os.environ.get('LANG', '')
    if os.name == 'nt':
        try:
            if ctypes.windll.kernel32.GetUserDefaultUILanguage() == 2052:
                return 'zh'
        except: pass
    if 'zh' in lang.lower(): return 'zh'
    return 'en'

CURRENT_LANG = detect_language()
def t(key): return TEXT[CURRENT_LANG].get(key, key)

# ================= Utility Functions =================

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    print(entry, end='')
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f: f.write(entry)
    except: pass

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() if os.name == 'nt' else os.getuid() == 0
    except: return False

def save_config(data):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)
    except: pass

def load_config():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return {}

def test_ip_speed(ip, port=443, timeout=2):
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        latency = (time.time() - start) * 1000
        sock.close()
        return latency if result == 0 else None
    except: return None

def find_fastest_ip(domain, ip_list):
    best_ip, best_latency = None, float('inf')
    for ip in ip_list:
        latency = test_ip_speed(ip)
        if latency and latency < best_latency:
            best_latency, best_ip = latency, ip
    if best_ip:
        log(f"  {domain}: {best_ip} ({best_latency:.0f}ms)")
        return best_ip
    try:
        dns_ip = socket.gethostbyname(domain)
        log(f"  {domain}: {dns_ip} (DNS)")
        return dns_ip
    except:
        log(f"  {domain}: No IP")
        return None

def get_current_hosts_entries():
    entries = {}
    try:
        with open(HOSTS_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        in_block = False
        for line in lines:
            if "# GITBOOST_PRO_START" in line: in_block = True; continue
            if "# GITBOOST_PRO_END" in line: in_block = False; continue
            if in_block and line.strip() and not line.startswith('#'):
                parts = line.strip().split()
                if len(parts) >= 2:
                    for domain in parts[1:]: entries[domain] = parts[0]
    except Exception as e: log(f"Read hosts error: {e}")
    return entries

def update_hosts_file(ip_map):
    if not ip_map: return False
    try:
        backup = HOSTS_PATH + f".backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(HOSTS_PATH, backup)
        log(f"  Backup: {Path(backup).name}")
        
        with open(HOSTS_PATH, 'r', encoding='utf-8') as f: lines = f.readlines()
        new_lines = []
        in_block = False
        for line in lines:
            if "# GITBOOST_PRO_START" in line: in_block = True; continue
            if "# GITBOOST_PRO_END" in line: in_block = False; continue
            if not in_block:
                is_github = any(d in line for d in GITHUB_DOMAINS.keys())
                if not is_github or line.startswith('#'): new_lines.append(line)
        
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_content = ["\n", f"# GITBOOST_PRO_START (Updated at {ts})\n"]
        for domain, ip in ip_map.items(): new_content.append(f"{ip} {domain}\n")
        new_content.append("# GITBOOST_PRO_END\n")
        
        with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            f.writelines(new_content)
        log("  Hosts updated!")
        return True
    except Exception as e:
        log(f"  Update error: {e}")
        return False

def flush_dns():
    try:
        os.system("ipconfig /flushdns >nul 2>&1")
        log("  DNS flushed")
        return True
    except: return False

def check_and_update():
    log("=" * 50)
    log("Checking GitHub IPs...")
    updates = {}
    for domain, ip_list in GITHUB_DOMAINS.items():
        fastest = find_fastest_ip(domain, ip_list)
        if fastest: updates[domain] = fastest
    
    if updates:
        current = get_current_hosts_entries()
        needs_update = False
        for domain, ip in updates.items():
            if current.get(domain) != ip:
                needs_update = True
                log(f"  {domain}: {current.get(domain, 'N/A')} -> {ip} [UPDATE]")
            else:
                log(f"  {domain}: {ip} [OK]")
        
        if needs_update:
            log("\nUpdating hosts...")
            if update_hosts_file(updates): flush_dns()
        else:
            log("All IPs optimal")
    else:
        log("No available IPs")

# ================= Feature Functions =================

def start_background_monitor():
    """Start background monitoring service"""
    log("\n" + "=" * 60)
    log(t('starting_monitor'))
    
    if not is_admin():
        print(t('admin_required'))
        return False
    
    script = os.path.abspath(__file__)
    params = f'--background --interval {CHECK_INTERVAL}'
    
    try:
        subprocess.Popen([sys.executable, script] + params.split(), 
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0)
        log(t('monitor_started'))
        return True
    except Exception as e:
        log(f"Error: {e}")
        return False

def test_speed_menu():
    """Test IP speeds"""
    log("\n" + "=" * 60)
    log(t('testing_speed'))
    print("\nCurrent DNS Resolution:")
    for domain in list(GITHUB_DOMAINS.keys())[:4]:
        try: print(f"  {domain}: {socket.gethostbyname(domain)}")
        except: pass
    
    print("\nTesting IPs...")
    results = []
    all_ips = set(ip for ips in GITHUB_DOMAINS.values() for ip in ips)
    for ip in list(all_ips)[:15]:
        latency = test_ip_speed(ip)
        if latency:
            results.append((ip, latency))
            print(f"  {ip}: {latency:.0f}ms [OK]")
        else:
            print(f"  {ip}: Timeout [Fail]")
    
    if results:
        results.sort(key=lambda x: x[1])
        print("\n" + "=" * 60)
        print("Top 5 Fastest:")
        for i, (ip, lat) in enumerate(results[:5], 1):
            print(f"  {i}. {ip}: {lat:.0f}ms")
    input(f"\n{t('press_enter')}")

def update_hosts_now():
    """Immediate hosts update"""
    log("\n" + "=" * 60)
    log(t('updating_hosts'))
    if not is_admin():
        print(t('admin_required'))
        input(t('press_enter'))
        return
    check_and_update()
    input(f"\n{t('press_enter')}")

def install_autostart():
    """Install auto-start on boot"""
    log("\n" + "=" * 60)
    log(t('install_autostart'))
    
    startup_dir = Path(os.getenv('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    shortcut = startup_dir / "GitBoost Pro.lnk"
    
    try:
        script = os.path.abspath(__file__)
        vbs_content = f'''Set objShell = CreateObject("WScript.Shell")
objShell.Run "python ""{script}"" --background", 0, False
'''
        vbs_path = Path(script).parent / "gitboost_start.vbs"
        with open(vbs_path, 'w', encoding='utf-8') as f: f.write(vbs_content)
        
        # Create shortcut via PowerShell
        ps_cmd = f'''$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut}')
$Shortcut.TargetPath = '{vbs_path}'
$Shortcut.WorkingDirectory = '{Path(script).parent}'
$Shortcut.Description = 'GitBoost Pro Background Service'
$Shortcut.Save()
'''
        subprocess.run(['powershell', '-Command', ps_cmd], check=True)
        log(f"  AutoStart installed: {shortcut}")
        print(f"\n{t('success')}: {shortcut}")
    except Exception as e:
        log(f"  Error: {e}")
        print(f"\n{t('failed')}: {e}")
    input(t('press_enter'))

def remove_autostart():
    """Remove auto-start"""
    log("\n" + "=" * 60)
    log(t('remove_autostart'))
    
    startup_dir = Path(os.getenv('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    shortcut = startup_dir / "GitBoost Pro.lnk"
    vbs_path = Path(__file__).parent / "gitboost_start.vbs"
    
    try:
        if shortcut.exists(): shortcut.unlink()
        if vbs_path.exists(): vbs_path.unlink()
        log("  AutoStart removed")
        print(f"\n{t('success')}")
    except Exception as e:
        log(f"  Error: {e}")
        print(f"\n{t('failed')}: {e}")
    input(t('press_enter'))

def view_log():
    """Open log file"""
    log("\n" + "=" * 60)
    log(t('viewing_log'))
    try:
        if LOG_FILE.exists():
            os.startfile(str(LOG_FILE))
            # Show last 20 lines
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print("\nLast 20 lines:")
                for line in lines[-20:]: print(line, end='')
        else:
            print("No log file found")
    except Exception as e:
        print(f"Error: {e}")
    input(t('press_enter'))

def flush_dns_menu():
    """Flush DNS"""
    log("\n" + "=" * 60)
    log(t('flushing_dns'))
    if flush_dns(): print(f"\n{t('success')}")
    else: print(f"\n{t('failed')}")
    input(t('press_enter'))

def run_background_service(interval=300):
    """Run as background service"""
    log("\n" + "=" * 60)
    log(f"GitBoost Pro Background Service v{VERSION}")
    log("=" * 60)
    
    if not is_admin():
        log("Warning: Not running as admin, some features may fail")
    
    log(f"Interval: {interval}s")
    log(f"Log: {LOG_FILE}")
    log("\nFirst check...\n")
    
    check_and_update()
    count = 1
    
    while True:
        next_time = datetime.datetime.now() + datetime.timedelta(seconds=interval)
        log(f"\nNext: {next_time.strftime('%H:%M:%S')}")
        log(f"Waiting {interval}s... (#{count})")
        time.sleep(interval)
        count += 1
        check_and_update()

def show_menu():
    """Show main menu"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 60)
    print(t('title'))
    print("=" * 60)
    print(t('menu_title'))
    print(t('menu_1'))
    print(t('menu_2'))
    print(t('menu_3'))
    print(t('menu_4'))
    print(t('menu_5'))
    print(t('menu_6'))
    print(t('menu_7'))
    print(t('menu_0'))
    print("=" * 60)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--background', action='store_true', help='Run as background service')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds')
    parser.add_argument('--test', action='store_true', help='Quick test mode')
    args = parser.parse_args()
    
    if args.background:
        run_background_service(args.interval)
        return
    
    if args.test:
        check_and_update()
        return
    
    # Interactive mode
    while True:
        show_menu()
        choice = input(t('select')).strip()
        
        if choice == '1': start_background_monitor()
        elif choice == '2': test_speed_menu()
        elif choice == '3': update_hosts_now()
        elif choice == '4': install_autostart()
        elif choice == '5': remove_autostart()
        elif choice == '6': view_log()
        elif choice == '7': flush_dns_menu()
        elif choice == '0':
            log(t('exiting'))
            break
        else:
            print(t('invalid'))
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n\nInterrupted by user")
    except Exception as e:
        log(f"\nFatal error: {e}")
        if not '--background' in sys.argv:
            input("Press Enter to exit...")
