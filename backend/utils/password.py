import secrets
import hashlib
import hmac

def generate_token(length:  int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    
    Args:
        length:  Token length in bytes
        
    Returns: 
        Hex-encoded token string
    """
    return secrets.token_hex(length)


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    salt = secrets.token_hex(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${key.hex()}"


def verify_password(password: str, hashed:  str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: Plain text password to verify
        hashed: Stored hash
        
    Returns: 
        True if password matches, False otherwise
    """
    try:
        salt, key = hashed.split('$')
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return hmac.compare_digest(new_key. hex(), key)
    except Exception: 
        return False