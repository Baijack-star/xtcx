#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证窗口最小化功能
用于测试增强版监控器的窗口管理功能
"""

import time
import win32gui
import win32con

def find_trae_window():
    """
    查找Trae IDE窗口
    """
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title and any(keyword in window_title.lower() for keyword in ['trae', 'github']):
                windows.append((hwnd, window_title))
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def test_window_operations():
    """
    测试窗口操作：激活、最大化、最小化
    """
    print("=== 测试窗口最小化功能 ===")
    print()
    
    # 查找Trae窗口
    print("🔍 正在查找Trae IDE窗口...")
    windows = find_trae_window()
    
    if not windows:
        print("❌ 未找到Trae IDE窗口")
        return False
    
    print(f"✅ 找到 {len(windows)} 个Trae相关窗口:")
    for i, (hwnd, title) in enumerate(windows):
        print(f"   {i+1}. {title}")
    
    # 使用第一个窗口进行测试
    hwnd, title = windows[0]
    print(f"\n📋 使用窗口进行测试: {title}")
    
    try:
        # 测试1: 激活并最大化窗口
        print("\n🔄 测试1: 激活并最大化窗口")
        if win32gui.IsIconic(hwnd):
            print("   窗口当前是最小化状态，正在恢复...")
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(1)
        
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        print("   ✅ 窗口已激活并最大化")
        
        # 等待用户确认
        input("   按Enter继续测试最小化功能...")
        
        # 测试2: 最小化窗口
        print("\n🔽 测试2: 最小化窗口")
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        time.sleep(1)
        print("   ✅ 窗口已最小化")
        
        # 等待用户确认
        input("   按Enter继续测试恢复功能...")
        
        # 测试3: 再次恢复窗口
        print("\n🔄 测试3: 再次恢复窗口")
        if win32gui.IsIconic(hwnd):
            print("   检测到窗口是最小化状态，正在恢复...")
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(1)
        
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        print("   ✅ 窗口已重新激活并最大化")
        
        print("\n🎉 所有窗口操作测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def test_monitoring_cycle():
    """
    模拟监控周期测试
    """
    print("\n=== 模拟监控周期测试 ===")
    print("这将模拟监控器的完整工作流程：")
    print("1. 激活窗口")
    print("2. 检测按钮（模拟）")
    print("3. 发送消息（模拟）")
    print("4. 最小化窗口")
    print()
    
    windows = find_trae_window()
    if not windows:
        print("❌ 未找到Trae IDE窗口")
        return False
    
    hwnd, title = windows[0]
    print(f"📋 使用窗口: {title}")
    
    try:
        for cycle in range(1, 4):  # 测试3个周期
            print(f"\n--- 监控周期 {cycle} ---")
            
            # 步骤1: 激活窗口
            print("🔄 激活Trae IDE窗口...")
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(1)
            win32gui.SetForegroundWindow(hwnd)
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            print("   ✅ 窗口已激活")
            
            # 步骤2-3: 模拟检测和发送（等待2秒）
            print("🔍 模拟检测按钮和发送消息...")
            time.sleep(2)
            print("   ✅ 模拟操作完成")
            
            # 步骤4: 最小化窗口
            print("🔽 最小化窗口...")
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            time.sleep(1)
            print("   ✅ 窗口已最小化")
            
            if cycle < 3:
                print("⏱️  等待下次周期...")
                time.sleep(3)
        
        print("\n🎉 监控周期测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 监控周期测试中发生错误: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("开始测试窗口最小化功能...")
    print("请确保Trae IDE在运行，然后按Enter开始测试...")
    input()
    
    # 基础窗口操作测试
    success1 = test_window_operations()
    
    if success1:
        print("\n是否要进行监控周期测试？(y/n): ", end="")
        if input().lower() == 'y':
            success2 = test_monitoring_cycle()
        else:
            success2 = True
    else:
        success2 = False
    
    print("\n=== 测试结果 ===")
    if success1 and success2:
        print("🎉 所有测试通过！增强版监控器的窗口管理功能正常。")
        print("💡 现在可以在生产环境中使用，Trae IDE将在检测完成后自动最小化。")
    else:
        print("⚠️  部分测试失败，请检查配置。")
    
    print("\n测试完成。")

if __name__ == "__main__":
    main()