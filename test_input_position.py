#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输入框位置测试脚本
用于测试和调整输入框的定位位置
"""

import pyautogui
import cv2
import numpy as np
import os
import time

def test_input_position():
    """
    测试输入框位置定位
    """
    target_button_path = "dd.PNG"
    match_threshold = 0.95
    
    print("=== 输入框位置测试 ===")
    print("这个脚本将帮助您找到正确的输入框位置")
    print()
    
    # 检查目标图片是否存在
    if not os.path.exists(target_button_path):
        print(f"❌ 错误: 找不到目标按钮图片 {target_button_path}")
        return False
    
    try:
        # 截取全屏并查找按钮
        print("📸 正在截取屏幕并查找发送按钮...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        target_img = cv2.imread(target_button_path)
        if target_img is None:
            print(f"❌ 错误: 无法读取目标按钮图片 {target_button_path}")
            return False
        
        # 模板匹配
        result = cv2.matchTemplate(screenshot_cv, target_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= match_threshold:
            h, w = target_img.shape[:2]
            button_center_x = max_loc[0] + w // 2
            button_center_y = max_loc[1] + h // 2
            button_pos = (button_center_x, button_center_y)
            
            print(f"✅ 找到发送按钮位置: {button_pos}")
            print()
            
            # 测试不同的输入框位置偏移
            offsets = [
                (-200, -20, "当前设置: 左侧200px, 上方20px"),
                (-150, -20, "测试1: 左侧150px, 上方20px"),
                (-250, -20, "测试2: 左侧250px, 上方20px"),
                (-200, 0, "测试3: 左侧200px, 同一水平线"),
                (-200, -40, "测试4: 左侧200px, 上方40px"),
                (-300, -30, "测试5: 左侧300px, 上方30px"),
            ]
            
            for i, (offset_x, offset_y, description) in enumerate(offsets):
                input_x = button_pos[0] + offset_x
                input_y = button_pos[1] + offset_y
                
                print(f"{i+1}. {description}")
                print(f"   计算位置: ({input_x}, {input_y})")
                
                # 询问用户是否要测试这个位置
                choice = input(f"   是否测试这个位置？(y/n/q退出): ").strip().lower()
                
                if choice == 'q':
                    break
                elif choice == 'y':
                    print(f"   正在点击位置 ({input_x}, {input_y})...")
                    
                    # 移动鼠标到目标位置（不点击，只是显示位置）
                    pyautogui.moveTo(input_x, input_y)
                    print(f"   鼠标已移动到计算位置，请查看是否在输入框内")
                    
                    test_click = input(f"   位置正确吗？如果正确请输入'click'进行点击测试: ").strip().lower()
                    
                    if test_click == 'click':
                        # 执行点击测试
                        pyautogui.click(input_x, input_y)
                        time.sleep(0.5)
                        
                        # 输入测试文本
                        test_text = "测试输入"
                        pyautogui.write(test_text)
                        
                        print(f"   已在位置 ({input_x}, {input_y}) 点击并输入测试文本")
                        print(f"   如果文本出现在正确的输入框中，这就是正确的位置！")
                        
                        # 询问是否要清除测试文本
                        clear = input(f"   是否清除测试文本？(y/n): ").strip().lower()
                        if clear == 'y':
                            pyautogui.hotkey('ctrl', 'a')
                            time.sleep(0.2)
                            pyautogui.press('delete')
                        
                        # 询问是否找到了正确位置
                        correct = input(f"   这是正确的输入框位置吗？(y/n): ").strip().lower()
                        if correct == 'y':
                            print(f"\n🎉 找到正确位置！")
                            print(f"请将以下代码更新到 trae_ide_monitor.py 的 find_input_area 方法中:")
                            print(f"input_x = button_pos[0] + {offset_x}")
                            print(f"input_y = button_pos[1] + {offset_y}")
                            return True
                
                print()
            
            print("测试完成。如果没有找到合适的位置，可能需要手动调整偏移值。")
            return False
            
        else:
            print(f"❌ 未找到发送按钮 (匹配度: {max_val:.4f} < {match_threshold})")
            print("请确保Trae IDE在屏幕上可见且发送按钮处于可检测状态")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("输入框位置测试工具")
    print("=" * 50)
    print("使用说明:")
    print("1. 确保Trae IDE在屏幕上可见")
    print("2. 确保对话框处于可见状态")
    print("3. 脚本会测试不同的输入框位置")
    print("4. 选择合适的位置进行点击测试")
    print("=" * 50)
    print()
    
    input("准备好后按Enter开始测试...")
    
    success = test_input_position()
    
    if not success:
        print("\n💡 提示:")
        print("如果所有预设位置都不正确，您可以:")
        print("1. 手动测量发送按钮到输入框的距离")
        print("2. 修改 trae_ide_monitor.py 中的偏移值")
        print("3. 重新运行此测试脚本验证")
    
    print("\n测试完成。")

if __name__ == "__main__":
    main()