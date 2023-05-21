import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf8'), hashed_password)
