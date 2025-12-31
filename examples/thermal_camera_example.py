"""
红外热成像基础示例
使用 OpenCV 通过 RTSP 流获取热成像视频
"""
import cv2
import sys


def capture_frame(rtsp_url, output_file="thermal_image.jpg"):
    """
    从 RTSP 流中捕获一帧图像
    
    Args:
        rtsp_url: RTSP 流地址
        output_file: 输出文件名
    """
    # 使用 TCP 传输（更稳定）
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    if not cap.isOpened():
        print(f"错误: 无法连接到 RTSP 流: {rtsp_url}")
        return False
    
    print("正在捕获图像...")
    ret, frame = cap.read()
    
    if ret:
        cv2.imwrite(output_file, frame)
        print(f"图像已保存: {output_file}")
    else:
        print("错误: 无法读取帧数据")
    
    cap.release()
    return ret


def record_video(rtsp_url, output_file="thermal_video.mp4", duration=10):
    """
    录制 RTSP 视频流
    
    Args:
        rtsp_url: RTSP 流地址
        output_file: 输出文件名
        duration: 录制时长（秒）
    """
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    if not cap.isOpened():
        print(f"错误: 无法连接到 RTSP 流: {rtsp_url}")
        return False
    
    # 获取视频属性
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    print(f"开始录制 {duration} 秒...")
    print(f"分辨率: {width}x{height}, 帧率: {fps} fps")
    
    import time
    start_time = time.time()
    frame_count = 0
    
    try:
        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
                frame_count += 1
            else:
                print("警告: 无法读取帧")
                break
    except KeyboardInterrupt:
        print("\n录制被中断")
    finally:
        cap.release()
        out.release()
        print(f"录制完成，共 {frame_count} 帧")
        print(f"视频已保存: {output_file}")


def show_live_stream(rtsp_url):
    """
    实时显示 RTSP 视频流
    
    Args:
        rtsp_url: RTSP 流地址
    """
    # 使用 TCP 传输（更稳定）
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    if not cap.isOpened():
        print(f"错误: 无法连接到 RTSP 流: {rtsp_url}")
        return
    
    print("按 'q' 键退出")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("错误: 无法读取帧")
                break
            
            cv2.imshow('红外热成像', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("\n退出")
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # 默认 RTSP 地址（根据实际情况修改）
    default_rtsp_url = "rtsp://admin:yoseen2018@10.21.31.201:554/h264"
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python thermal_camera_example.py capture [rtsp_url] [输出文件]  # 捕获一帧")
        print("  python thermal_camera_example.py record [rtsp_url] [输出文件] [时长]  # 录制视频")
        print("  python thermal_camera_example.py live [rtsp_url]  # 实时显示")
        print(f"\n默认 RTSP 地址: {default_rtsp_url}")
        sys.exit(1)
    
    command = sys.argv[1]
    rtsp_url = sys.argv[2] if len(sys.argv) > 2 else default_rtsp_url
    
    if command == "capture":
        output_file = sys.argv[3] if len(sys.argv) > 3 else "thermal_image.jpg"
        capture_frame(rtsp_url, output_file)
    elif command == "record":
        output_file = sys.argv[3] if len(sys.argv) > 3 else "thermal_video.mp4"
        duration = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        record_video(rtsp_url, output_file, duration)
    elif command == "live":
        show_live_stream(rtsp_url)
    else:
        print(f"未知命令: {command}")

