#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试菜单显示功能
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

# 语言检测
def detect_language():
    """自动检测系统语言，返回 'zh' 或 'en'"""
    lang = os.environ.get('LANG', '')
    if os.name == 'nt':
        try:
            if 'zh' in lang.lower():
                return 'zh'
            if ctypes.windll.kernel32.GetUserDefaultUILanguage() == 2052: # 2052 是简体中文
                return 'zh'
        except:
            pass
    
    if 'zh' in lang.lower():
        return 'zh'
    return 'en'

CURRENT_LANG = detect_language()

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

# 显示菜单
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

# 测试菜单显示
def test_menu():
    print("="*60)
    print(t('title'))
    print("="*60)
    
    # 显示菜单
    show_menu()
    
    # 模拟用户输入
    print("\n测试菜单显示完成！")
    print("菜单选项:")
    print("1. 默认运行 (获取IP + 扫描仓库 + 更新Hosts + 刷新DNS)")
    print("2. 设置开机自启动")
    print("3. 移除开机自启动")
    print("4. 设置自动更新时间")
    print("5. 退出程序")
    print("\n菜单显示正确吗？")

if __name__ == "__main__":
    test_menu()