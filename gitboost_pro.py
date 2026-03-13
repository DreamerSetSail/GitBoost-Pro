# -*- coding: utf-8 -*-
"""
GitBoost Pro - GitHub Accelerator & Repo Scanner
Supports Auto Language Detection (CN/EN)
"""

import os
import sys
import socket
import datetime
import re
import shutil
import subprocess
import ctypes
import json
import time
from pathlib import Path

# ================= 配置与语言包 =================

# 语言检测
def detect_language():
    """自动检测系统语言，返回 'zh' 或 'en'"""
    lang = os.environ.get('LANG', '')
    # Windows 有时使用 LC_ALL 或 USERNAME 等间接判断，但主要看 LANG 或系统区域
    if os.name == 'nt':
        # Windows 尝试通过 PowerShell 获取区域，或者简单判断环境变量
        try:
            # 简单的启发式：如果用户名为中文或特定环境变量存在
            if 'zh' in lang.lower():
                return 'zh'
            # 更准确的 Windows 检测方法 (可选，若上面的不够用)
            # 这里为了保持脚本轻量，主要依赖 LANG 环境变量，
            # 如果用户在中文 Windows 且没设置 LANG，默认尝试检测系统区域代码页
            if ctypes.windll.kernel32.GetUserDefaultUILanguage() == 2052: # 2052 是简体中文
                return 'zh'
        except:
            pass
    
    if 'zh' in lang.lower():
        return 'zh'
    return 'en'

CURRENT_LANG = detect_language()

# 配置文件路径
CONFIG_FILE = Path(__file__).parent / "gitboost_config.json"

# 语言字典
TEXT = {
    'zh': {
        'title': "🚀 GitBoost Pro - GitHub 全能加速与仓库扫描",
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
        'menu_select': "请输入选项 (1-5): "
    },
    'en': {
        'title': "🚀 GitBoost Pro - GitHub Accelerator & Repo Scanner",
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
        'menu_select': "Please enter option (1-5): "
    }
}

def t(key):
    """获取当前语言的文本"""
    return TEXT[CURRENT_LANG].get(key, key)

# ================= 配置管理函数 =================

def load_config():
    """加载配置文件"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_config(config):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def get_update_interval():
    """获取自动更新时间间隔"""
    config = load_config()
    return config.get('update_interval', 5)

def set_update_interval(minutes):
    """设置自动更新时间间隔"""
    if 1 <= minutes <= 1440:
        config = load_config()
        config['update_interval'] = minutes
        if save_config(config):
            print(t('update_interval_set').format(minutes))
            return True
    print(t('invalid_interval'))
    return False

# ================= 功能函数 =================

def set_startup():
    """设置开机自启动"""
    if os.name == 'nt':
        # Windows系统
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        vbs_path = os.path.join(startup_folder, 'gitboost_start.vbs')
        bat_path = os.path.abspath('GitBoost_Pro.bat')
        
        vbs_content = f'CreateObject("WScript.Shell").Run "{bat_path}", 0, False'
        
        try:
            with open(vbs_path, 'w', encoding='utf-8') as f:
                f.write(vbs_content)
            print("✅ 已设置开机自启动")
            return True
        except Exception as e:
            print(f"❌ 设置开机自启动失败: {e}")
            return False
    else:
        print("⚠️ 仅支持Windows系统设置开机自启动")
        return False

def remove_startup():
    """移除开机自启动"""
    if os.name == 'nt':
        # Windows系统
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        vbs_path = os.path.join(startup_folder, 'gitboost_start.vbs')
        
        try:
            if os.path.exists(vbs_path):
                os.remove(vbs_path)
                print("✅ 已移除开机自启动")
            else:
                print("ℹ️ 开机自启动未设置")
            return True
        except Exception as e:
            print(f"❌ 移除开机自启动失败: {e}")
            return False
    else:
        print("⚠️ 仅支持Windows系统移除开机自启动")
        return False

def set_update_interval_menu():
    """设置自动更新时间间隔菜单"""
    current_interval = get_update_interval()
    print(f"\n{t('current_update_interval').format(current_interval)}")
    
    try:
        input_str = input(t('set_update_interval')).strip()
        if not input_str:
            # 使用默认值5
            set_update_interval(5)
        else:
            minutes = int(input_str)
            set_update_interval(minutes)
    except ValueError:
        print(t('invalid_interval'))
    input("\n按 [回车键] 继续...")

def show_menu():
    """显示功能菜单"""
    print("\n" + "="*60)
    print(t('menu_title'))
    print("="*60)
    print(t('menu_1'))
    print(t('menu_1_desc'))
    print(t('menu_2'))
    print(t('menu_3'))
    print(t('menu_4'))
    print(t('menu_5'))
    print("="*60)
    print(t('menu_hint'))
    print("="*60)

HOSTS_PATH_MAP = {
    'win32': r'C:\Windows\System32\drivers\etc\hosts',
    'darwin': '/etc/hosts',
    'linux': '/etc/hosts'
}

GITHUB_DOMAINS = {
    'github.com': [
        '185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153',
        '20.205.243.166', '20.205.243.167', '20.205.243.168',
        '140.82.113.3', '140.82.113.4', '140.82.114.3', '140.82.114.4',
        '192.30.255.112', '192.30.255.113'
    ],
    'api.github.com': [
        '185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153',
        '20.205.243.166', '20.205.243.167', '20.205.243.168',
        '192.30.255.116', '192.30.255.117'
    ],
    'raw.githubusercontent.com': [
        '185.199.108.133', '185.199.109.133', '185.199.110.133', '185.199.111.133',
        '199.232.68.133', '199.232.69.133'
    ],
    'avatars.githubusercontent.com': [
        '185.199.108.133', '185.199.109.133', '185.199.110.133', '185.199.111.133',
        '199.232.68.133', '199.232.69.133'
    ],
    'gist.github.com': [
        '20.205.243.166', '20.205.243.167',
        '192.30.255.118', '192.30.255.119'
    ],
    'collector.github.com': ['140.82.113.21', '140.82.114.21'],
    'alive.github.com': ['140.82.114.26', '140.82.113.26'],
    'assets-cdn.github.com': [
        '185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153',
        '199.232.68.133', '199.232.69.133'
    ],
    'github.global.ssl.fastly.net': [
        '151.101.1.194', '151.101.65.194', '151.101.129.194', '151.101.193.194',
        '199.232.68.163', '199.232.69.163'
    ],
    'camo.githubusercontent.com': [
        '185.199.108.133', '185.199.109.133', '185.199.110.133', '185.199.111.133'
    ],
    'github.io': [
        '185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153'
    ],
    'githubstatus.com': [
        '185.199.108.153', '185.199.109.153', '185.199.110.153', '185.199.111.153'
    ]
}

COMMON_ROOTS = [
    os.path.expanduser("~"),
    os.path.expanduser("~/Projects"),
    os.path.expanduser("~/Code"),
    os.path.expanduser("~/Dev"),
    os.path.expanduser("~/workspace"),
    "C:\\Projects",
    "D:\\Projects",
    "C:\\Code",
    "D:\\Code"
]

def get_system_type():
    return sys.platform

def get_hosts_path():
    platform = get_system_type()
    if platform in HOSTS_PATH_MAP:
        return HOSTS_PATH_MAP[platform]
    raise OSError("Unsupported OS")

def is_admin():
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.getuid() == 0
    except Exception:
        return False

def backup_hosts(hosts_path):
    backup_path = hosts_path + f".backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        shutil.copy2(hosts_path, backup_path)
        print(t('backup_ok') + backup_path)
        return True
    except Exception as e:
        print(t('backup_fail') + str(e))
        return False

def test_ip_speed(ip, port=443, timeout=2):
    """测试IP速度"""
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        latency = (time.time() - start) * 1000
        sock.close()
        return latency if result == 0 else None
    except:
        return None

def find_fastest_ip(domain, ip_list):
    """找到最快的IP地址"""
    best_ip, best_latency = None, float('inf')
    
    # 测试所有IP地址
    for ip in ip_list:
        latency = test_ip_speed(ip)
        if latency and latency < best_latency:
            best_latency, best_ip = latency, ip
    
    if best_ip:
        print(f"  {domain}: {best_ip} ({best_latency:.0f}ms) [最佳]")
        return best_ip
    
    # 如果所有IP都测试失败，尝试DNS解析
    try:
        dns_ip = socket.gethostbyname(domain)
        print(f"  {domain}: {dns_ip} (DNS) [备用]")
        return dns_ip
    except:
        print(f"  {domain}: 无法解析 [失败]")
        return None

def resolve_ip(domain):
    try:
        # 修正拼写错误
        ip = socket.gethostbyname(domain)
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            return ip
    except socket.gaierror:
        pass
    return None

def fetch_github_ips():
    print("\n" + t('step1'))
    ip_map = {}
    success_count = 0
    
    for domain, ip_list in GITHUB_DOMAINS.items():
        print(f"{t('resolving')} {domain}...")
        ip = find_fastest_ip(domain, ip_list)
        if ip:
            ip_map[domain] = ip
            success_count += 1
        else:
            print(f"  {domain}: {t('failed')}")
            
    return ip_map, success_count

def find_local_repos():
    print("\n" + t('step2'))
    repos = []
    valid_roots = [Path(root) for root in COMMON_ROOTS if Path(root).exists()]
    
    if not valid_roots:
        print(t('no_repos'))
        return repos

    print(f"{t('scan_range')} {[str(r) for r in valid_roots]}")
    
    for root in valid_roots:
        try:
            for dirpath, dirnames, filenames in os.walk(str(root)):
                depth = dirpath.replace(str(root), '').count(os.sep)
                if depth > 4: 
                    dirnames[:] = []
                    continue
                
                if '.git' in dirnames:
                    git_config_path = os.path.join(dirpath, '.git', 'config')
                    is_github = False
                    repo_name = os.path.basename(dirpath)
                    
                    try:
                        # 尝试多种编码读取 config
                        content = ""
                        for enc in ['utf-8', 'gbk', 'latin-1']:
                            try:
                                with open(git_config_path, 'r', encoding=enc) as f:
                                    content = f.read()
                                break
                            except UnicodeDecodeError:
                                continue
                        
                        if 'github.com' in content:
                            is_github = True
                            match = re.search(r'url = .+github\.com[:/](.+?)(?:\.git)?', content)
                            if match:
                                repo_name = match.group(1)
                    except Exception:
                        pass

                    if is_github:
                        repos.append({'path': dirpath, 'name': repo_name})
                    
                    # 优化：找到 .git 后不再深入子目录
                    dirnames.remove('.git') 
                    dirnames[:] = [] 
                    
        except PermissionError:
            continue
        except Exception:
            continue

    if repos:
        print(t('found_repos').format(len(repos)))
        for i, repo in enumerate(repos[:5]):
            print(f"      {i+1}. {repo['name']} -> {repo['path']}")
        if len(repos) > 5:
            print(f"      ... and {len(repos) - 5} more repos")
    else:
        print(t('no_repos'))
        
    return repos

def update_hosts_file(ip_map):
    hosts_path = get_hosts_path()
    if not os.path.exists(hosts_path):
        print(f"❌ Hosts file not found: {hosts_path}")
        return False

    if not backup_hosts(hosts_path):
        return False

    try:
        # 尝试多种编码读取
        lines = []
        read_success = False
        for enc in ['utf-8', 'gbk', 'latin-1']:
            try:
                with open(hosts_path, 'r', encoding=enc) as f:
                    lines = f.readlines()
                read_success = True
                break
            except UnicodeDecodeError:
                continue
        
        if not read_success:
            print("❌ Could not read Hosts file due to encoding issues.")
            return False

    except Exception as e:
        print(f"❌ Error reading Hosts: {e}")
        return False

    new_lines = []
    start_marker = "# GITBOOST_PRO_START"
    end_marker = "# GITBOOST_PRO_END"
    
    inside_block = False
    for line in lines:
        if start_marker in line:
            inside_block = True
            continue
        if end_marker in line:
            inside_block = False
            continue
        
        if not inside_block:
            # 移除旧的 GitHub 条目
            is_old_github = False
            for domain in GITHUB_DOMAINS:
                if domain in line and not line.strip().startswith('#'):
                    is_old_github = True
                    break
            if not is_old_github:
                new_lines.append(line)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_content = [
        "\n",
        f"{start_marker} (Updated at {timestamp})\n"
    ]
    
    for domain, ip in ip_map.items():
        new_content.append(f"{ip} {domain}\n")
    new_content.append(f"{end_marker}\n")

    try:
        # 强制使用 UTF-8 写入，防止中文注释乱码
        with open(hosts_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            f.writelines(new_content)
        print(t('hosts_update_ok'))
        return True
    except PermissionError:
        print("❌ Permission Denied! Please run as Administrator.")
        return False
    except Exception as e:
        print(f"❌ Write failed: {e}")
        return False

def flush_dns():
    print("\n" + t('step3'))
    platform = get_system_type()
    try:
        if platform == 'win32':
            subprocess.run(["ipconfig", "/flushdns"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif platform == 'darwin':
            subprocess.run(["sudo", "dscacheutil", "-flushcache"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif platform == 'linux':
            try:
                subprocess.run(["sudo", "systemctl", "restart", "nscd"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                try:
                    subprocess.run(["sudo", "service", "nscd", "restart"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    pass
        print(t('dns_ok'))
    except Exception as e:
        print(t('dns_fail').format(str(e)))

def default_run():
    """默认运行所有功能"""
    ip_map, success_count = fetch_github_ips()
    if success_count == 0:
        print("\n" + t('network_error'))
        input(t('press_exit'))
        return False

    local_repos = find_local_repos()
    
    print("\n" + t('step4'))
    if update_hosts_file(ip_map):
        flush_dns()
        print("\n" + "="*60)
        print(t('all_done'))
        print("="*60)
        if local_repos:
            print(t('repo_hint').format(len(local_repos)))
        else:
            print(t('no_repo_hint'))
        return True
    else:
        print("\n" + t('hosts_update_fail'))
        return False

def main():
    # 清屏 (可选)
    # os.system('cls' if os.name == 'nt' else 'clear') 
    
    print("="*60)
    print(t('title'))
    print("="*60)
    
    if not is_admin():
        print("\n" + t('admin_error'))
        if os.name == 'nt':
            print(t('admin_win_hint'))
        else:
            print(t('admin_unix_hint'))
        input(t('press_exit'))
        return

    # 显示菜单并处理用户选择
    while True:
        show_menu()
        choice = input(t('menu_select')).strip()
        
        if choice == '1':
            # 默认运行
            default_run()
            input(t('press_close'))
            break
        elif choice == '2':
            # 设置开机自启动
            set_startup()
            input("\n按 [回车键] 继续...")
        elif choice == '3':
            # 移除开机自启动
            remove_startup()
            input("\n按 [回车键] 继续...")
        elif choice == '4':
            # 设置自动更新时间
            set_update_interval_menu()
        elif choice == '5':
            # 退出程序
            print("\n👋 退出程序")
            input(t('press_exit'))
            break
        else:
            # 无效选择，默认运行
            print("\n⚠️ 无效选择，默认运行所有功能")
            default_run()
            input(t('press_close'))
            break

if __name__ == "__main__":
    main()