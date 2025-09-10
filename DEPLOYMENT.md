# 部署说明文档

## 依赖安装问题分析

### 问题原因

刚才 `pip install -r requirements.txt` 报错的主要原因：

1. **版本固定过严格**：使用 `==` 固定版本号可能导致与当前Python版本或系统环境不兼容
2. **pywin32依赖问题**：pywin32是Windows专用库，在其他平台会导致安装失败
3. **依赖冲突**：某些包的特定版本之间可能存在依赖冲突
4. **构建工具问题**：部分包需要编译，可能缺少必要的构建工具

### 解决方案

#### 1. 使用灵活版本范围

原来的固定版本：
```
pyautogui==0.9.54
numpy==1.24.3
```

改为版本范围：
```
pyautogui>=0.9.50
numpy>=1.24.0
```

#### 2. 平台特定依赖

- `requirements.txt` - 跨平台通用依赖
- `requirements-windows.txt` - Windows专用依赖（包含pywin32）

## 部署指南

### Windows环境部署

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装Windows专用依赖
pip install -r requirements-windows.txt
```

### Linux/macOS环境部署

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装跨平台依赖
pip install -r requirements.txt
```

### 分步安装（推荐）

如果直接安装requirements文件失败，可以分步安装：

```bash
# 1. 安装核心依赖
pip install pyautogui opencv-python Pillow numpy pyperclip

# 2. 安装Web框架依赖
pip install Flask Flask-CORS requests

# 3. Windows环境额外安装
pip install pywin32  # 仅Windows需要
```

### 常见问题解决

#### 1. 编译错误

如果遇到编译错误，尝试安装预编译版本：
```bash
pip install --only-binary=all package_name
```

#### 2. 网络问题

使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 3. 权限问题

使用用户安装：
```bash
pip install --user -r requirements.txt
```

## 测试部署

安装完成后，测试程序是否正常运行：

```bash
# 测试基础功能
python enhanced_trae_ide_monitor.py --help

# 测试API模式
python enhanced_trae_ide_monitor.py --api

# 测试API客户端
python monitor_api_client.py
```

## 生产环境建议

1. **使用虚拟环境**：避免依赖冲突
2. **锁定依赖版本**：生产环境使用 `pip freeze > requirements-lock.txt`
3. **容器化部署**：使用Docker确保环境一致性
4. **监控日志**：配置适当的日志记录和监控

## Docker部署（可选）

创建 `Dockerfile`：
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "enhanced_trae_ide_monitor.py", "--api"]
```

构建和运行：
```bash
docker build -t trae-monitor .
docker run -p 5000:5000 trae-monitor
```