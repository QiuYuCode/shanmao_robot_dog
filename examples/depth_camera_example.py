"""
深度相机基础示例
使用 pyrealsense2 进行深度相机操作
"""
import pyrealsense2 as rs
import numpy as np
import cv2


def capture_image():
    """拍摄一张彩色图像和深度图像"""
    # 配置深度和彩色流
    pipeline = rs.pipeline()
    config = rs.config()
    
    # 启用彩色流
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    # 启用深度流
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    # 启动流
    pipeline.start(config)
    
    try:
        # 等待一帧数据（让相机稳定）
        for _ in range(30):
            pipeline.wait_for_frames()
        
        # 获取帧
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        
        if not color_frame or not depth_frame:
            print("无法获取帧数据")
            return
        
        # 转换为 numpy 数组
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        
        # 保存彩色图像
        cv2.imwrite("color_image.jpg", color_image)
        print("彩色图像已保存: color_image.jpg")
        
        # 应用颜色映射到深度图像（用于可视化）
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03), 
            cv2.COLORMAP_JET
        )
        cv2.imwrite("depth_image.jpg", depth_colormap)
        print("深度图像已保存: depth_image.jpg")
        
    finally:
        # 停止流
        pipeline.stop()


def record_video(duration=10):
    """录制视频（彩色和深度）"""
    pipeline = rs.pipeline()
    config = rs.config()
    
    # 启用彩色流
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    # 启用深度流
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    # 启动流
    pipeline.start(config)
    
    # 创建视频写入器
    # 使用 mp4v 编码（与 MP4 容器格式兼容，避免 XVID 警告）
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    color_writer = cv2.VideoWriter('color_video.mp4', fourcc, 30.0, (640, 480))
    depth_writer = cv2.VideoWriter('depth_video.mp4', fourcc, 30.0, (640, 480))
    
    try:
        import time
        start_time = time.time()
        
        print(f"开始录制 {duration} 秒...")
        while time.time() - start_time < duration:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            
            if color_frame and depth_frame:
                color_image = np.asanyarray(color_frame.get_data())
                depth_image = np.asanyarray(depth_frame.get_data())
                
                # 应用颜色映射到深度图像
                depth_colormap = cv2.applyColorMap(
                    cv2.convertScaleAbs(depth_image, alpha=0.03),
                    cv2.COLORMAP_JET
                )
                
                color_writer.write(color_image)
                depth_writer.write(depth_colormap)
        
        print("录制完成")
        print("彩色视频已保存: color_video.mp4")
        print("深度视频已保存: depth_video.mp4")
        
    finally:
        color_writer.release()
        depth_writer.release()
        pipeline.stop()


def show_live_stream():
    """实时显示深度相机画面"""
    pipeline = rs.pipeline()
    config = rs.config()
    
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    pipeline.start(config)
    
    try:
        print("按 'q' 键退出")
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            
            if not color_frame or not depth_frame:
                continue
            
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            
            # 应用颜色映射到深度图像
            depth_colormap = cv2.applyColorMap(
                cv2.convertScaleAbs(depth_image, alpha=0.03),
                cv2.COLORMAP_JET
            )
            
            # 水平堆叠显示
            images = np.hstack((color_image, depth_colormap))
            cv2.imshow('深度相机 - 彩色 | 深度', images)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "capture":
            capture_image()
        elif mode == "record":
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            record_video(duration)
        elif mode == "live":
            show_live_stream()
        else:
            print("用法:")
            print("  python depth_camera_example.py capture  # 拍摄图像")
            print("  python depth_camera_example.py record [时长]  # 录制视频，默认10秒")
            print("  python depth_camera_example.py live  # 实时显示")
    else:
        # 默认拍摄图像
        capture_image()

