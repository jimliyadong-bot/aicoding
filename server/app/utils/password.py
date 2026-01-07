"""
密码哈希工具
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    哈希密码
    
    Args:
        password: 明文密码
        
    Returns:
        str: 哈希后的密码
    """
    # bcrypt 需要 bytes
    password_bytes = password.encode('utf-8')
    # 生成盐并哈希
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # 返回字符串
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码
        
    Returns:
        bool: 密码是否匹配
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
