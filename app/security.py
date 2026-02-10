from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # bcrypt soporta máximo 72 bytes
    password = password.strip().encode("utf-8")[:72]
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    password = password.strip().encode("utf-8")[:72]
    return pwd_context.verify(password, hashed)
