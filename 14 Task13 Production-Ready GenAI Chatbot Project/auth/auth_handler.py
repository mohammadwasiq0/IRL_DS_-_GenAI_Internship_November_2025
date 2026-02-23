from passlib.context import CryptContext
from database.db import SessionLocal
from database.models import User

# ONLY argon2
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def register_user(username, password):
    db = SessionLocal()

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        db.close()
        raise ValueError("User already exists")

    hashed = hash_password(password)

    user = User(username=username, password=hashed)
    db.add(user)
    db.commit()
    db.close()


def authenticate_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if user and verify_password(password, user.password):
        return user

    return None
