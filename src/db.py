from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Base

SQLALCHEMY_DATABASE_URL = "postgresql://nima:19911991@localhost:5432/data_viz_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
sess = Session()
