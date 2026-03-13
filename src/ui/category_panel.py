"""
分类面板组件
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from sqlalchemy.orm import Session


class CategoryPanel(QWidget):
    """分类面板组件"""
    
    category_selected = pyqtSignal(int)  # category_id
    
    def __init__(self, session: Session, task_service):
        super().__init__()
        
        self.session = session
        self.task_service = task_service
        
        self._init_ui()
        self._load_categories()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 10, 0)
        
        # 标题
        title_label = QLabel("Categories")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 分类列表
        self.category_list = QListWidget()
        self.category_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)
        self.category_list.itemClicked.connect(self._on_category_clicked)
        layout.addWidget(self.category_list)
        
        # 添加分类按钮
        self.add_btn = QPushButton("+ Add Category")
        self.add_btn.clicked.connect(self._add_category)
        layout.addWidget(self.add_btn)
    
    def _load_categories(self):
        """加载分类列表"""
        from src.models.category import Category
        
        self.category_list.clear()
        
        # 添加"全部"选项
        all_item = QListWidgetItem("📋 All Tasks")
        all_item.setData(Qt.ItemDataRole.UserRole, None)
        all_item.setFont(QFont("Arial", 11))
        self.category_list.addItem(all_item)
        
        # 加载用户分类
        categories = self.session.query(Category).order_by(Category.sort_order).all()
        for cat in categories:
            item = QListWidgetItem(f"{cat.icon} {cat.name}")
            item.setData(Qt.ItemDataRole.UserRole, cat.id)
            item.setFont(QFont("Arial", 11))
            self.category_list.addItem(item)
    
    def _on_category_clicked(self, item):
        """分类点击事件"""
        category_id = item.data(Qt.ItemDataRole.UserRole)
        self.category_selected.emit(category_id if category_id else 0)
    
    def _add_category(self):
        """添加新分类"""
        # TODO: 实现添加分类对话框
        pass
