#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监控程序API客户端示例
用于演示如何通过API接口控制监控程序
"""

import requests
import json
import time

class MonitorAPIClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.base_url = f'http://{host}:{port}'
        
    def get_status(self):
        """获取监控状态"""
        try:
            response = requests.get(f'{self.base_url}/status')
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def start_monitor(self):
        """启动监控"""
        try:
            response = requests.post(f'{self.base_url}/start')
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def stop_monitor(self):
        """停止监控"""
        try:
            response = requests.post(f'{self.base_url}/stop')
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def pause_monitor(self):
        """暂停监控"""
        try:
            response = requests.post(f'{self.base_url}/pause')
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def resume_monitor(self):
        """恢复监控"""
        try:
            response = requests.post(f'{self.base_url}/resume')
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def restart_monitor(self):
        """重启监控"""
        try:
            response = requests.post(f'{self.base_url}/restart')
            return response.json()
        except Exception as e:
            return {'error': str(e)}

def main():
    """演示API调用"""
    client = MonitorAPIClient()
    
    print("=== 监控程序API客户端演示 ===")
    print("\n1. 获取当前状态:")
    status = client.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))

    print("\n等待3秒...")
    time.sleep(3)
    
    print("\n2. 暂停监控:")
    result = client.pause_monitor()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n等待3秒...")
    time.sleep(3)
    
    #print("\n3. 恢复监控:")
    #result = client.resume_monitor()
    #print(json.dumps(result, indent=2, ensure_ascii=False))
    
    #print("\n4. 获取状态确认:")
    #status = client.get_status()
    #print(json.dumps(status, indent=2, ensure_ascii=False))
    
    #print("\n5. 重启监控:")
    #result = client.restart_monitor()
    #print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n演示完成！")

if __name__ == "__main__":
    main()