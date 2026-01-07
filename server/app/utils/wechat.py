"""
微信小程序工具类
"""
import httpx
from app.core.config import settings


class WeChatMiniProgram:
    """微信小程序工具类"""
    
    def __init__(self):
        self.appid = settings.WECHAT_APPID
        self.secret = settings.WECHAT_SECRET
    
    async def code2session(self, code: str) -> dict:
        """
        通过 code 换取 openid 和 session_key
        
        Args:
            code: wx.login 返回的 code
            
        Returns:
            dict: {
                "openid": "xxx",
                "session_key": "xxx",
                "unionid": "xxx"  # 可选
            }
        """
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": self.appid,
            "secret": self.secret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if "errcode" in data and data["errcode"] != 0:
                raise Exception(f"微信接口错误: {data.get('errmsg', '未知错误')}")
            
            return data
    
    async def get_phone_number(self, code: str) -> dict:
        """
        通过 code 获取手机号
        
        Args:
            code: getPhoneNumber 返回的 code
            
        Returns:
            dict: {
                "phone_number": "13800138000",
                "pure_phone_number": "13800138000",
                "country_code": "86"
            }
        """
        # 获取 access_token
        access_token = await self._get_access_token()
        
        url = f"https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}"
        data = {"code": code}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            result = response.json()
            
            if result.get("errcode") != 0:
                raise Exception(f"获取手机号失败: {result.get('errmsg', '未知错误')}")
            
            return result.get("phone_info", {})
    
    async def _get_access_token(self) -> str:
        """
        获取 access_token
        
        Returns:
            str: access_token
        """
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if "errcode" in data and data["errcode"] != 0:
                raise Exception(f"获取 access_token 失败: {data.get('errmsg', '未知错误')}")
            
            return data.get("access_token", "")


# 创建全局实例
wechat_mp = WeChatMiniProgram()
