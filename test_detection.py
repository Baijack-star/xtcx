#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证图像识别功能
用于测试是否能正确识别目标按钮
"""

import pyautogui
import cv2
import numpy as np
import os

def test_button_detection():
    """
    测试按钮检测功能
    """
    target_button_path = "dd.PNG"
    match_threshold = 0.95  # 提高阈值，要求更精确的匹配
    
    print("=== Trae IDE监控器 - 检测测试 ===")
    print(f"目标按钮图片: {target_button_path}")
    print(f"匹配阈值: {match_threshold}")
    print()
    
    # 检查目标图片是否存在
    if not os.path.exists(target_button_path):
        print(f"❌ 错误: 找不到目标按钮图片 {target_button_path}")
        return False
    
    try:
        # 截取全屏
        print("📸 正在截取屏幕...")
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # 读取目标按钮图片
        print("🔍 正在加载目标按钮图片...")
        target_img = cv2.imread(target_button_path)
        if target_img is None:
            print(f"❌ 错误: 无法读取目标按钮图片 {target_button_path}")
            return False
        
        print(f"📏 屏幕尺寸: {screenshot_cv.shape[1]}x{screenshot_cv.shape[0]}")
        print(f"📏 目标图片尺寸: {target_img.shape[1]}x{target_img.shape[0]}")
        
        # 模板匹配
        print("🔎 正在进行模板匹配...")
        result = cv2.matchTemplate(screenshot_cv, target_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        print(f"📊 匹配结果:")
        print(f"   最大匹配度: {max_val:.4f}")
        print(f"   匹配位置: {max_loc}")
        print(f"   阈值: {match_threshold}")
        
        # 判断是否找到目标
        if max_val >= match_threshold:
            h, w = target_img.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            
            print(f"✅ 成功找到目标按钮!")
            print(f"   按钮中心坐标: ({center_x}, {center_y})")
            print(f"   匹配度: {max_val:.4f}")
            
            # 可选：保存标记了检测结果的图片
            marked_img = screenshot_cv.copy()
            cv2.rectangle(marked_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            cv2.circle(marked_img, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.imwrite("detection_result.png", marked_img)
            print(f"💾 检测结果已保存到 detection_result.png")
            
            return True
        else:
            print(f"❌ 未找到目标按钮")
            print(f"   当前匹配度 {max_val:.4f} 低于阈值 {match_threshold}")
            print(f"   可能原因:")
            print(f"   - 目标按钮不在当前屏幕上")
            print(f"   - 按钮外观发生了变化")
            print(f"   - 需要调整匹配阈值")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("开始测试...")
    print("请确保Trae IDE在屏幕上可见，然后按Enter继续...")
    input()
    
    success = test_button_detection()
    
    print()
    if success:
        print("🎉 测试通过！监控器应该能正常工作。")
    else:
        print("⚠️  测试失败，请检查配置或目标图片。")
    
    print("\n测试完成。")

if __name__ == "__main__":
    main()