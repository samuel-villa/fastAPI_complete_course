from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 'postgresql://<username>:<password>@localhost/<DB_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/TodoApplicationDB'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
