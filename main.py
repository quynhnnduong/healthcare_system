from model import Base
from model.db import engine
from AESCipher import *
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()