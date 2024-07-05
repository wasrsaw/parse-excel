"""
Здесь инициализируем модель БД
"""

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, create_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

Base = declarative_base()

class Rasp(Base):
   __tablename__ = 'Rasp'
   
   id = Column(Integer, primary_key=True, autoincrement=True)
   prep_id = Column(Integer, ForeignKey("Prep.id"))

class Prep(Base):
    __tablename__ = 'Prep'

    id = Column(Integer, primary_key=True)