#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试用的pp.PNG和kk.PNG图像文件
"""

import cv2
import numpy as np

def create_test_button_image(filename, text, color):
    """
    创建测试按钮图像
    """
    # 创建一个50x30像素的图像
    img = np.zeros((30, 50, 3), dtype=np.uint8)
    
    # 设置背景颜色
    img[:] = color
    
    # 添加文字
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_color = (255, 255, 255)  # 白色文字
    
    # 计算文字位置（居中）
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = (img.shape[0] + text_size[1]) // 2
    
    # 绘制文字
    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)
    
    # 添加边框
    cv2.rectangle(img, (0, 0), (img.shape[1]-1, img.shape[0]-1), (200, 200, 200), 1)
    
    # 保存图像
    cv2.imwrite(filename, img)
    print(f"✅ 已创建测试图像: {filename}")

def main():
    # 创建pp.PNG - 蓝色按钮
    create_test_button_image('pp.PNG', 'PP', (100, 50, 200))
    
    # 创建kk.PNG - 绿色按钮
    create_test_button_image('kk.PNG', 'KK', (50, 150, 50))
    
    print("\n测试图像创建完成！")
    print("pp.PNG: 蓝色按钮，文字'PP'")
    print("kk.PNG: 绿色按钮，文字'KK'")
    print("\n这些图像可用于测试繁忙状态下的按钮检测功能。")

if __name__ == "__main__":
    main()