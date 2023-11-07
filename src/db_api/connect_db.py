from config import PASSWORD_MANAGER_CREATED_DATABASE, \
                   NAME_MANAGER_CREATED_DATABASE, \
                   NAME_CREATED_DATABASE, \
                   HOST_SERVER, \
                   PORT_SERVER
from sqlalchemy.orm import declarative_base, \
                           sessionmaker
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = \
    f"postgresql://" \
    f"{NAME_MANAGER_CREATED_DATABASE}:" \
    f"{PASSWORD_MANAGER_CREATED_DATABASE}@" \
    f"{HOST_SERVER}:{PORT_SERVER}/{NAME_CREATED_DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()
