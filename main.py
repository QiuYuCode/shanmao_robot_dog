"""
山猫 M20 pro 组件测试主程序
提供统一的入口来使用各种组件的示例代码
"""
import sys
import argparse


def show_menu():
    """显示主菜单"""
    print("\n" + "=" * 60)
    print("山猫 M20 pro 组件测试菜单")
    print("=" * 60)
    print("1. 深度相机 (Depth Camera)")
    print("2. 麦克风扬声器 (Audio)")
    print("3. 红外热成像 (Thermal Camera)")
    print("4. 温湿度模块 (Temperature & Humidity)")
    print("0. 退出")
    print("=" * 60)


def run_depth_camera():
    """运行深度相机示例"""
    print("\n深度相机示例")
    print("-" * 60)
    print("可用命令:")
    print("  capture  - 拍摄图像（彩色和深度）")
    print("  record   - 录制视频（需要指定时长，如: record 10）")
    print("  live     - 实时显示")
    print("\n示例:")
    print("  python examples/depth_camera_example.py capture")
    print("  python examples/depth_camera_example.py record 10")
    print("  python examples/depth_camera_example.py live")
    
    choice = input("\n是否直接运行示例? (y/n): ").strip().lower()
    if choice == 'y':
        cmd = input("请输入命令 (capture/record/live): ").strip()
        if cmd == "capture":
            from examples.depth_camera_example import capture_image
            capture_image()
        elif cmd == "record":
            duration = input("请输入录制时长（秒，默认10）: ").strip()
            duration = int(duration) if duration else 10
            from examples.depth_camera_example import record_video
            record_video(duration)
        elif cmd == "live":
            from examples.depth_camera_example import show_live_stream
            show_live_stream()
        else:
            print("无效命令")


def run_audio():
    """运行音频示例"""
    print("\n麦克风扬声器示例")
    print("-" * 60)
    print("可用命令:")
    print("  list     - 列出所有音频设备")
    print("  record   - 录制音频（需要指定文件名和时长）")
    print("  play     - 播放音频文件（需要指定文件名）")
    print("  test     - 录制并播放测试（需要指定时长）")
    print("\n示例:")
    print("  python examples/audio_example.py list")
    print("  python examples/audio_example.py record recording.wav 5")
    print("  python examples/audio_example.py play recording.wav")
    print("  python examples/audio_example.py test 5")
    
    choice = input("\n是否直接运行示例? (y/n): ").strip().lower()
    if choice == 'y':
        cmd = input("请输入命令 (list/record/play/test): ").strip()
        if cmd == "list":
            from examples.audio_example import list_audio_devices
            list_audio_devices()
        elif cmd == "record":
            filename = input("请输入文件名（默认: recording.wav）: ").strip() or "recording.wav"
            duration = input("请输入录制时长（秒，默认5）: ").strip()
            duration = int(duration) if duration else 5
            from examples.audio_example import record_audio
            record_audio(filename, duration)
        elif cmd == "play":
            filename = input("请输入要播放的文件名: ").strip()
            if filename:
                from examples.audio_example import play_audio
                play_audio(filename)
            else:
                print("请指定文件名")
        elif cmd == "test":
            duration = input("请输入测试时长（秒，默认5）: ").strip()
            duration = int(duration) if duration else 5
            from examples.audio_example import record_and_play
            record_and_play(duration)
        else:
            print("无效命令")


def run_thermal_camera():
    """运行红外热成像示例"""
    print("\n红外热成像示例")
    print("-" * 60)
    print("可用命令:")
    print("  capture  - 捕获一帧图像（需要 RTSP 地址）")
    print("  record   - 录制视频（需要 RTSP 地址和时长）")
    print("  live     - 实时显示（需要 RTSP 地址）")
    print("\n默认 RTSP 地址: rtsp://admin:yoseen2018@10.21.31.201:554/h264")
    print("\n示例:")
    print("  python examples/thermal_camera_example.py capture <rtsp_url> thermal_image.jpg")
    print("  python examples/thermal_camera_example.py record <rtsp_url> thermal_video.mp4 10")
    print("  python examples/thermal_camera_example.py live <rtsp_url>")
    
    choice = input("\n是否直接运行示例? (y/n): ").strip().lower()
    if choice == 'y':
        rtsp_url = input("请输入 RTSP 地址（默认: rtsp://admin:yoseen2018@10.21.31.201:554/h264）: ").strip()
        if not rtsp_url:
            rtsp_url = "rtsp://admin:yoseen2018@10.21.31.201:554/h264"
        
        cmd = input("请输入命令 (capture/record/live): ").strip()
        if cmd == "capture":
            output_file = input("请输入输出文件名（默认: thermal_image.jpg）: ").strip() or "thermal_image.jpg"
            from examples.thermal_camera_example import capture_frame
            capture_frame(rtsp_url, output_file)
        elif cmd == "record":
            output_file = input("请输入输出文件名（默认: thermal_video.mp4）: ").strip() or "thermal_video.mp4"
            duration = input("请输入录制时长（秒，默认10）: ").strip()
            duration = int(duration) if duration else 10
            from examples.thermal_camera_example import record_video
            record_video(rtsp_url, output_file, duration)
        elif cmd == "live":
            from examples.thermal_camera_example import show_live_stream
            show_live_stream(rtsp_url)
        else:
            print("无效命令")


def run_temperature_humidity():
    """运行温湿度模块示例"""
    print("\n温湿度模块示例")
    print("-" * 60)
    print("使用云平台 API 获取实时温湿度数据")
    print("\n示例:")
    print("  python examples/temperature_humidity_api.py")
    
    choice = input("\n是否直接运行示例? (y/n): ").strip().lower()
    if choice == 'y':
        from examples.temperature_humidity_api import TemperatureHumidityAPI
        
        api = TemperatureHumidityAPI()
        
        try:
            # 获取用户名和密码
            username = input("请输入用户名（默认: h251225krt）: ").strip() or "h251225krt"
            password = input("请输入密码（默认: h251225krt）: ").strip() or "h251225krt"
            
            # 1. 获取 Token
            print("\n正在获取 Token...")
            token_data = api.get_token(username, password)
            print(f"Token 获取成功，过期时间: {token_data['expiration']}")
            
            # 2. 获取设备分组列表
            print("\n正在获取设备分组列表...")
            groups = api.get_group_list()
            print(f"找到 {len(groups)} 个分组:")
            for group in groups:
                print(f"  - {group['groupName']} (ID: {group['groupId']})")
            
            # 3. 查询实时数据
            print("\n正在查询实时数据...")
            group_id = input("请输入分组ID（可选，直接回车查询所有）: ").strip() or None
            real_time_data = api.get_real_time_data(group_id=group_id)
            print(f"找到 {len(real_time_data)} 个设备的数据:")
            for device in real_time_data:
                print(f"\n设备: {device['deviceName']} (地址: {device['deviceAddr']})")
                print(f"状态: {device['deviceStatus']}")
                if device.get('dataItem'):
                    for node in device['dataItem']:
                        for register in node.get('registerItem', []):
                            print(f"  {register['registerName']}: {register['data']} {register['unit']}")
        
        except Exception as e:
            print(f"错误: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='山猫 M20 pro 组件测试主程序')
    parser.add_argument(
        '--component',
        type=str,
        choices=['depth', 'audio', 'thermal', 'temp', 'all'],
        help='直接运行指定组件测试（depth/audio/thermal/temp/all）'
    )
    
    args = parser.parse_args()
    
    # 如果指定了组件，直接运行
    if args.component:
        if args.component == 'depth':
            run_depth_camera()
        elif args.component == 'audio':
            run_audio()
        elif args.component == 'thermal':
            run_thermal_camera()
        elif args.component == 'temp':
            run_temperature_humidity()
        elif args.component == 'all':
            print("运行所有组件测试...")
            run_depth_camera()
            run_audio()
            run_thermal_camera()
            run_temperature_humidity()
        return
    
    # 交互式菜单
    while True:
        show_menu()
        choice = input("\n请选择功能 (0-4): ").strip()
        
        if choice == '0':
            print("\n退出程序")
            break
        elif choice == '1':
            run_depth_camera()
        elif choice == '2':
            run_audio()
        elif choice == '3':
            run_thermal_camera()
        elif choice == '4':
            run_temperature_humidity()
        else:
            print("\n无效选择，请重新输入")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

