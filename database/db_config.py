from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import (
    DeclarativeBase, 
    Session, 
    sessionmaker
)


DATABASE_URL: str = 'postgresql://localhost/fastapi_db?user=fastapi_app&password=fastapi_app'
engine: Engine = create_engine(DATABASE_URL)
LocalSession: sessionmaker[Session] = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def setup_db():
    Base.metadata.create_all(engine)

def get_db():
    db = LocalSession()

    try:
        yield db
    finally:
        db.close()
