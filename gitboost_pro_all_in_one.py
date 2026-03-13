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
        'title': f"GitBoost Pro v{VERSION} - GitHub 全能加速与仓库扫描",
        'step1': "🌐 [步骤 1] 正在查询最新 IP 地址...",
        'step2': "🔍 [步骤 2] 正在扫描本地 GitHub 仓库...",
        'step3': "🔄 [步骤 3] 正在刷新 DNS 缓存...",
        'step4': "📝 [步骤 4] 正在更新 Hosts 文件...",
        'resolving': "   解析",
        'success': "✅ 成功",
        'failed': "❌ 失败",
        'backup_ok': "✅ 已备份 Hosts 文件到：",
        'backup_fail': "❌ 备份失败：",
        'scan_range': "   搜索范围:",
        'found_repos': "   ✅ 发现 {} 个 GitHub 本地仓库:",
        'no_repos': "   ℹ️ 未在常见目录中找到 GitHub 本地仓库。",
        'hosts_update_ok': "✅ Hosts 文件更新成功！",
        'hosts_update_fail': "❌ 更新 Hosts 失败。",
        'dns_ok': "✅ DNS 缓存已刷新。",
        'dns_fail': "⚠️ 刷新 DNS 失败 (可忽略): {}",
        'all_done': "🎉 所有任务完成！",
        'repo_hint': "💡 检测到 {} 个本地仓库。",
        'no_repo_hint': "💡 提示：未检测到本地仓库，快去克隆一个吧！",
        'admin_error': "❌ 错误：必须以管理员身份运行！",
        'admin_win_hint': "💡 Windows: 请右键 '一键加速.bat' -> '以管理员身份运行'",
        'admin_unix_hint': "💡 Mac/Linux: 请使用 'sudo python3 gitboost_pro.py'",
        'network_error': "❌ 无法获取任何 IP，请检查网络连接。",
        'press_exit': "\n⛔ 按 [回车键] 退出...",
        'press_close': "\n✅ 操作已完成。按 [回车键] 关闭窗口...",
        'current_update_interval': "当前自动更新时间间隔: {} 分钟",
        'set_update_interval': "请输入自动更新时间间隔 (1-1440 分钟，默认 5 分钟): ",
        'update_interval_set': "✅ 自动更新时间间隔已设置为 {} 分钟",
        'invalid_interval': "⚠️ 无效的时间间隔，请输入 1-1440 之间的数字",
        'menu_title': "🚀 GitBoost Pro - 功能菜单",
        'menu_1': "1. 默认运行",
        'menu_1_desc': "   (获取IP + 扫描仓库 + 更新Hosts + 刷新DNS)",
        'menu_2': "2. 设置开机自启动",
        'menu_3': "3. 移除开机自启动",
        'menu_4': "4. 设置自动更新时间",
        'menu_5': "5. 退出程序",
        'menu_hint': "提示: 直接按回车或输入其他数字将默认运行所有功能",
        'menu_select': "请输入选项 (1-5): ",
        'press_enter': "按回车键继续...",
        'starting_monitor': "正在启动后台监控...",
        'monitor_started': "监控服务已启动",
        'testing_speed': "正在测试 IP 速度...",
        'updating_hosts': "正在更新 Hosts...",
        'install_autostart': "正在安装开机自启动...",
        'remove_autostart': "正在移除开机自启动...",
        'viewing_log': "打开日志文件...",
        'flushing_dns': "正在刷新 DNS...",
        'exiting': "退出程序",
    },
    'en': {
        'title': f"GitBoost Pro v{VERSION} - GitHub Accelerator & Repo Scanner",
        'step1': "🌐 [Step 1] Fetching latest IP addresses...",
        'step2': "🔍 [Step 2] Scanning for local GitHub repositories...",
        'step3': "🔄 [Step 3] Flushing DNS cache...",
        'step4': "📝 [Step 4] Updating Hosts file...",
        'resolving': "   Resolving",
        'success': "✅ Success",
        'failed': "❌ Failed",
        'backup_ok': "✅ Hosts backed up to: ",
        'backup_fail': "❌ Backup failed: ",
        'scan_range': "   Search scope:",
        'found_repos': "   ✅ Found {} local GitHub repos:",
        'no_repos': "   ℹ️ No GitHub repos found in common directories.",
        'hosts_update_ok': "✅ Hosts file updated successfully!",
        'hosts_update_fail': "❌ Failed to update Hosts.",
        'dns_ok': "✅ DNS cache flushed.",
        'dns_fail': "⚠️ DNS flush failed (ignorable): {}",
        'all_done': "🎉 All tasks completed!",
        'repo_hint': "💡 Detected {} local repositories.",
        'no_repo_hint': "💡 Tip: No local repos found. Time to clone one!",
        'admin_error': "❌ Error: Administrator privileges required!",
        'admin_win_hint': "💡 Windows: Right-click '一键加速.bat' and select 'Run as Administrator'",
        'admin_unix_hint': "💡 Mac/Linux: Run with 'sudo python3 gitboost_pro.py'",
        'network_error': "❌ Could not resolve any IPs. Please check your internet connection.",
        'press_exit': "\n⛔ Press [Enter] to exit...",
        'press_close': "\n✅ Done. Press [Enter] to close...",
        'current_update_interval': "Current auto-update interval: {} minutes",
        'set_update_interval': "Please enter auto-update interval (1-1440 minutes, default 5): ",
        'update_interval_set': "✅ Auto-update interval set to {} minutes",
        'invalid_interval': "⚠️ Invalid interval, please enter a number between 1-1440",
        'menu_title': "🚀 GitBoost Pro - Function Menu",
        'menu_1': "1. Default Run",
        'menu_1_desc': "   (Fetch IP + Scan Repos + Update Hosts + Flush DNS)",
        'menu_2': "2. Set Auto-Start on Boot",
        'menu_3': "3. Remove Auto-Start",
        'menu_4': "4. Set Auto-Update Time",
        'menu_5': "5. Exit Program",
        'menu_hint': "Hint: Press Enter or input other numbers to run default functions",
        'menu_select': "Please enter option (1-5): ",
        'press_enter': "Press Enter to continue...",
        'starting_monitor': "Starting background monitor...",
        'monitor_started': "Monitor service started",
        'testing_speed': "Testing IP speed...",
        'updating_hosts': "Updating Hosts...",
        'install_autostart': "Installing AutoStart...",
        'remove_autostart': "Removing AutoStart...",
        'viewing_log': "Opening log file...",
        'flushing_dns': "Flushing DNS...",
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

def set_update_interval():
    """设置自动更新时间间隔"""
    config = load_config()
    current_interval = config.get('update_interval', 5)
    print(f"\n{t('current_update_interval').format(current_interval)}")
    
    try:
        minutes = input(t('set_update_interval'))
        if not minutes:  # 直接回车，使用默认值
            minutes = 5
        else:
            minutes = int(minutes)
        
        if 1 <= minutes <= 1440:
            config['update_interval'] = minutes
            if save_config(config):
                print(t('update_interval_set').format(minutes))
            else:
                print(t('failed'))
        else:
            print(t('invalid_interval'))
    except ValueError:
        print(t('invalid_interval'))
    input("\n按 [回车键] 继续...")

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
    print("=" * 60)
    print(t('menu_1'))
    print(t('menu_1_desc'))
    print(t('menu_2'))
    print(t('menu_3'))
    print(t('menu_4'))
    print(t('menu_5'))
    print("=" * 60)
    print(t('menu_hint'))
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
        choice = input(t('menu_select')).strip()
        
        if choice == '1' or not choice:
            # 默认运行
            check_and_update()
            input(t('press_close'))
        elif choice == '2':
            # 设置开机自启动
            install_autostart()
        elif choice == '3':
            # 移除开机自启动
            remove_autostart()
        elif choice == '4':
            # 设置自动更新时间
            set_update_interval()
        elif choice == '5':
            # 退出程序
            log(t('exiting'))
            break
        else:
            # 其他输入默认运行
            check_and_update()
            input(t('press_close'))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n\nInterrupted by user")
    except Exception as e:
        log(f"\nFatal error: {e}")
        if not '--background' in sys.argv:
            input("Press Enter to exit...")
