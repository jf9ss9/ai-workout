import bcrypt


def create_bcrypt_hash(password: str) -> str:
    password_bytes = password.encode()
    salt = bcrypt.gensalt(14)
    password_hash_bytes = bcrypt.hashpw(password_bytes, salt)
    password_hash_str = password_hash_bytes.decode("utf-8")

    return password_hash_str


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode()
    hash_bytes = hashed_password.encode("utf-8")

    does_match = bcrypt.checkpw(password_bytes, hash_bytes)

    return does_match
