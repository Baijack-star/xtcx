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
- **描述**: 暂停监控程序（不退出，可恢复）
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
- **描述**: 重启监控程序（停止后重新启动）
- **响应示例**:
```json
{
  "message": "监控已重启",
  "success": true
}
```

## 使用示例

### Python客户端示例

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