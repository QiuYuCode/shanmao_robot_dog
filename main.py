import time
import can
import usb.core
# 导入 piper_sdk 模块
from piper_sdk import *

# ==========================================
# V3 修复版：解决 'bustype' 和 'interface' 冲突
# ==========================================
_original_can_bus = can.Bus

def _custom_can_bus_hook(*args, **kwargs):
    """
    V3 钩子函数：
    精确修改 SDK 传入的参数，避免重复传参报错。
    """
    # SDK 代码里写的是 bustype="socketcan"，所以我们主要检查这个键
    target_key = None
    if kwargs.get('bustype') == 'socketcan':
        target_key = 'bustype'
    elif kwargs.get('interface') == 'socketcan':
        target_key = 'interface'
    
    # 只要检测到 socketcan 请求，就开始拦截
    if target_key:
        print("\n[Hack] 检测到 SDK 正在请求 socketcan 接口...")
        
        # 查找 USB 设备
        dev = usb.core.find(idVendor=0x1d50, idProduct=0x606f)
        
        if dev:
            print(f"[Hack] 成功找到 USB CAN 适配器: {dev.product}")
            print("[Hack] 正在切换驱动模式...")
            
            # --- 关键修改开始 ---
            # 1. 修改目标键的值为 'gs_usb' (绕过内核)
            kwargs[target_key] = 'gs_usb'
            
            # 2. 彻底清理冲突键：如果修改的是 bustype，必须确保 interface 不存在，反之亦然
            if target_key == 'bustype':
                kwargs.pop('interface', None)
            else:
                kwargs.pop('bustype', None)
            # --- 关键修改结束 ---

            # 3. 设置 USB 直连参数
            kwargs['channel'] = dev.product
            kwargs['index'] = 0
            
            # 4. 自动适配波特率
            if not kwargs.get('bitrate'):
                 kwargs['bitrate'] = 1000000
                 print(f"[Hack] SDK 未指定波特率，默认设置为: 1000000")
            else:
                 print(f"[Hack] 使用 SDK 请求的波特率: {kwargs['bitrate']}")
                
            return _original_can_bus(*args, **kwargs)
        else:
            print("[Hack] 错误：未找到 USB CAN 设备！")
            return _original_can_bus(*args, **kwargs)
    
    # 非 socketcan 请求直接放行
    return _original_can_bus(*args, **kwargs)

# 应用补丁
can.Bus = _custom_can_bus_hook
can.interface.Bus = _custom_can_bus_hook
# ==========================================


if __name__ == "__main__":
    print("正在启动适配版 Piper 测试程序 (V3)...")

    try:
        # 实例化接口
        piper = C_PiperInterface(can_name="can0",
                                    judge_flag=False,
                                    can_auto_init=True,
                                    dh_is_offset=1,
                                    start_sdk_joint_limit=False,
                                    start_sdk_gripper_limit=False,
                                    logger_level=LogLevel.WARNING,
                                    log_to_file=False)
        
        piper.ConnectPort()
        print("连接成功！开始读取数据...")
        
        while True:
            msgs = piper.GetArmJointMsgs()
            print(f"关节数据: {msgs}")
            time.sleep(0.005)

    except Exception as e:
        print(f"\n运行时发生错误: {e}")
        import traceback
        traceback.print_exc()
