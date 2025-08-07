#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查安全位置坐标
分析当前设置的安全位置是否合适
"""

import pyautogui
import time

def check_safe_position():
    """
    检查当前安全位置的坐标
    """
    print("=== 安全位置坐标检查 ===")
    
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕尺寸: {screen_width} x {screen_height}")
    
    # 计算当前使用的安全位置
    safe_x = screen_width - 50
    safe_y = screen_height - 50
    
    print(f"\n当前安全位置坐标: ({safe_x}, {safe_y})")
    print(f"距离屏幕右边缘: 50 像素")
    print(f"距离屏幕下边缘: 50 像素")
    
    # 分析可能的问题
    print("\n=== 潜在问题分析 ===")
    print("屏幕右下角 (screen_width-50, screen_height-50) 可能存在的控件:")
    print("1. Windows 任务栏通知区域")
    print("2. 系统托盘图标")
    print("3. 时间显示区域")
    print("4. 输入法状态栏")
    print("5. 其他系统级悬浮控件")
    
    # 建议更安全的位置
    print("\n=== 建议的替代位置 ===")
    
    # 选项1: 屏幕中央偏右上
    alt1_x = screen_width - 200
    alt1_y = 100
    print(f"选项1 - 右上角安全区: ({alt1_x}, {alt1_y})")
    
    # 选项2: 屏幕左下角
    alt2_x = 50
    alt2_y = screen_height - 100
    print(f"选项2 - 左下角安全区: ({alt2_x}, {alt2_y})")
    
    # 选项3: 屏幕中央
    alt3_x = screen_width // 2
    alt3_y = screen_height // 2
    print(f"选项3 - 屏幕中央: ({alt3_x}, {alt3_y})")
    
    # 选项4: 更远离边缘的右下角
    alt4_x = screen_width - 150
    alt4_y = screen_height - 150
    print(f"选项4 - 远离边缘的右下角: ({alt4_x}, {alt4_y})")
    
    return safe_x, safe_y

def test_mouse_positions():
    """
    测试不同位置的鼠标移动效果
    """
    print("\n=== 鼠标位置测试 ===")
    print("将依次测试不同的安全位置，观察是否触发其他控件")
    print("按Enter开始测试...")
    input()
    
    screen_width, screen_height = pyautogui.size()
    
    positions = [
        ("当前位置 (右下角-50)", screen_width - 50, screen_height - 50),
        ("右上角安全区", screen_width - 200, 100),
        ("左下角安全区", 50, screen_height - 100),
        ("屏幕中央", screen_width // 2, screen_height // 2),
        ("远离边缘的右下角", screen_width - 150, screen_height - 150)
    ]
    
    for name, x, y in positions:
        print(f"\n测试 {name}: ({x}, {y})")
        print("移动鼠标到此位置...")
        pyautogui.moveTo(x, y)
        print(f"鼠标已移动到 ({x}, {y})")
        print("观察是否有控件被触发，然后按Enter继续...")
        input()
    
    print("\n测试完成！")

def main():
    """
    主函数
    """
    print("安全位置坐标检查工具")
    print("=" * 40)
    
    # 检查当前安全位置
    current_x, current_y = check_safe_position()
    
    print("\n是否要进行鼠标位置测试？(y/n): ", end="")
    choice = input().lower().strip()
    
    if choice == 'y' or choice == 'yes':
        test_mouse_positions()
    
    print("\n=== 总结 ===")
    print(f"当前安全位置: ({current_x}, {current_y})")
    print("如果此位置触发了其他控件，建议修改为:")
    print("1. 屏幕中央 (最安全，但可能影响用户操作)")
    print("2. 左下角安全区 (避开任务栏)")
    print("3. 右上角安全区 (远离任务栏和托盘)")
    print("4. 距离边缘更远的位置")

if __name__ == "__main__":
    main()