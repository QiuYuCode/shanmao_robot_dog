# 山猫 M20 pro 组件测试命令

用于测试山猫 M20 pro 机械狗的外围组件是否正常工作的命令和示例代码

> 当前 GOS 系统环境已预装用于管理 python 的开发环境工具 uv
> 
> python 虚拟环境版本使用的 3.9, 如果需要使用不同版本的 python，建议使用 uv 创建不同的环境
> 
> [uv 中文使用说明文档](https://uv.oaix.tech/guides/)
> 
> 如果你需要在其他环境安装 uv 迁移该项目，建议参考国内安装 uv 的方法，确保环境依赖的一致性
> 
> [uv 国内安装脚本](https://gitee.com/wangnov/uv-custom/releases)

运行测试代码前，请运行 `source .venv/bin/activate` 激活虚拟环境
或在不激活虚拟环境，当前目录中，直接使用 uv 命令运行相关测试代码

例如：
```bash
uv run main.py
```

## 一、深度相机

### 命令行使用

拍照
```bash
ffmpeg -f v4l2 -i /dev/video4 -frames:v 1 image_test.jpg
```

录像
```bash
ffmpeg -f v4l2 -i /dev/video4 -t 10 test_video.mkv
```

### Python 使用

项目已包含 `examples/depth_camera_example.py` 示例代码，使用 `pyrealsense2` 进行深度相机操作。

**基本使用：**

```python
from examples.depth_camera_example import capture_image, record_video, show_live_stream

# 拍摄图像（彩色和深度）
capture_image()

# 录制视频（默认10秒）
record_video(duration=10)

# 实时显示
show_live_stream()
```

**运行示例代码：**

```bash
# 拍摄图像
uv run examples/depth_camera_example.py capture

# 录制视频（10秒）
uv run examples/depth_camera_example.py record 10

# 实时显示
uv run examples/depth_camera_example.py live
```

**依赖说明：**

项目使用 `pyrealsense2` 和 `opencv-python`，已包含在项目依赖中。

详细文档请参考：[pyrealsense2 使用文档](https://github.com/realsenseai/librealsense/tree/master/doc)

## 二、麦克风扬声器

### 命令行使用

检查命令
```bash
sudo arecord -l  # 查看麦克风
sudo aplay -l    # 查看扬声器
```

录制音频
```bash
# 录制
sudo arecord -D plughw:1,0 -r 16000 -c 1 -f S16_LE -d 5 mic_test.wav
# 播放
sudo aplay mic_test.wav
```

直接测试扬声器
```bash
# -c 2 (双声道), -t wav (测试音), -l 1 (循环1次)
sudo speaker-test -c 2 -t wav -l 1
```

### Python 使用

项目已包含 `examples/audio_example.py` 示例代码，使用 `pyaudio` 进行音频录制和播放。

**系统依赖：**

使用 pyaudio 模块前需要安装系统依赖 portaudio19-dev

```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev
```

**基本使用：**

```python
from examples.audio_example import list_audio_devices, record_audio, play_audio

# 列出所有音频设备
list_audio_devices()

# 录制音频（5秒，16000Hz，单声道）
record_audio("recording.wav", duration=5, sample_rate=16000, channels=1)

# 播放音频
play_audio("recording.wav")
```

**运行示例代码：**

```bash
# 列出音频设备
uv run examples/audio_example.py list

# 录制音频（默认5秒）
uv run examples/audio_example.py record recording.wav 5

# 播放音频
uv run examples/audio_example.py play recording.wav

# 录制并播放测试
uv run examples/audio_example.py test 5
```

**依赖说明：**

项目使用 `pyaudio` 模块，已包含在项目依赖中。

## 三、红外热成像

### 命令行使用

录制视频
```bash
ffmpeg -rtsp_transport tcp -i "rtsp://admin:yoseen2018@10.21.31.201:554/h264" -c copy output.mp4
## 或者
ffmpeg -rtsp_transport udp -i "rtsp://admin:yoseen2018@10.21.31.201:554/h264" -c copy output.mp4
```

### Python 使用

项目已包含 `examples/thermal_camera_example.py` 示例代码，使用 `opencv-python` 通过 RTSP 流获取热成像视频。

**基本使用：**

```python
from examples.thermal_camera_example import capture_frame, record_video, show_live_stream

rtsp_url = "rtsp://admin:yoseen2018@10.21.31.201:554/h264"

# 捕获一帧图像
capture_frame(rtsp_url, "thermal_image.jpg")

# 录制视频（10秒）
record_video(rtsp_url, "thermal_video.mp4", duration=10)

# 实时显示
show_live_stream(rtsp_url)
```

**运行示例代码：**

```bash
# 捕获一帧图像
uv run examples/thermal_camera_example.py capture "rtsp://admin:yoseen2018@10.21.31.201:554/h264" thermal_image.jpg

# 录制视频（10秒）
uv run examples/thermal_camera_example.py record "rtsp://admin:yoseen2018@10.21.31.201:554/h264" thermal_video.mp4 10

# 实时显示
uv run examples/thermal_camera_example.py live "rtsp://admin:yoseen2018@10.21.31.201:554/h264"
```

**依赖说明：**

项目使用 `opencv-python` 模块，已包含在项目依赖中。

## 温湿度模块

温湿度模块通过云平台 API 获取实时温湿度数据。

### Python 使用

项目已包含 `examples/temperature_humidity_api.py` 示例代码，提供了完整的 API 客户端封装。

**基本使用：**

```python
from examples.temperature_humidity_api import TemperatureHumidityAPI

# 初始化 API 客户端
api = TemperatureHumidityAPI()

# 1. 获取 Token（需要用户名和密码）
token_data = api.get_token("your_username", "your_password")

# 2. 获取设备分组列表
groups = api.get_group_list()

# 3. 查询实时数据（可指定分组ID）
real_time_data = api.get_real_time_data(group_id="your_group_id")
```

**运行示例代码：**

```bash
uv run examples/temperature_humidity_api.py
```

**API 接口说明：**

- `get_token(login_name, password)`: 根据用户名和密码获取访问 Token
- `get_group_list()`: 获取设备分组列表
- `get_real_time_data(group_id=None)`: 查询实时温湿度数据，可指定分组ID过滤

**依赖说明：**

项目使用 `requests` 模块发起 HTTP 请求，已包含在项目依赖中。如果未安装，运行：

```bash
uv add requests
```

## 四、机械臂

### Python 使用

项目已包含 `examples/arm_example.py` 示例代码，使用 `piper-sdk` 控制机械臂。

**系统准备：**

使用前需要先激活 CAN 设备：

```bash
# 激活 CAN 设备（以 can0 为例，波特率 1000000）
sudo ip link set can0 up type can bitrate 1000000

# 检查 CAN 设备状态
ip link show can0
```

**基本使用：**

```python
from examples.arm_example import basic_control_example, get_status_example, use_v1_interface_example

# 基础控制示例（连接、获取状态和关节信息）
# can_name 参数指定 CAN 设备名称，默认为 'can0'
basic_control_example(can_name='can0')

# 获取机械臂状态示例
get_status_example(can_name='can0')

# 使用 V1 接口示例
use_v1_interface_example(can_name='can0')
```

**运行示例代码：**

```bash
# 基础控制示例（使用默认 can0）
uv run examples/arm_example.py basic

# 基础控制示例（指定 CAN 设备）
uv run examples/arm_example.py basic can1

# 获取状态示例
uv run examples/arm_example.py status

# 使用 V1 接口示例
uv run examples/arm_example.py v1
```

**依赖说明：**

项目使用 `piper-sdk` 模块，已包含在项目依赖中。

**注意事项：**

1. **CAN 设备激活**：使用前必须先激活 CAN 设备，否则会连接失败
2. **从臂模式**：机械臂需要处在从臂模式下才能读取反馈数据
3. **CAN 设备名称**：根据实际硬件配置修改 `can_name` 参数（默认为 'can0'）
4. **接口选择**：推荐使用 V2 接口（`C_PiperInterface_V2`），功能更完善
5. **连接参数**：代码中已设置默认参数（波特率 1000000），如需修改请参考代码注释

**详细文档：**

- [Piper 机械臂 SDK使用说明](https://github.com/agilexrobotics/piper_sdk/blob/master/README(ZH).MD)

## 五、灵巧手