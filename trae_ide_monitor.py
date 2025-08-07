#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae IDE监控器
功能：监控Trae IDE的运行状态，当检测到停止时自动输入"继续你的使命"并发送
"""

import time
import pyautogui
import cv2
import numpy as np
from PIL import Image
import os

class TraeIDEMonitor:
    def __init__(self):
        # 监控间隔（秒）
        self.monitor_interval = 15
        
        # 目标按钮图片路径
        self.target_button_path = "dd.PNG"
        
        # 要输入的文本
        self.input_text = "继续你的使命"
        
        # 图像匹配阈值（提高阈值以避免误检测）
        self.match_threshold = 0.95
        
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        print("Trae IDE监控器已启动...")
        print(f"监控间隔: {self.monitor_interval}秒")
        print(f"目标文本: {self.input_text}")
        print("按Ctrl+C停止监控")
    
    def find_button_on_screen(self):
        """
        在屏幕上查找目标按钮
        返回: (x, y) 坐标或 None
        """
        try:
            # 截取全屏
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # 读取目标按钮图片
            if not os.path.exists(self.target_button_path):
                print(f"错误: 找不到目标按钮图片 {self.target_button_path}")
                return None
                
            target_img = cv2.imread(self.target_button_path)
            if target_img is None:
                print(f"错误: 无法读取目标按钮图片 {self.target_button_path}")
                return None
            
            # 模板匹配
            result = cv2.matchTemplate(screenshot_cv, target_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # 如果匹配度超过阈值，返回坐标
            if max_val >= self.match_threshold:
                # 计算按钮中心坐标
                h, w = target_img.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return (center_x, center_y)
            
            return None
            
        except Exception as e:
            print(f"查找按钮时发生错误: {e}")
            return None
    
    def find_input_area(self, button_pos):
        """
        根据按钮位置查找输入框区域
        发送按钮在对话框右下角，输入框应该在按钮的左侧或上方
        """
        try:
            # 根据用户测试确定的精确坐标
            input_x = 1670
            input_y = 844
            
            print(f"按钮位置: {button_pos}, 使用固定输入框位置: ({input_x}, {input_y})")
            return (input_x, input_y)
            
        except Exception as e:
            print(f"查找输入框时发生错误: {e}")
            return None
    
    def send_message(self, button_pos):
        """
        在检测到目标按钮时，输入文本并发送
        """
        try:
            print("检测到Trae IDE需要激活，开始输入文本...")
            
            # 查找输入框位置
            input_pos = self.find_input_area(button_pos)
            if input_pos is None:
                print("错误: 无法找到输入框位置")
                return False
            
            # 点击输入框
            pyautogui.click(input_pos[0], input_pos[1])
            time.sleep(0.5)
            
            # 确保输入框获得焦点
            pyautogui.click(input_pos[0], input_pos[1])
            time.sleep(0.3)
            
            # 清空输入框（以防有残留文本）
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.2)
            
            # 使用剪贴板方式输入文本（更可靠）
            print(f"正在输入文本: {self.input_text}")
            import pyperclip
            pyperclip.copy(self.input_text)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            print("文本输入完成")
            
            # 点击发送按钮
            pyautogui.click(button_pos[0], button_pos[1])
            
            print(f"已发送消息: {self.input_text}")
            return True
            
        except Exception as e:
            print(f"发送消息时发生错误: {e}")
            return False
    
    def monitor_loop(self):
        """
        主监控循环
        """
        try:
            while True:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在监控...")
                
                # 查找目标按钮
                button_pos = self.find_button_on_screen()
                
                if button_pos:
                    print(f"发现目标按钮位置: {button_pos}")
                    # 发送消息
                    if self.send_message(button_pos):
                        print("消息发送成功，等待下次监控...")
                    else:
                        print("消息发送失败")
                else:
                    print("未发现目标按钮，AI助手可能正在工作中...")
                
                # 等待下次监控
                print(f"等待 {self.monitor_interval} 秒后继续监控...\n")
                time.sleep(self.monitor_interval)
                
        except KeyboardInterrupt:
            print("\n监控已停止")
        except Exception as e:
            print(f"监控过程中发生错误: {e}")

def main():
    """
    主函数
    """
    monitor = TraeIDEMonitor()
    monitor.monitor_loop()

if __name__ == "__main__":
    main()