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
import json
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS

class EnhancedTraeIDEMonitor:
    def __init__(self, config_file="config.json"):
        # 加载配置文件
        self.load_config(config_file)
        
        # Trae IDE窗口标题关键词
        self.trae_window_keywords = ["Trae", "trae", "IDE", "ide"]
        
        # 线程控制变量
        self.monitor_running = False
        self.monitor_paused = False
        self.monitor_thread = None
        self.api_thread = None
        
        # API服务器配置
        self.api_port = getattr(self, 'api_port', 5000)
        self.api_host = getattr(self, 'api_host', '127.0.0.1')
        
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        print("增强版Trae IDE监控器已启动...")
        print(f"监控间隔: {self.monitor_interval}秒")
        print(f"目标文本: {self.input_text}")
        print(f"匹配阈值: {self.match_threshold}")
        print("具备窗口自动激活功能")
        print("按Ctrl+C停止监控")
    
    def load_config(self, config_file):
        """
        加载配置文件
        """
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 监控设置
                self.monitor_interval = config.get('monitor_settings', {}).get('interval_seconds', 15)
                
                # 消息设置
                self.input_text = config.get('message_settings', {}).get('trigger_message', '继续你的使命')
                
                # 检测设置
                detection_settings = config.get('detection_settings', {})
                self.match_threshold = detection_settings.get('match_threshold', 0.95)
                self.target_button_path = detection_settings.get('target_button_image', 'dd.PNG')
                self.busy_state_images = detection_settings.get('busy_state_images', ['pp.PNG', 'kk.PNG'])
                
                # 位置设置
                position_settings = config.get('position_settings', {})
                self.input_box_x = position_settings.get('input_box_x', 1670)
                self.input_box_y = position_settings.get('input_box_y', 844)
                self.safe_mouse_x = position_settings.get('safe_mouse_x', 1720)
                self.safe_mouse_y = position_settings.get('safe_mouse_y', 100)
                
                # 窗口设置
                window_settings = config.get('window_settings', {})
                self.auto_minimize = window_settings.get('auto_minimize', True)
                self.auto_activate = window_settings.get('auto_activate', True)
                
                print(f"✅ 配置文件 {config_file} 加载成功")
            else:
                print(f"⚠️  配置文件 {config_file} 不存在，使用默认配置")
                self.use_default_config()
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            print("使用默认配置")
            self.use_default_config()
    
    def use_default_config(self):
        """
        使用默认配置
        """
        self.monitor_interval = 15
        self.input_text = "继续你的使命"
        self.match_threshold = 0.95
        self.target_button_path = "dd.PNG"
        self.busy_state_images = ['pp.PNG', 'kk.PNG']
        self.input_box_x = 1670
        self.input_box_y = 844
        self.safe_mouse_x = 1720
        self.safe_mouse_y = 100
        self.auto_minimize = True
        self.auto_activate = True
    
    def find_trae_window(self):
        """
        查找Trae IDE窗口
        返回: 窗口句柄或None
        """
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title:
                    # 更精确的Trae窗口识别逻辑
                    if self._is_trae_window(window_title):
                        windows.append((hwnd, window_title))
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
    
    def _is_trae_window(self, window_title):
        """
        判断窗口标题是否为Trae IDE窗口
        使用更精确的匹配规则，避免误识别
        """
        window_title_lower = window_title.lower()
        
        # 排除明显不是Trae的窗口
        exclude_keywords = [
            '命令提示符', 'cmd', 'powershell', 'terminal',
            'chrome', 'firefox', 'edge', 'browser',
            'explorer', 'notepad', 'word', 'excel',
            'outlook', 'teams', 'zoom', 'skype'
        ]
        
        for exclude in exclude_keywords:
            if exclude in window_title_lower:
                return False
        
        # 精确匹配Trae IDE窗口
        # 1. 包含"Trae"且不包含其他应用名称
        if 'trae' in window_title_lower:
            # 确保是真正的Trae IDE窗口，而不是包含"trae"的其他窗口
            trae_indicators = [
                '- trae',  # 典型的Trae IDE窗口格式
                'trae -',  # 另一种格式
                'trae ide',  # 明确的IDE标识
                '.py - trae',  # Python文件在Trae中打开
                '.js - trae',  # JavaScript文件
                '.md - trae',  # Markdown文件
                '.json - trae',  # JSON文件
                '.txt - trae',  # 文本文件
            ]
            
            for indicator in trae_indicators:
                if indicator in window_title_lower:
                    return True
        
        return False
    
    def detect_interfering_windows(self):
        """
        检测可能干扰Trae IDE激活的窗口
        返回: 干扰窗口列表，包含窗口句柄、标题和当前状态
        """
        interfering_keywords = ["Chrome", "chrome", "Firefox", "firefox", "Edge", "edge", 
                               "浏览器", "Browser", "browser"]
        
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title:
                    for keyword in interfering_keywords:
                        if keyword in window_title:
                            # 记录窗口的当前状态
                            is_minimized = win32gui.IsIconic(hwnd)
                            placement = win32gui.GetWindowPlacement(hwnd)
                            # 检查是否最大化：placement[1] == win32con.SW_SHOWMAXIMIZED
                            is_maximized = placement[1] == win32con.SW_SHOWMAXIMIZED
                            
                            windows.append({
                                'hwnd': hwnd,
                                'title': window_title,
                                'is_minimized': is_minimized,
                                'is_maximized': is_maximized,
                                'placement': placement,
                                'was_foreground': win32gui.GetForegroundWindow() == hwnd
                            })
                            break
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows
    
    def handle_interfering_windows(self, restore_mode=False, saved_states=None):
        """
        智能处理干扰窗口，支持状态保存和恢复
        
        Args:
            restore_mode: 是否为恢复模式
            saved_states: 保存的窗口状态（恢复模式时使用）
        
        Returns:
            如果是保存模式，返回保存的窗口状态；如果是恢复模式，返回是否成功恢复
        """
        if restore_mode and saved_states:
            return self._restore_window_states(saved_states)
        else:
            return self._save_and_handle_interfering_windows()
    
    def _save_and_handle_interfering_windows(self):
        """
        保存干扰窗口状态并进行温和处理
        返回: 保存的窗口状态列表
        """
        interfering_windows = self.detect_interfering_windows()
        
        if not interfering_windows:
            return []
        
        print(f"🔍 检测到 {len(interfering_windows)} 个可能的干扰窗口:")
        for window in interfering_windows:
            print(f"   - {window['title']} (最小化: {window['is_minimized']}, 最大化: {window['is_maximized']})")
        
        # 只处理当前在前台且未最小化的干扰窗口
        handled_windows = []
        for window in interfering_windows:
            if not window['is_minimized'] and window['was_foreground']:
                try:
                    print(f"🔽 温和处理干扰窗口: {window['title']}")
                    # 使用更温和的方式：将窗口置于后台而不是最小化
                    win32gui.SetWindowPos(window['hwnd'], win32con.HWND_BOTTOM, 0, 0, 0, 0, 
                                         win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
                    time.sleep(0.2)
                    handled_windows.append(window)
                except Exception as e:
                    print(f"   ⚠️  处理失败: {e}")
            else:
                # 记录但不处理已最小化或非前台的窗口
                handled_windows.append(window)
        
        return handled_windows
    
    def _restore_window_states(self, saved_states):
        """
        恢复窗口的原始状态
        
        Args:
            saved_states: 之前保存的窗口状态列表
        
        Returns:
            是否成功恢复所有窗口状态
        """
        if not saved_states:
            return True
        
        print(f"🔄 正在恢复 {len(saved_states)} 个窗口的原始状态...")
        success_count = 0
        
        for window in saved_states:
            try:
                hwnd = window['hwnd']
                # 检查窗口是否仍然存在
                if not win32gui.IsWindow(hwnd):
                    continue
                
                print(f"   🔄 恢复窗口: {window['title']}")
                
                # 恢复窗口位置和状态
                if window['was_foreground'] and not window['is_minimized']:
                    # 如果原来是前台窗口且未最小化，则恢复到前台
                    if window['is_maximized']:
                        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    else:
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    
                    # 尝试恢复为前台窗口（但不强制）
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                    except:
                        # 如果无法设置为前台，至少确保窗口可见
                        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0, 
                                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
                
                success_count += 1
                time.sleep(0.1)
                
            except Exception as e:
                print(f"   ⚠️  恢复窗口 {window['title']} 失败: {e}")
        
        print(f"✅ 成功恢复 {success_count}/{len(saved_states)} 个窗口状态")
        return success_count == len(saved_states)
    
    def activate_trae_window(self):
        """
        激活Trae IDE窗口（增强版，解决窗口焦点竞争问题）
        返回: 是否成功激活
        """
        hwnd = self.find_trae_window()
        
        if not hwnd:
            print("❌ 未找到Trae IDE窗口")
            return False
        
        try:
            # 获取当前前台窗口
            current_foreground = win32gui.GetForegroundWindow()
            current_title = win32gui.GetWindowText(current_foreground) if current_foreground else "未知"
            print(f"🔍 当前前台窗口: {current_title}")
            
            # 强制激活策略 - 多重尝试
            max_attempts = 3
            for attempt in range(max_attempts):
                print(f"🔄 尝试激活Trae IDE窗口 (第{attempt + 1}次)...")
                
                # 步骤1: 如果窗口最小化，先恢复
                if win32gui.IsIconic(hwnd):
                    print("   📤 恢复最小化窗口...")
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.5)
                
                # 步骤2: 强制显示窗口
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                time.sleep(0.3)
                
                # 步骤3: 尝试多种激活方法
                try:
                    # 方法1: 标准激活
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.3)
                    
                    # 方法2: 如果失败，使用更强力的方法
                    if win32gui.GetForegroundWindow() != hwnd:
                        print("   🔧 使用强制激活方法...")
                        # 模拟Alt+Tab切换（有时能绕过焦点限制）
                        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                        time.sleep(0.2)
                        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, 
                                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                        win32gui.SetForegroundWindow(hwnd)
                        time.sleep(0.3)
                    
                    # 方法3: 最后尝试点击窗口来激活
                    if win32gui.GetForegroundWindow() != hwnd:
                        print("   🖱️  尝试点击窗口激活...")
                        rect = win32gui.GetWindowRect(hwnd)
                        center_x = (rect[0] + rect[2]) // 2
                        center_y = (rect[1] + rect[3]) // 2
                        # 保存当前鼠标位置
                        original_pos = pyautogui.position()
                        # 点击窗口中心
                        pyautogui.click(center_x, center_y)
                        time.sleep(0.3)
                        # 恢复鼠标位置
                        pyautogui.moveTo(original_pos.x, original_pos.y)
                        
                except Exception as inner_e:
                    print(f"   ⚠️  激活方法异常: {inner_e}")
                
                # 步骤4: 最大化窗口
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                time.sleep(0.5)
                
                # 验证激活是否成功
                current_foreground = win32gui.GetForegroundWindow()
                if current_foreground == hwnd:
                    print(f"✅ Trae IDE窗口已成功激活并最大化 (第{attempt + 1}次尝试成功)")
                    return True
                else:
                    current_title = win32gui.GetWindowText(current_foreground) if current_foreground else "未知"
                    print(f"   ⚠️  激活失败，当前前台窗口仍为: {current_title}")
                    if attempt < max_attempts - 1:
                        print(f"   🔄 等待1秒后重试...")
                        time.sleep(1)
            
            print(f"❌ 经过{max_attempts}次尝试，仍无法激活Trae IDE窗口")
            print("💡 建议手动点击Trae IDE窗口或关闭干扰的应用程序")
            return False
            
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
    
    def find_busy_state_button(self):
        """
        在繁忙状态下查找特定的按钮图像（pp.PNG或kk.PNG）
        返回: (image_name, x, y) 或 None
        """
        try:
            # 截取全屏
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # 遍历检测每个繁忙状态图像
            for image_name in self.busy_state_images:
                if not os.path.exists(image_name):
                    print(f"⚠️  警告: 找不到繁忙状态图片 {image_name}")
                    continue
                
                target_img = cv2.imread(image_name)
                if target_img is None:
                    print(f"⚠️  警告: 无法读取繁忙状态图片 {image_name}")
                    continue
                
                # 模板匹配
                result = cv2.matchTemplate(screenshot_cv, target_img, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val >= self.match_threshold:
                    # 计算按钮中心坐标
                    h, w = target_img.shape[:2]
                    center_x = max_loc[0] + w // 2
                    center_y = max_loc[1] + h // 2
                    print(f"✅ 在繁忙状态下检测到 {image_name}，位置: ({center_x}, {center_y})，匹配度: {max_val:.3f}")
                    return (image_name, center_x, center_y)
            
            return None
            
        except Exception as e:
            print(f"❌ 查找繁忙状态按钮时发生错误: {e}")
            return None
    
    def find_input_area(self, button_pos):
        """
        根据按钮位置推算输入框位置或使用配置的固定位置
        """
        # 使用配置文件中的固定输入框位置
        print(f"按钮位置: {button_pos}, 使用固定输入框位置: ({self.input_box_x}, {self.input_box_y})")
        return (self.input_box_x, self.input_box_y)
    
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
            
            # 将鼠标移动到安全位置，避免hover效果遮挡按钮
            # 使用配置文件中的安全位置
            pyautogui.moveTo(self.safe_mouse_x, self.safe_mouse_y)
            time.sleep(0.5)
            
            print(f"已发送消息: {self.input_text}")
            print("🔄 鼠标已移动到安全位置，避免遮挡检测区域")
            return True
            
        except Exception as e:
            print(f"❌ 发送消息时发生错误: {e}")
            return False
    
    def monitor_loop(self):
        """
        主监控循环
        """
        try:
            self.monitor_running = True
            while self.monitor_running:
                # 检查是否暂停
                if self.monitor_paused:
                    print("[监控已暂停] 等待恢复...")
                    time.sleep(1)
                    continue
                    
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在监控...")
                
                # 保存干扰窗口状态的变量
                saved_window_states = None
                
                # 根据配置决定是否激活Trae IDE窗口
                if self.auto_activate:
                    # 首先保存并处理可能的干扰窗口
                    saved_window_states = self._save_and_handle_interfering_windows()
                    
                    # 然后尝试激活Trae IDE窗口
                    if not self.activate_trae_window():
                        print("⚠️  无法激活Trae IDE窗口，将在下次循环重试")
                        # 如果激活失败，恢复窗口状态
                        if saved_window_states:
                            self._restore_window_states(saved_window_states)
                        time.sleep(self.monitor_interval)
                        continue
                
                # 查找目标按钮
                button_pos = self.find_button_on_screen()
                
                if button_pos:
                    print(f"发现目标按钮位置: {button_pos}")
                    # 发送消息
                    if self.send_message(button_pos):
                        print("消息发送成功")
                        # 根据配置决定是否最小化窗口
                        if self.auto_minimize:
                            self.minimize_trae_window()
                        print("等待下次监控...")
                    else:
                        print("消息发送失败")
                        # 根据配置决定是否最小化窗口
                        if self.auto_minimize:
                            self.minimize_trae_window()
                else:
                    print("未发现目标按钮，AI助手可能正在工作中...")
                    
                    # 在繁忙状态下检测特定按钮
                    busy_button_result = self.find_busy_state_button()
                    if busy_button_result:
                        image_name, x, y = busy_button_result
                        print(f"🎯 检测到繁忙状态按钮 {image_name}，准备点击位置: ({x}, {y})")
                        
                        try:
                            # 点击检测到的按钮
                            pyautogui.click(x, y)
                            print(f"✅ 已点击 {image_name} 按钮")
                            time.sleep(1)  # 等待点击生效
                        except Exception as e:
                            print(f"❌ 点击 {image_name} 按钮时发生错误: {e}")
                    else:
                        print("未检测到任何繁忙状态按钮")
                    
                    # 根据配置决定是否最小化窗口
                    if self.auto_minimize:
                        self.minimize_trae_window()
                
                # 恢复之前保存的窗口状态
                if saved_window_states:
                    print("🔄 恢复其他应用的窗口状态...")
                    self._restore_window_states(saved_window_states)
                
                # 等待下次监控
                print(f"等待 {self.monitor_interval} 秒后继续监控...\n")
                time.sleep(self.monitor_interval)
                
        except KeyboardInterrupt:
            print("\n监控已停止")
        except Exception as e:
            print(f"监控过程中发生错误: {e}")
        finally:
            self.monitor_running = False
            print("监控循环已退出")
    
    def create_api_server(self):
        """
        创建API服务器
        """
        app = Flask(__name__)
        CORS(app)
        
        @app.route('/status', methods=['GET'])
        def get_status():
            """获取监控状态"""
            return jsonify({
                'running': self.monitor_running,
                'paused': self.monitor_paused,
                'thread_alive': self.monitor_thread.is_alive() if self.monitor_thread else False
            })
        
        @app.route('/start', methods=['POST'])
        def start_monitor():
            """启动监控"""
            if not self.monitor_running:
                self.monitor_thread = threading.Thread(target=self.monitor_loop)
                self.monitor_thread.daemon = True
                self.monitor_thread.start()
                return jsonify({'message': '监控已启动', 'success': True})
            else:
                return jsonify({'message': '监控已在运行中', 'success': False})
        
        @app.route('/stop', methods=['POST'])
        def stop_monitor():
            """停止监控"""
            self.monitor_running = False
            self.monitor_paused = False
            return jsonify({'message': '监控已停止', 'success': True})
        
        @app.route('/pause', methods=['POST'])
        def pause_monitor():
            """暂停监控"""
            if self.monitor_running:
                self.monitor_paused = True
                return jsonify({'message': '监控已暂停', 'success': True})
            else:
                return jsonify({'message': '监控未运行', 'success': False})
        
        @app.route('/resume', methods=['POST'])
        def resume_monitor():
            """恢复监控"""
            if self.monitor_running and self.monitor_paused:
                self.monitor_paused = False
                return jsonify({'message': '监控已恢复', 'success': True})
            else:
                return jsonify({'message': '监控未暂停或未运行', 'success': False})
        
        @app.route('/restart', methods=['POST'])
        def restart_monitor():
            """重启监控"""
            # 停止当前监控
            self.monitor_running = False
            self.monitor_paused = False
            
            # 等待线程结束
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=5)
            
            # 启动新的监控线程
            self.monitor_thread = threading.Thread(target=self.monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            return jsonify({'message': '监控已重启', 'success': True})
        
        return app
    
    def start_api_server(self):
        """
        启动API服务器
        """
        app = self.create_api_server()
        print(f"API服务器启动在 http://{self.api_host}:{self.api_port}")
        print("可用接口:")
        print("  GET  /status  - 获取监控状态")
        print("  POST /start   - 启动监控")
        print("  POST /stop    - 停止监控")
        print("  POST /pause   - 暂停监控")
        print("  POST /resume  - 恢复监控")
        print("  POST /restart - 重启监控")
        app.run(host=self.api_host, port=self.api_port, debug=False, use_reloader=False)
    
    def start_with_api(self):
        """
        启动监控器和API服务器
        """
        # 启动API服务器线程
        self.api_thread = threading.Thread(target=self.start_api_server)
        self.api_thread.daemon = True
        self.api_thread.start()
        
        # 启动监控线程
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        try:
            # 主线程等待
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n正在停止服务...")
            self.monitor_running = False
            self.monitor_paused = False

def main():
    """
    主函数
    """
    import sys
    
    monitor = EnhancedTraeIDEMonitor()
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == '--api':
        print("启动API模式...")
        monitor.start_with_api()
    else:
        print("启动普通模式...")
        monitor.monitor_loop()

if __name__ == "__main__":
    main()