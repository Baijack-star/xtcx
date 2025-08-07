#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证鼠标移动到安全位置功能
用于测试发送消息后鼠标是否正确移动到安全区域
"""

import pyautogui
import time

def test_mouse_movement():
    """
    测试鼠标移动到安全位置的功能
    """
    print("=== 鼠标移动测试 ===")
    
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕尺寸: {screen_width}x{screen_height}")
    
    # 计算安全位置
    safe_x = screen_width - 50
    safe_y = screen_height - 50
    print(f"安全位置: ({safe_x}, {safe_y})")
    
    print("\n开始测试...")
    print("1. 鼠标将移动到屏幕中央")
    
    # 移动到屏幕中央（模拟点击发送按钮的位置）
    center_x = screen_width // 2
    center_y = screen_height // 2
    pyautogui.moveTo(center_x, center_y)
    print(f"鼠标已移动到中央位置: ({center_x}, {center_y})")
    
    time.sleep(2)
    
    print("2. 鼠标将移动到安全位置")
    
    # 移动到安全位置
    pyautogui.moveTo(safe_x, safe_y)
    print(f"鼠标已移动到安全位置: ({safe_x}, {safe_y})")
    
    time.sleep(2)
    
    print("\n✅ 鼠标移动测试完成！")
    print("如果鼠标正确移动到了屏幕右下角，说明功能正常。")

def test_complete_flow():
    """
    测试完整的消息发送流程（模拟）
    """
    print("\n=== 完整流程测试 ===")
    
    # 模拟点击输入框
    print("1. 模拟点击输入框...")
    screen_width, screen_height = pyautogui.size()
    input_x = screen_width // 2 - 100
    input_y = screen_height // 2
    pyautogui.moveTo(input_x, input_y)
    time.sleep(1)
    
    # 模拟点击发送按钮
    print("2. 模拟点击发送按钮...")
    button_x = screen_width // 2 + 100
    button_y = screen_height // 2
    pyautogui.moveTo(button_x, button_y)
    time.sleep(1)
    
    print("3. 发送完成，移动鼠标到安全位置...")
    
    # 移动到安全位置（与实际代码相同的逻辑）
    safe_x = screen_width - 50
    safe_y = screen_height - 50
    pyautogui.moveTo(safe_x, safe_y)
    time.sleep(0.5)
    
    print("✅ 完整流程测试完成！")
    print("鼠标应该在屏幕右下角的安全位置。")

def main():
    """
    主测试函数
    """
    print("鼠标移动功能测试")
    print("=" * 40)
    print("此测试将验证发送消息后鼠标移动到安全位置的功能")
    print("请确保屏幕上没有重要操作，然后按Enter开始测试...")
    input()
    
    try:
        # 基础鼠标移动测试
        test_mouse_movement()
        
        print("\n按Enter继续完整流程测试...")
        input()
        
        # 完整流程测试
        test_complete_flow()
        
        print("\n🎉 所有测试完成！")
        print("如果鼠标行为正常，说明修复成功。")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
    
    print("\n测试结束。")

if __name__ == "__main__":
    main()