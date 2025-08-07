# Trae IDE监控器

一个用于监控Trae IDE运行状态的自动化工具。当检测到IDE停止工作时，会自动输入"继续你的使命"并发送，以重新激活AI助手。

## 功能特点

- 🔍 **静默监控**: 后台运行，不干扰正常工作
- 🎯 **图像识别**: 通过截图和模板匹配检测目标按钮
- ⚡ **自动激活**: 检测到停止状态时自动发送激活消息
- 🕐 **定时监控**: 15秒间隔检测（可配置）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 确保 `dd.PNG` 文件在项目目录中（这是目标按钮的截图）

2. 测试检测功能：
```bash
python test_detection.py
```

3. **重要**: 如果出现误检测，请校准阈值：
```bash
python calibrate_threshold.py
```

4. 运行监控器：
```bash
python trae_ide_monitor.py
```

5. 按 `Ctrl+C` 停止监控

## 配置文件

项目现在支持通过 `config.json` 文件进行配置，无需修改代码。如果配置文件不存在，程序将使用默认设置。

### 配置文件结构

```json
{
  "monitor_settings": {
    "interval_seconds": 3
  },
  "message_settings": {
    "trigger_message": "继续你的使命"
  },
  "detection_settings": {
    "match_threshold": 0.8,
    "target_button_image": "target_button.png"
  },
  "position_settings": {
    "input_box_x": 1670,
    "input_box_y": 844,
    "safe_mouse_x": 1720,
    "safe_mouse_y": 100
  },
  "window_settings": {
    "auto_activate": true,
    "auto_minimize": true
  }
}
```

### 配置项说明

#### 监控设置 (monitor_settings)
- `interval_seconds`: 监控循环间隔时间（秒），默认3秒

#### 消息设置 (message_settings)
- `trigger_message`: 要发送的消息内容，默认"继续你的使命"

#### 检测设置 (detection_settings)
- `match_threshold`: 图像匹配阈值（0.0-1.0），默认0.8
- `target_button_image`: 目标按钮图像文件路径，默认"target_button.png"

#### 位置设置 (position_settings)
- `input_box_x`: 输入框 X 坐标，默认1670
- `input_box_y`: 输入框 Y 坐标，默认844
- `safe_mouse_x`: 安全鼠标位置 X 坐标，默认1720
- `safe_mouse_y`: 安全鼠标位置 Y 坐标，默认100

#### 窗口设置 (window_settings)
- `auto_activate`: 是否自动激活 Trae IDE 窗口，默认true
- `auto_minimize`: 是否自动最小化窗口，默认true

## 工作原理

1. 每15秒截取全屏画面
2. 使用OpenCV模板匹配查找目标按钮
3. 如果找到按钮，说明IDE处于停止状态
4. 自动点击输入框，输入激活文本，点击发送按钮
5. 如果未找到按钮，说明AI助手正在工作，继续等待

## 故障排除

### 误检测问题
如果监控器错误地将运行状态识别为停止状态：

1. 运行阈值校准工具：
```bash
python calibrate_threshold.py
```

2. 分别在停止状态和运行状态下测试匹配度
3. 选择合适的阈值（建议在两个状态匹配度之间）
4. 在 `trae_ide_monitor.py` 中修改 `match_threshold` 值

### 常见阈值设置
- **严格模式**: 0.95+ （避免误检测，但可能漏检）
- **平衡模式**: 0.85-0.94 （推荐）
- **宽松模式**: 0.80-0.84 （可能误检测）

## 注意事项

- 首次使用前请确保目标按钮截图 `dd.PNG` 准确
- 程序需要屏幕访问权限
- 建议在稳定的显示环境下使用
- 如果界面发生变化，可能需要重新截取目标按钮图片