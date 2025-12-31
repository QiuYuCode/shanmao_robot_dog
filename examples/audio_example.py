"""
麦克风扬声器基础示例
使用 pyaudio 进行音频录制和播放
"""
import pyaudio
import wave
import sys


def list_audio_devices():
    """列出所有可用的音频设备"""
    p = pyaudio.PyAudio()
    print("可用的音频设备:")
    print("-" * 80)
    
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"设备 {i}: {info['name']}")
        print(f"  最大输入通道数: {info['maxInputChannels']}")
        print(f"  最大输出通道数: {info['maxOutputChannels']}")
        print(f"  默认采样率: {info['defaultSampleRate']}")
        print()
    
    p.terminate()


def record_audio(filename="recording.wav", duration=5, sample_rate=16000, channels=1):
    """
    录制音频
    
    Args:
        filename: 保存的文件名
        duration: 录制时长（秒）
        sample_rate: 采样率，默认 16000
        channels: 声道数，1=单声道，2=立体声
    """
    chunk = 1024
    format = pyaudio.paInt16
    
    p = pyaudio.PyAudio()
    
    print(f"开始录制 {duration} 秒...")
    print(f"采样率: {sample_rate} Hz, 声道: {channels}")
    
    stream = p.open(
        format=format,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk
    )
    
    frames = []
    
    try:
        for _ in range(0, int(sample_rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
    except KeyboardInterrupt:
        print("\n录制被中断")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # 保存为 WAV 文件
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"录制完成，已保存到: {filename}")


def play_audio(filename):
    """
    播放音频文件
    
    Args:
        filename: 要播放的音频文件名
    """
    chunk = 1024
    
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )
    
    print(f"正在播放: {filename}")
    print(f"采样率: {wf.getframerate()} Hz, 声道: {wf.getnchannels()}")
    
    try:
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)
    except KeyboardInterrupt:
        print("\n播放被中断")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()
        print("播放完成")


def record_and_play(duration=5):
    """录制并立即播放"""
    filename = "temp_recording.wav"
    record_audio(filename, duration)
    print("\n开始播放录制的音频...")
    play_audio(filename)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python audio_example.py list  # 列出所有音频设备")
        print("  python audio_example.py record [文件名] [时长]  # 录制音频，默认 recording.wav, 5秒")
        print("  python audio_example.py play <文件名>  # 播放音频文件")
        print("  python audio_example.py test [时长]  # 录制并播放，默认5秒")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        list_audio_devices()
    elif command == "record":
        filename = sys.argv[2] if len(sys.argv) > 2 else "recording.wav"
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        record_audio(filename, duration)
    elif command == "play":
        if len(sys.argv) < 3:
            print("错误: 请指定要播放的文件名")
            sys.exit(1)
        play_audio(sys.argv[2])
    elif command == "test":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        record_and_play(duration)
    else:
        print(f"未知命令: {command}")

