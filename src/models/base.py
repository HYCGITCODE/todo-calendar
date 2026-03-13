"""
SQLAlchemy Base 基类

所有模型共享同一个 Base，确保外键关系正确
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
