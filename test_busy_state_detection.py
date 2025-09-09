#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试繁忙状态检测功能
"""

import sys
import os
from enhanced_trae_ide_monitor import EnhancedTraeIDEMonitor

def test_busy_state_detection():
    """
    测试繁忙状态下的图像检测功能
    """
    print("=== 繁忙状态检测功能测试 ===")
    
    # 创建监控实例
    monitor = EnhancedTraeIDEMonitor()
    
    print(f"\n配置信息:")
    print(f"- 繁忙状态图像: {monitor.busy_state_images}")
    print(f"- 匹配阈值: {monitor.match_threshold}")
    
    # 检查图像文件是否存在
    print(f"\n检查图像文件:")
    for image_name in monitor.busy_state_images:
        if os.path.exists(image_name):
            print(f"✅ {image_name} - 文件存在")
        else:
            print(f"❌ {image_name} - 文件不存在")
    
    # 测试繁忙状态检测
    print(f"\n开始测试繁忙状态检测...")
    print("注意: 请确保屏幕上显示了pp.PNG或kk.PNG对应的按钮图像")
    print("按Enter键开始检测，或输入'q'退出:")
    
    user_input = input()
    if user_input.lower() == 'q':
        print("测试已取消")
        return
    
    # 执行检测
    result = monitor.find_busy_state_button()
    
    if result:
        image_name, x, y = result
        print(f"\n🎯 检测结果: 成功")
        print(f"- 检测到图像: {image_name}")
        print(f"- 位置坐标: ({x}, {y})")
        print(f"\n是否要点击该位置? (y/n):")
        
        click_input = input()
        if click_input.lower() == 'y':
            try:
                import pyautogui
                pyautogui.click(x, y)
                print(f"✅ 已点击位置 ({x}, {y})")
            except Exception as e:
                print(f"❌ 点击失败: {e}")
        else:
            print("跳过点击操作")
    else:
        print(f"\n❌ 检测结果: 未检测到任何繁忙状态按钮")
        print("可能的原因:")
        print("1. 屏幕上没有显示对应的按钮图像")
        print("2. 图像匹配度低于阈值")
        print("3. 图像文件损坏或格式不正确")
    
    print(f"\n=== 测试完成 ===")

def test_config_loading():
    """
    测试配置加载功能
    """
    print("=== 配置加载测试 ===")
    
    monitor = EnhancedTraeIDEMonitor()
    
    print(f"繁忙状态图像配置: {monitor.busy_state_images}")
    print(f"预期值: ['pp.PNG', 'kk.PNG']")
    
    if monitor.busy_state_images == ['pp.PNG', 'kk.PNG']:
        print("✅ 配置加载正确")
    else:
        print("❌ 配置加载错误")
    
    print(f"\n=== 配置测试完成 ===")

def main():
    print("繁忙状态检测功能测试工具")
    print("\n选择测试项目:")
    print("1. 配置加载测试")
    print("2. 繁忙状态检测测试")
    print("3. 退出")
    
    while True:
        choice = input("\n请输入选择 (1-3): ")
        
        if choice == '1':
            test_config_loading()
        elif choice == '2':
            test_busy_state_detection()
        elif choice == '3':
            print("退出测试")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()