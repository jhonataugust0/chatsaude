from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os 
from ..configs.base import Base

  

class Connection():
  def __init__(self):
    self.url_connection = os.environ.get("CONNECTION_URL")
    self.engine = self.create_database_engine()
    self.session = None
    self.sql_meta = MetaData(self.engine)

  def create_database_engine(self):
    engine = create_engine(f'{self.url_connection}')
    return engine

  def get_engine(self):
    return self.engine

  def __enter__(self):
    session_make = sessionmaker(bind=self.engine)
    self.session = session_make()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.session.close()
