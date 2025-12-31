"""
机械臂基础示例
使用 piper-sdk 控制机械臂
基于 Piper SDK 文档编写

注意：
1. 使用前需要先激活 CAN 设备（如 can0）
2. 机械臂需要处在从臂模式下才能读取反馈
3. 请根据实际设备配置修改 can_name 等参数
"""
from piper_sdk import (
    C_PiperInterface,
    C_PiperInterface_V2,
    ArmMsgFeedbackStatus,
    ArmMsgFeedbackJointStates,
    ArmMsgJointCtrl,
    LogLevel
)
import time


def basic_control_example(can_name='can0'):
    """
    基础控制示例
    
    Args:
        can_name: CAN 设备名称，默认为 'can0'
    """
    # 初始化 V2 接口（推荐使用）
    # 参数说明：
    # - can_name: CAN 设备名称
    # - judge_flag: 判断标志，默认 True
    # - can_auto_init: 自动初始化 CAN，默认 True
    # - logger_level: 日志级别，默认 WARNING
    print(f"正在初始化机械臂接口 (CAN: {can_name})...")
    piper = C_PiperInterface_V2(
        can_name=can_name,
        judge_flag=True,
        can_auto_init=True,
        logger_level=LogLevel.WARNING
    )
    
    try:
        # 连接端口，开启 can 收发线程
        # ConnectPort() 返回 0 表示成功
        print("正在连接机械臂...")
        result = piper.ConnectPort()
        if result != 0:
            print(f"错误: 无法连接到机械臂，返回码: {result}")
            print("请检查:")
            print("  1. CAN 设备是否已激活")
            print("  2. 机械臂是否已上电")
            print("  3. CAN 连接是否正常")
            return
        
        print("连接成功")
        
        # 等待连接稳定
        time.sleep(0.5)
        
        # 获取机械臂状态（需要机械臂处在从臂模式下）
        print("\n获取机械臂状态...")
        status = piper.GetArmStatus()
        if status:
            # status 是 ArmMsgFeedbackStatus 对象
            print(f"机械臂状态类型: {type(status).__name__}")
            # 打印状态信息
            if hasattr(status, '__dict__'):
                for key, value in status.__dict__.items():
                    if not key.startswith('_'):
                        print(f"  {key}: {value}")
        
        # 获取关节消息
        print("\n获取关节消息...")
        joint_msgs = piper.GetArmJointMsgs()
        if joint_msgs:
            print(f"关节消息数量: {len(joint_msgs)}")
            for i, msg in enumerate(joint_msgs):
                print(f"\n关节 {i+1}:")
                # msg 是 ArmMsgFeedbackJointStates 对象
                if hasattr(msg, '__dict__'):
                    for key, value in msg.__dict__.items():
                        if not key.startswith('_'):
                            print(f"  {key}: {value}")
                else:
                    print(f"  {msg}")
        
        # 提取关节角度信息
        if joint_msgs:
            angles = []
            for msg in joint_msgs:
                # 根据 ArmMsgFeedbackJointStates 的实际结构提取角度
                # 可能的属性名：angle, position, joint_angle 等
                if hasattr(msg, 'angle'):
                    angles.append(msg.angle)
                elif hasattr(msg, 'position'):
                    angles.append(msg.position)
                elif hasattr(msg, 'joint_angle'):
                    angles.append(msg.joint_angle)
            if angles:
                print(f"\n当前关节角度: {angles}")
        
        # 注意：控制机械臂移动需要使用 ArmMsgJointCtrl 等消息类型
        # 具体使用方法请参考 SDK 文档和示例
        
    except ConnectionError as e:
        print(f"连接错误: {e}")
        print("提示: 请确保 CAN 设备已正确配置和激活")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 断开连接
        try:
            piper.DisconnectPort()
            print("\n已断开连接")
        except:
            pass


def get_status_example(can_name='can0'):
    """
    获取机械臂状态示例
    
    Args:
        can_name: CAN 设备名称，默认为 'can0'
    """
    print(f"正在初始化机械臂接口 (CAN: {can_name})...")
    piper = C_PiperInterface_V2(can_name=can_name, logger_level=LogLevel.WARNING)
    
    try:
        # 连接端口
        print("正在连接机械臂...")
        result = piper.ConnectPort()
        if result != 0:
            print(f"错误: 无法连接到机械臂，返回码: {result}")
            return
        
        print("连接成功")
        time.sleep(0.5)
        
        # 获取机械臂状态
        print("\n获取机械臂状态...")
        status = piper.GetArmStatus()
        if status:
            print(f"状态对象类型: {type(status).__name__}")
            if hasattr(status, '__dict__'):
                for key, value in status.__dict__.items():
                    if not key.startswith('_'):
                        print(f"  {key}: {value}")
        
        # 获取关节消息
        print("\n获取关节消息...")
        joint_msgs = piper.GetArmJointMsgs()
        if joint_msgs:
            print(f"关节数量: {len(joint_msgs)}")
            for i, msg in enumerate(joint_msgs):
                print(f"\n关节 {i+1} ({type(msg).__name__}):")
                if hasattr(msg, '__dict__'):
                    for key, value in msg.__dict__.items():
                        if not key.startswith('_'):
                            print(f"  {key}: {value}")
        
        # 持续获取状态（可选）
        print("\n持续获取状态（10次，按 Ctrl+C 可提前停止）...")
        try:
            for i in range(10):
                status = piper.GetArmStatus()
                joint_msgs = piper.GetArmJointMsgs()
                print(f"\n第 {i+1} 次读取:")
                if joint_msgs:
                    angles = []
                    for msg in joint_msgs:
                        if hasattr(msg, 'angle'):
                            angles.append(msg.angle)
                        elif hasattr(msg, 'position'):
                            angles.append(msg.position)
                        elif hasattr(msg, 'joint_angle'):
                            angles.append(msg.joint_angle)
                    if angles:
                        print(f"  关节角度: {angles}")
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n停止读取")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            piper.DisconnectPort()
            print("\n已断开连接")
        except:
            pass


def use_v1_interface_example(can_name='can0'):
    """
    使用 V1 接口示例
    
    Args:
        can_name: CAN 设备名称，默认为 'can0'
    """
    print(f"使用 V1 接口初始化机械臂 (CAN: {can_name})...")
    piper = C_PiperInterface(can_name=can_name)
    
    try:
        print("正在连接机械臂...")
        result = piper.ConnectPort()
        if result != 0:
            print(f"错误: 无法连接到机械臂，返回码: {result}")
            return
        
        print("连接成功")
        time.sleep(0.5)
        
        # V1 接口的使用方式与 V2 类似
        status = piper.GetArmStatus()
        joint_msgs = piper.GetArmJointMsgs()
        
        if status:
            print(f"机械臂状态: {type(status).__name__}")
            if hasattr(status, '__dict__'):
                for key, value in status.__dict__.items():
                    if not key.startswith('_'):
                        print(f"  {key}: {value}")
        
        if joint_msgs:
            print(f"\n关节消息数量: {len(joint_msgs)}")
            for i, msg in enumerate(joint_msgs):
                print(f"关节 {i+1}: {type(msg).__name__}")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            piper.DisconnectPort()
            print("\n已断开连接")
        except:
            pass


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python arm_example.py basic [can_name]  # 基础控制示例（使用 V2 接口）")
        print("  python arm_example.py status [can_name]  # 获取状态示例")
        print("  python arm_example.py v1 [can_name]     # 使用 V1 接口示例")
        print("\n参数说明:")
        print("  can_name: CAN 设备名称，默认为 'can0'")
        print("\n注意事项:")
        print("  1. 使用前需要先激活 CAN 设备（如: sudo ip link set can0 up type can bitrate 1000000）")
        print("  2. 机械臂需要处在从臂模式下才能读取反馈")
        print("  3. 请根据实际设备配置修改 can_name 等参数")
        print("  4. 详细使用请参考: https://github.com/agilexrobotics/piper_sdk/blob/master/README(ZH).MD")
        sys.exit(1)
    
    command = sys.argv[1]
    can_name = sys.argv[2] if len(sys.argv) > 2 else 'can0'
    
    if command == "basic":
        basic_control_example(can_name)
    elif command == "status":
        get_status_example(can_name)
    elif command == "v1":
        use_v1_interface_example(can_name)
    else:
        print(f"未知命令: {command}")
