#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版Trae IDE监控器
功能：
1. 自动检测并激活Trae IDE窗口（即使被最小化或遮挡）
2. 监控Trae IDE的运行状态，当检测到停止时自动输入"继续你的使命"并发送
3. 具备窗口管理功能，确保监控的可靠性
"""

import time
import pyautogui
import cv2
import numpy as np
from PIL import Image
import os
import win32gui
import win32con
import win32api
import pyperclip

class EnhancedTraeIDEMonitor:
    def __init__(self):
        # 监控间隔（秒）
        self.monitor_interval = 15
        
        # 目标按钮图片路径
        self.target_button_path = "dd.PNG"
        
        # 要输入的文本
        self.input_text = "继续你的使命"
        
        # 图像匹配阈值
        self.match_threshold = 0.95
        
        # Trae IDE窗口标题关键词
        self.trae_window_keywords = ["Trae", "trae", "IDE", "ide"]
        
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        print("增强版Trae IDE监控器已启动...")
        print(f"监控间隔: {self.monitor_interval}秒")
        print(f"目标文本: {self.input_text}")
        print("具备窗口自动激活功能")
        print("按Ctrl+C停止监控")
    
    def find_trae_window(self):
        """
        查找Trae IDE窗口
        返回: 窗口句柄或None
        """
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title:
                    # 检查窗口标题是否包含Trae相关关键词
                    for keyword in self.trae_window_keywords:
                        if keyword in window_title:
                            windows.append((hwnd, window_title))
                            break
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            print(f"找到 {len(windows)} 个可能的Trae窗口:")
            for hwnd, title in windows:
                print(f"  - {title}")
            # 返回第一个找到的窗口
            return windows[0][0]
        
        return None
    
    def activate_trae_window(self):
        """
        激活Trae IDE窗口
        返回: 是否成功激活
        """
        hwnd = self.find_trae_window()
        
        if not hwnd:
            print("❌ 未找到Trae IDE窗口")
            return False
        
        try:
            # 检查窗口是否最小化
            if win32gui.IsIconic(hwnd):
                print("🔄 检测到Trae IDE窗口被最小化，正在恢复...")
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(1)
            
            # 将窗口置于最前
            print("🔄 正在激活Trae IDE窗口...")
            win32gui.SetForegroundWindow(hwnd)
            
            # 最大化窗口以确保最佳检测效果
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            
            # 等待窗口状态稳定
            time.sleep(2)
            
            print("✅ Trae IDE窗口已激活并最大化")
            return True
            
        except Exception as e:
            print(f"❌ 激活窗口时发生错误: {e}")
            return False
    
    def minimize_trae_window(self):
        """
        将Trae IDE窗口最小化
        返回: 是否成功最小化
        """
        hwnd = self.find_trae_window()
        
        if not hwnd:
            print("❌ 未找到Trae IDE窗口，无法最小化")
            return False
        
        try:
            print("🔽 正在最小化Trae IDE窗口...")
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            time.sleep(1)
            print("✅ Trae IDE窗口已最小化")
            return True
            
        except Exception as e:
            print(f"❌ 最小化窗口时发生错误: {e}")
            return False
    
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
                print(f"❌ 错误: 找不到目标按钮图片 {self.target_button_path}")
                return None
            
            target_img = cv2.imread(self.target_button_path)
            if target_img is None:
                print(f"❌ 错误: 无法读取目标按钮图片 {self.target_button_path}")
                return None
            
            # 模板匹配
            result = cv2.matchTemplate(screenshot_cv, target_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= self.match_threshold:
                # 计算按钮中心坐标
                h, w = target_img.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return (center_x, center_y)
            
            return None
            
        except Exception as e:
            print(f"❌ 查找按钮时发生错误: {e}")
            return None
    
    def find_input_area(self, button_pos):
        """
        根据按钮位置计算输入框位置
        """
        # 使用固定坐标 (1670, 844)
        input_x = 1670
        input_y = 844
        
        print(f"按钮位置: {button_pos}, 使用固定输入框位置: ({input_x}, {input_y})")
        return (input_x, input_y)
    
    def send_message(self, button_pos):
        """
        发送消息到输入框
        """
        try:
            print("检测到Trae IDE需要激活，开始输入文本...")
            
            # 获取输入框位置
            input_pos = self.find_input_area(button_pos)
            
            # 点击输入框确保获得焦点
            pyautogui.click(input_pos[0], input_pos[1])
            time.sleep(0.5)
            
            # 再次点击确保焦点
            pyautogui.click(input_pos[0], input_pos[1])
            time.sleep(0.5)
            
            # 清空输入框内容
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.5)
            
            # 使用剪贴板输入文本（更可靠）
            print(f"正在输入文本: {self.input_text}")
            pyperclip.copy(self.input_text)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            
            print("文本输入完成")
            
            # 点击发送按钮
            pyautogui.click(button_pos[0], button_pos[1])
            time.sleep(1)
            
            print(f"已发送消息: {self.input_text}")
            return True
            
        except Exception as e:
            print(f"❌ 发送消息时发生错误: {e}")
            return False
    
    def monitor_loop(self):
        """
        主监控循环
        """
        try:
            while True:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在监控...")
                
                # 首先尝试激活Trae IDE窗口
                if not self.activate_trae_window():
                    print("⚠️  无法激活Trae IDE窗口，将在下次循环重试")
                    time.sleep(self.monitor_interval)
                    continue
                
                # 查找目标按钮
                button_pos = self.find_button_on_screen()
                
                if button_pos:
                    print(f"发现目标按钮位置: {button_pos}")
                    # 发送消息
                    if self.send_message(button_pos):
                        print("消息发送成功")
                        # 发送完成后最小化窗口，避免干扰桌面操作
                        self.minimize_trae_window()
                        print("等待下次监控...")
                    else:
                        print("消息发送失败")
                        # 即使发送失败也最小化窗口
                        self.minimize_trae_window()
                else:
                    print("未发现目标按钮，AI助手可能正在工作中...")
                    # 未发现按钮时也最小化窗口，避免干扰
                    self.minimize_trae_window()
                
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
    monitor = EnhancedTraeIDEMonitor()
    monitor.monitor_loop()

if __name__ == "__main__":
    main()