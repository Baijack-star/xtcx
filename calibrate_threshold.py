#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阈值校准脚本
帮助用户找到合适的匹配阈值，以区分运行状态和停止状态的按钮
"""

import pyautogui
import cv2
import numpy as np
import os

def test_with_threshold(threshold):
    """
    使用指定阈值测试检测
    """
    target_button_path = "dd.PNG"
    
    try:
        # 截取全屏
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # 读取目标按钮图片
        target_img = cv2.imread(target_button_path)
        if target_img is None:
            return None, None
        
        # 模板匹配
        result = cv2.matchTemplate(screenshot_cv, target_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        return max_val, max_loc
        
    except Exception as e:
        print(f"错误: {e}")
        return None, None

def main():
    """
    主校准函数
    """
    print("=== Trae IDE监控器 - 阈值校准工具 ===")
    print()
    print("此工具将帮助您找到合适的匹配阈值")
    print("建议步骤:")
    print("1. 确保Trae IDE处于【停止状态】（显示发送按钮）")
    print("2. 运行测试，记录匹配度")
    print("3. 让Trae IDE进入【运行状态】（隐藏发送按钮）")
    print("4. 再次运行测试，记录匹配度")
    print("5. 选择一个介于两者之间的阈值")
    print()
    
    # 检查目标图片是否存在
    if not os.path.exists("dd.PNG"):
        print("❌ 错误: 找不到目标按钮图片 dd.PNG")
        return
    
    while True:
        print("\n请选择操作:")
        print("1. 测试当前屏幕状态")
        print("2. 推荐阈值设置")
        print("3. 退出")
        
        choice = input("请输入选择 (1-3): ").strip()
        
        if choice == "1":
            print("\n📸 正在检测当前屏幕...")
            max_val, max_loc = test_with_threshold(0.0)  # 使用最低阈值获取实际匹配度
            
            if max_val is not None:
                print(f"🔍 检测结果:")
                print(f"   匹配度: {max_val:.4f}")
                print(f"   位置: {max_loc}")
                
                # 提供阈值建议
                if max_val >= 0.98:
                    print(f"   状态判断: 很可能是【停止状态】（完全匹配）")
                elif max_val >= 0.90:
                    print(f"   状态判断: 可能是【停止状态】（高度匹配）")
                elif max_val >= 0.80:
                    print(f"   状态判断: 可能是【运行状态】（部分匹配）")
                else:
                    print(f"   状态判断: 很可能是【运行状态】或按钮不可见")
            else:
                print("❌ 检测失败")
                
        elif choice == "2":
            print("\n💡 阈值设置建议:")
            print("   - 如果停止状态匹配度 > 0.95，运行状态匹配度 < 0.90")
            print("     推荐阈值: 0.92-0.94")
            print("   - 如果停止状态匹配度 > 0.90，运行状态匹配度 < 0.85")
            print("     推荐阈值: 0.87-0.89")
            print("   - 当前程序设置: 0.95 (较严格)")
            print("\n⚠️  注意: 阈值太高可能导致漏检，太低可能导致误检")
            
        elif choice == "3":
            print("\n👋 校准完成，退出程序")
            break
            
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()