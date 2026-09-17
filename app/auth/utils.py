from bcrypt import checkpw, gensalt, hashpw


def get_password_hash(password: str) -> str:
    if is_password_valid(password):
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
    raise ValueError(
        f"Password size is invalid: {len(password.encode('utf-8'))} bytes. Must be between 8 and 72 bytes."
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if is_password_valid(plain_password):
        return checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    return False


def is_password_valid(password: str) -> bool:
    byte_length = len(password.encode("utf-8"))
    return 8 <= byte_length <= 72