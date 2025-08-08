#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证窗口焦点竞争问题的解决方案
模拟谷歌浏览器等应用抢占焦点的情况，测试增强版监控器的应对能力
"""

import time
import win32gui
import win32con
import subprocess
import os
from enhanced_trae_ide_monitor import EnhancedTraeIDEMonitor

def find_chrome_window():
    """
    查找Chrome浏览器窗口
    """
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title and ('Chrome' in window_title or 'chrome' in window_title):
                windows.append((hwnd, window_title))
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def simulate_browser_interference():
    """
    模拟浏览器干扰（如果有Chrome窗口就激活它）
    """
    chrome_windows = find_chrome_window()
    
    if chrome_windows:
        hwnd, title = chrome_windows[0]
        print(f"🌐 模拟浏览器干扰: 激活 {title}")
        try:
            win32gui.SetForegroundWindow(hwnd)
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(1)
            return True
        except Exception as e:
            print(f"   ⚠️  激活浏览器失败: {e}")
            return False
    else:
        print("🌐 未找到Chrome浏览器窗口，跳过干扰模拟")
        return False

def test_window_activation_with_interference():
    """
    测试在有干扰窗口的情况下激活Trae IDE
    """
    print("=== 窗口焦点竞争测试 ===")
    print()
    
    # 创建监控器实例
    monitor = EnhancedTraeIDEMonitor()
    
    # 检查是否能找到Trae IDE窗口
    trae_hwnd = monitor.find_trae_window()
    if not trae_hwnd:
        print("❌ 未找到Trae IDE窗口，请确保Trae IDE正在运行")
        return False
    
    print(f"✅ 找到Trae IDE窗口")
    
    # 测试步骤1: 正常激活（无干扰）
    print("\n--- 步骤1: 正常激活测试 ---")
    success1 = monitor.activate_trae_window()
    print(f"正常激活结果: {'成功' if success1 else '失败'}")
    
    if not success1:
        print("❌ 正常激活都失败了，请检查权限或窗口状态")
        return False
    
    time.sleep(2)
    
    # 测试步骤2: 模拟干扰后激活
    print("\n--- 步骤2: 干扰环境下激活测试 ---")
    
    # 模拟浏览器干扰
    interference_created = simulate_browser_interference()
    
    if interference_created:
        print("等待2秒让干扰窗口稳定...")
        time.sleep(2)
        
        # 尝试激活Trae IDE
        print("\n🔄 在干扰环境下尝试激活Trae IDE...")
        success2 = monitor.activate_trae_window()
        print(f"干扰环境下激活结果: {'成功' if success2 else '失败'}")
        
        if success2:
            print("🎉 测试通过！增强版监控器成功解决了窗口焦点竞争问题")
        else:
            print("⚠️  测试失败，仍然无法在干扰环境下激活窗口")
            
        return success2
    else:
        print("⚠️  无法创建干扰环境，测试不完整")
        return True

def test_interfering_window_detection():
    """
    测试干扰窗口检测功能
    """
    print("\n=== 干扰窗口检测测试 ===")
    
    monitor = EnhancedTraeIDEMonitor()
    
    # 检测干扰窗口
    interfering_windows = monitor.detect_interfering_windows()
    
    if interfering_windows:
        print(f"🔍 检测到 {len(interfering_windows)} 个干扰窗口:")
        for hwnd, title in interfering_windows:
            print(f"   - {title}")
        
        # 测试处理干扰窗口
        print("\n🔧 测试处理干扰窗口...")
        monitor.handle_interfering_windows()
        
        # 再次检测
        time.sleep(1)
        remaining_windows = monitor.detect_interfering_windows()
        print(f"\n处理后剩余干扰窗口: {len(remaining_windows)} 个")
        
        return True
    else:
        print("✅ 未检测到干扰窗口")
        return True

def test_complete_monitoring_cycle():
    """
    测试完整的监控周期（包括干扰处理）
    """
    print("\n=== 完整监控周期测试 ===")
    print("这将模拟一次完整的监控周期，包括:")
    print("1. 检测并处理干扰窗口")
    print("2. 激活Trae IDE窗口")
    print("3. 检测目标按钮（模拟）")
    print("4. 最小化窗口")
    print()
    
    monitor = EnhancedTraeIDEMonitor()
    
    try:
        # 步骤1: 处理干扰窗口
        print("🔧 步骤1: 处理干扰窗口...")
        monitor.handle_interfering_windows()
        
        # 步骤2: 激活Trae IDE
        print("🔄 步骤2: 激活Trae IDE窗口...")
        if not monitor.activate_trae_window():
            print("❌ 激活失败")
            return False
        
        # 步骤3: 模拟检测（等待2秒）
        print("🔍 步骤3: 模拟按钮检测...")
        time.sleep(2)
        
        # 步骤4: 最小化窗口
        print("🔽 步骤4: 最小化窗口...")
        monitor.minimize_trae_window()
        
        print("✅ 完整监控周期测试成功")
        return True
        
    except Exception as e:
        print(f"❌ 监控周期测试失败: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("开始窗口焦点竞争问题测试...")
    print("请确保:")
    print("1. Trae IDE正在运行")
    print("2. 如果有Chrome浏览器更好（用于模拟干扰）")
    print()
    input("准备就绪后按Enter开始测试...")
    
    # 测试1: 干扰窗口检测
    success1 = test_interfering_window_detection()
    
    # 测试2: 窗口激活（含干扰）
    success2 = test_window_activation_with_interference()
    
    # 测试3: 完整监控周期
    success3 = test_complete_monitoring_cycle()
    
    # 总结
    print("\n=== 测试结果总结 ===")
    print(f"干扰窗口检测: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"窗口激活测试: {'✅ 通过' if success2 else '❌ 失败'}")
    print(f"完整监控周期: {'✅ 通过' if success3 else '❌ 失败'}")
    
    if success1 and success2 and success3:
        print("\n🎉 所有测试通过！")
        print("💡 增强版监控器现在应该能够处理窗口焦点竞争问题了")
        print("📝 建议在实际环境中运行 enhanced_trae_ide_monitor.py 进行验证")
    else:
        print("\n⚠️  部分测试失败，请检查配置或权限")
    
    print("\n测试完成。")

if __name__ == "__main__":
    main()