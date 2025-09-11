# 监控程序API接口使用说明

## 概述

增强版Trae IDE监控程序现在支持HTTP API接口，允许其他程序通过网络请求来控制监控程序的运行状态。

## 启动方式

### 普通模式（原有方式）
```bash
python enhanced_trae_ide_monitor.py
```

### API模式（新增）
```bash
python enhanced_trae_ide_monitor.py --api
```

API模式会同时启动：
- 监控程序主循环（在后台线程运行）
- HTTP API服务器（默认端口5000）

## API接口列表

### 1. 获取监控状态
- **URL**: `GET /status`
- **描述**: 获取当前监控程序的运行状态
- **响应示例**:
```json
{
  "running": true,
  "paused": false,
  "thread_alive": true
}
```

### 2. 启动监控
- **URL**: `POST /start`
- **描述**: 启动监控程序（如果未运行）
- **响应示例**:
```json
{
  "message": "监控已启动",
  "success": true
}
```

### 3. 停止监控
- **URL**: `POST /stop`
- **描述**: 完全停止监控程序
- **响应示例**:
```json
{
  "message": "监控已停止",
  "success": true
}
```

### 4. 暂停监控
- **URL**: `POST /pause`
- **描述**: 暂停监控程序（保持线程运行但跳过监控逻辑）
- **响应示例**:
```json
{
  "message": "监控已暂停",
  "success": true
}
```

### 5. 恢复监控
- **URL**: `POST /resume`
- **描述**: 恢复已暂停的监控程序
- **响应示例**:
```json
{
  "message": "监控已恢复",
  "success": true
}
```

### 6. 重启监控
- **URL**: `POST /restart`
- **描述**: 重启监控程序（停止当前线程并启动新线程）
- **响应示例**:
```json
{
  "message": "监控已重启",
  "success": true
}
```

### 7. 窗口管理测试（同步）
- **URL**: `POST /test/window-management`
- **描述**: 测试窗口管理功能（激活Trae IDE窗口 → 等待3秒 → 最小化窗口）
- **用途**: 验证窗口操作功能，可在监控暂停期间使用
- **响应示例**:
```json
{
  "success": true,
  "message": "窗口管理测试完成",
  "steps": [
    {"step": 1, "action": "激活窗口", "status": "success"},
    {"step": 2, "action": "等待3秒", "status": "success"},
    {"step": 3, "action": "最小化窗口", "status": "success"}
  ]
}
```

### 8. 窗口管理测试（异步）
- **URL**: `POST /test/window-management-async`
- **描述**: 在独立线程中异步执行窗口管理测试
- **用途**: 不阻塞API响应，适合在监控暂停期间运行独立任务
- **响应示例**:
```json
{
  "success": true,
  "message": "异步窗口管理测试已启动，请查看控制台输出"
}
```

## 使用示例

### 基本控制流程
```bash
# 1. 启动API模式
python enhanced_trae_ide_monitor.py --api

# 2. 在另一个终端或程序中调用API
curl -X GET http://localhost:5000/status
curl -X POST http://localhost:5000/pause
curl -X POST http://localhost:5000/test/window-management
curl -X POST http://localhost:5000/resume
```

### 窗口管理测试场景
```bash
# 暂停监控
curl -X POST http://localhost:5000/pause

# 执行窗口管理测试
curl -X POST http://localhost:5000/test/window-management

# 恢复监控
curl -X POST http://localhost:5000/resume
```

## 技术特性

### 窗口管理测试功能
- **同步测试**: 直接在API请求中完成窗口操作，返回详细的执行步骤
- **异步测试**: 在独立线程中执行，不阻塞API响应，适合长时间运行的任务
- **复用性**: 可在监控暂停期间独立使用窗口管理功能
- **容错性**: 包含完整的错误处理和状态检查

### 应用场景
1. **调试窗口操作**: 验证窗口激活和最小化功能是否正常
2. **独立RPA任务**: 在监控暂停期间执行其他自动化任务
3. **系统集成**: 与其他程序协同工作，控制Trae IDE窗口状态

## Python客户端示例

```python
import requests

# 基础URL
base_url = 'http://127.0.0.1:5000'

# 获取状态
response = requests.get(f'{base_url}/status')
print(response.json())

# 暂停监控
response = requests.post(f'{base_url}/pause')
print(response.json())

# 执行窗口管理测试（同步）
response = requests.post(f'{base_url}/test/window-management')
print(response.json())

# 执行窗口管理测试（异步）
response = requests.post(f'{base_url}/test/window-management-async')
print(response.json())

# 恢复监控
response = requests.post(f'{base_url}/resume')
print(response.json())

# 重启监控
response = requests.post(f'{base_url}/restart')
print(response.json())
```

### curl命令示例

```bash
# 获取状态
curl http://127.0.0.1:5000/status

# 暂停监控
curl -X POST http://127.0.0.1:5000/pause

# 执行窗口管理测试（同步）
curl -X POST http://127.0.0.1:5000/test/window-management

# 执行窗口管理测试（异步）
curl -X POST http://127.0.0.1:5000/test/window-management-async

# 恢复监控
curl -X POST http://127.0.0.1:5000/resume

# 重启监控
curl -X POST http://127.0.0.1:5000/restart
```

## 配置说明

API服务器的配置可以在`config.json`中设置：

```json
{
  "api_host": "127.0.0.1",
  "api_port": 5000,
  "其他配置项": "..."
}
```

- `api_host`: API服务器监听的IP地址（默认：127.0.0.1）
- `api_port`: API服务器监听的端口（默认：5000）

## 安全注意事项

1. **本地访问**: 默认配置只允许本机访问（127.0.0.1）
2. **防火墙**: 如需远程访问，请确保防火墙设置正确
3. **权限控制**: 当前版本未实现身份验证，请在受信任的网络环境中使用

## 错误处理

所有API接口都会返回JSON格式的响应。如果操作失败，响应中会包含错误信息：

```json
{
  "message": "错误描述",
  "success": false
}
```

## 客户端工具

项目中包含了一个示例客户端程序 `monitor_api_client.py`，可以直接运行来测试API功能：

```bash
python monitor_api_client.py
```

这个客户端会演示所有API接口的使用方法。