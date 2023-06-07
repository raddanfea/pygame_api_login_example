import random
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext
from sqlalchemy.ext.declarative import declarative_base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Base = declarative_base()


class DbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    session_token = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def set_password(self, password):
        self.hashed_password = hash_password(password)

    def check_password(self, password):
        return verify_password(password, self.hashed_password)

    def generate_random_token(self):
        self.session_token = pwd_context.hash(random.randbytes(16))
        return self.session_token


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
