#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的安全位置
验证修改后的安全位置是否能避免触发其他控件
"""

import pyautogui
import time

def test_new_safe_position():
    """
    测试新的安全位置
    """
    print("=== 新安全位置测试 ===")
    
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕尺寸: {screen_width} x {screen_height}")
    
    # 旧的安全位置
    old_safe_x = screen_width - 50
    old_safe_y = screen_height - 50
    print(f"\n旧安全位置: ({old_safe_x}, {old_safe_y}) - 右下角")
    
    # 新的安全位置（与代码中相同的逻辑）
    new_safe_x = screen_width - 200  # 距离右边缘200像素
    new_safe_y = 100  # 距离顶部100像素
    print(f"新安全位置: ({new_safe_x}, {new_safe_y}) - 右上角")
    
    print(f"\n位置变化:")
    print(f"X坐标: {old_safe_x} → {new_safe_x} (向左移动 {old_safe_x - new_safe_x} 像素)")
    print(f"Y坐标: {old_safe_y} → {new_safe_y} (向上移动 {old_safe_y - new_safe_y} 像素)")
    
    return new_safe_x, new_safe_y

def simulate_message_sending():
    """
    模拟完整的消息发送流程，包括新的安全位置移动
    """
    print("\n=== 模拟消息发送流程 ===")
    print("此测试将模拟完整的消息发送流程，包括最后的鼠标移动")
    print("按Enter开始模拟...")
    input()
    
    screen_width, screen_height = pyautogui.size()
    
    # 模拟点击输入框（屏幕中央偏左）
    print("1. 模拟点击输入框...")
    input_x = screen_width // 2 - 100
    input_y = screen_height // 2
    pyautogui.moveTo(input_x, input_y)
    time.sleep(1)
    print(f"   鼠标移动到输入框位置: ({input_x}, {input_y})")
    
    # 模拟点击发送按钮（屏幕中央偏右）
    print("2. 模拟点击发送按钮...")
    button_x = screen_width // 2 + 100
    button_y = screen_height // 2
    pyautogui.moveTo(button_x, button_y)
    time.sleep(1)
    print(f"   鼠标移动到发送按钮位置: ({button_x}, {button_y})")
    
    # 移动到新的安全位置
    print("3. 移动鼠标到新的安全位置...")
    safe_x = screen_width - 200
    safe_y = 100
    pyautogui.moveTo(safe_x, safe_y)
    time.sleep(0.5)
    print(f"   鼠标已移动到安全位置: ({safe_x}, {safe_y})")
    
    print("\n✅ 模拟流程完成！")
    print("请观察鼠标是否在右上角，以及是否触发了任何控件。")

def compare_positions():
    """
    比较新旧位置的优缺点
    """
    print("\n=== 位置比较分析 ===")
    
    print("旧位置 (右下角-50):")
    print("  优点: 远离主要工作区域")
    print("  缺点: 可能触发任务栏、系统托盘、时间显示等")
    print("  风险: 高 - 容易触发系统级控件")
    
    print("\n新位置 (右上角):")
    print("  优点: 避开任务栏和系统托盘区域")
    print("  优点: 远离主要编辑区域")
    print("  优点: 不太可能触发系统控件")
    print("  缺点: 可能接近窗口控制按钮（最小化、最大化、关闭）")
    print("  风险: 低 - 相对安全的区域")

def main():
    """
    主测试函数
    """
    print("新安全位置测试工具")
    print("=" * 40)
    
    # 显示新的安全位置信息
    new_x, new_y = test_new_safe_position()
    
    # 位置比较分析
    compare_positions()
    
    # 询问是否进行模拟测试
    print("\n是否要进行消息发送流程模拟？(y/n): ", end="")
    choice = input().lower().strip()
    
    if choice == 'y' or choice == 'yes':
        simulate_message_sending()
    
    print("\n=== 总结 ===")
    print(f"新安全位置: ({new_x}, {new_y})")
    print("修改目标: 避免触发任务栏和系统托盘控件")
    print("预期效果: 减少意外的控件显示和交互")
    print("\n如果新位置仍有问题，可以考虑:")
    print("1. 屏幕中央 (960, 523) - 最安全但可能影响用户")
    print("2. 左上角 (100, 100) - 完全避开右侧区域")
    print("3. 左下角 (50, 946) - 避开右侧但接近开始菜单")

if __name__ == "__main__":
    main()