#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证增强版监控器的窗口检测和激活功能
用于测试是否能正确找到并激活Trae IDE窗口
"""

import win32gui
import win32con
import time

def find_all_windows():
    """
    列出所有可见窗口
    """
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title.strip():  # 只显示有标题的窗口
                windows.append((hwnd, window_title))
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def find_trae_windows():
    """
    查找Trae相关窗口
    """
    keywords = ["Trae", "trae", "IDE", "ide"]
    all_windows = find_all_windows()
    trae_windows = []
    
    for hwnd, title in all_windows:
        for keyword in keywords:
            if keyword in title:
                trae_windows.append((hwnd, title))
                break
    
    return trae_windows

def test_window_activation(hwnd, title):
    """
    测试窗口激活功能
    """
    print(f"\n🔄 测试激活窗口: {title}")
    
    try:
        # 检查窗口状态
        is_minimized = win32gui.IsIconic(hwnd)
        print(f"   窗口是否最小化: {is_minimized}")
        
        # 如果最小化，先恢复
        if is_minimized:
            print("   正在恢复最小化窗口...")
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(1)
        
        # 激活窗口
        print("   正在激活窗口...")
        win32gui.SetForegroundWindow(hwnd)
        
        # 最大化窗口
        print("   正在最大化窗口...")
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        
        time.sleep(2)
        print("   ✅ 窗口激活成功")
        return True
        
    except Exception as e:
        print(f"   ❌ 窗口激活失败: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("=== 增强版Trae IDE监控器 - 窗口检测测试 ===")
    print()
    
    # 列出所有窗口
    print("📋 当前所有可见窗口:")
    all_windows = find_all_windows()
    for i, (hwnd, title) in enumerate(all_windows[:10]):  # 只显示前10个
        print(f"   {i+1}. {title}")
    
    if len(all_windows) > 10:
        print(f"   ... 还有 {len(all_windows) - 10} 个窗口")
    
    print(f"\n总共找到 {len(all_windows)} 个可见窗口")
    
    # 查找Trae窗口
    print("\n🔍 查找Trae相关窗口...")
    trae_windows = find_trae_windows()
    
    if not trae_windows:
        print("❌ 未找到Trae相关窗口")
        print("\n💡 建议:")
        print("   1. 确保Trae IDE已经启动")
        print("   2. 检查窗口标题是否包含'Trae'或'IDE'关键词")
        print("   3. 如果窗口标题不同，请修改关键词列表")
        return
    
    print(f"✅ 找到 {len(trae_windows)} 个Trae相关窗口:")
    for i, (hwnd, title) in enumerate(trae_windows):
        print(f"   {i+1}. {title} (句柄: {hwnd})")
    
    # 测试激活第一个Trae窗口
    if trae_windows:
        hwnd, title = trae_windows[0]
        print(f"\n🎯 将测试激活第一个窗口: {title}")
        print("请注意观察窗口是否被激活和最大化...")
        
        input("按Enter键开始测试...")
        
        success = test_window_activation(hwnd, title)
        
        if success:
            print("\n🎉 测试通过！增强版监控器应该能正常激活窗口。")
        else:
            print("\n⚠️  测试失败，请检查权限或窗口状态。")
    
    print("\n测试完成。")

if __name__ == "__main__":
    main()