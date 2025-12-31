"""
温湿度云平台 API 客户端示例
基于 Postman 集合中的接口实现
"""
import requests
from typing import Optional, Dict, Any


class TemperatureHumidityAPI:
    """温湿度云平台 API 客户端"""
    
    def __init__(self, base_url: str = "https://www.0531yun.com/"):
        """
        初始化 API 客户端
        
        Args:
            base_url: API 基础地址，默认为 https://www.0531yun.com/
        """
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None
    
    def get_token(self, login_name: str, password: str) -> Dict[str, Any]:
        """
        根据用户名和密码获取 Token
        
        Args:
            login_name: 用户名
            password: 密码
            
        Returns:
            包含 token 和 expiration 的字典
        """
        url = f"{self.base_url}/api/getToken/"
        params = {
            "loginName": login_name,
            "password": password
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果状态码不是 200，抛出异常
        
        data = response.json()
        if data.get("code") == 1000:
            self.token = data["data"]["token"]
            return data["data"]
        else:
            raise Exception(f"获取 Token 失败: {data.get('message')}")
    
    def get_group_list(self) -> list:
        """
        获取设备分组列表
        
        Returns:
            分组列表
        """
        if not self.token:
            raise Exception("请先调用 get_token() 获取 Token")
        
        url = f"{self.base_url}/api/device/getGroupList"
        headers = {
            "Authorization": self.token
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") == 1000:
            return data["data"]
        else:
            raise Exception(f"获取分组列表失败: {data.get('message')}")
    
    def get_real_time_data(self, group_id: Optional[str] = None) -> list:
        """
        查询实时数据
        
        Args:
            group_id: 分组ID，可选
            
        Returns:
            实时数据列表
        """
        if not self.token:
            raise Exception("请先调用 get_token() 获取 Token")
        
        url = f"{self.base_url}/api/data/getRealTimeData"
        headers = {
            "Authorization": self.token
        }
        params = {}
        if group_id:
            params["groupId"] = group_id
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") == 1000:
            return data["data"]
        else:
            raise Exception(f"获取实时数据失败: {data.get('message')}")


if __name__ == "__main__":
    # 使用示例
    api = TemperatureHumidityAPI()
    
    try:
        # 1. 获取 Token
        print("正在获取 Token...")
        token_data = api.get_token("h251225krt", "h251225krt")
        print(f"Token 获取成功，过期时间: {token_data['expiration']}")
        
        # 2. 获取设备分组列表
        print("\n正在获取设备分组列表...")
        groups = api.get_group_list()
        print(f"找到 {len(groups)} 个分组:")
        for group in groups:
            print(f"  - {group['groupName']} (ID: {group['groupId']})")
        
        # 3. 查询实时数据
        print("\n正在查询实时数据...")
        real_time_data = api.get_real_time_data()
        print(f"找到 {len(real_time_data)} 个设备的数据:")
        for device in real_time_data:
            print(f"\n设备: {device['deviceName']} (地址: {device['deviceAddr']})")
            print(f"状态: {device['deviceStatus']}")
            if device.get('dataItem'):
                for node in device['dataItem']:
                    for register in node.get('registerItem', []):
                        print(f"  {register['registerName']}: {register['data']} {register['unit']}")
        
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"错误: {e}")

