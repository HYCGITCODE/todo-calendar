"""
分类数据模型
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Category(Base):
    """分类模型"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True, comment='分类名称')
    color = Column(String(7), default='#CCCCCC', comment='分类颜色 (十六进制)')
    icon = Column(String(20), comment='分类图标 (emoji)')
    sort_order = Column(Integer, default=0, comment='排序顺序')
    
    tasks = relationship("Task", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
    
    @classmethod
    def get_defaults(cls):
        """返回默认分类列表"""
        return [
            {'name': '工作', 'color': '#3498db', 'icon': '💼'},
            {'name': '个人', 'color': '#2ecc71', 'icon': '🏠'},
            {'name': '购物', 'color': '#e74c3c', 'icon': '🛒'},
            {'name': '学习', 'color': '#f39c12', 'icon': '📚'},
        ]
