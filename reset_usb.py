import usb.core
import usb.util
import time

# 查找 candleLight 设备
dev = usb.core.find(idVendor=0x1d50, idProduct=0x606f)

if dev:
    print(f"找到设备: {dev.product}")
    try:
        # 尝试卸载可能存在的内核驱动（虽然现在可能没有）
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)
            print("内核驱动已卸载")
            
        # 核心操作：复位 USB 端口
        print("正在复位 USB 设备...")
        dev.reset()
        print("复位完成！设备已释放。")
    except Exception as e:
        print(f"复位时发生错误: {e}")
else:
    print("未找到设备，请确认是否已插入。")
