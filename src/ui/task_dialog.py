"""
任务对话框组件 - 创建/编辑任务
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QDateEdit,
    QPushButton, QLabel, QGroupBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

from src.models.task import Task
from src.database.db_manager import get_session
from src.services.task_service import TaskService


class TaskDialog(QDialog):
    """任务创建/编辑对话框"""
    
    def __init__(self, session, default_date=None, task: Task = None):
        super().__init__()
        
        self.session = session
        self.task = task
        self.default_date = default_date or QDate.currentDate().toPyDate()
        self.task_service = TaskService(session)
        
        self.setWindowTitle("Edit Task" if task else "New Task")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self._init_ui()
        self._load_data()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("Task Details")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 表单区域
        form_group = QGroupBox()
        form_layout = QFormLayout(form_group)
        
        # 标题输入
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title...")
        self.title_input.setMaxLength(200)
        form_layout.addRow("Title:", self.title_input)
        
        # 描述输入
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Enter task description (optional)...")
        self.desc_input.setMaximumHeight(80)
        form_layout.addRow("Description:", self.desc_input)
        
        # 日期选择
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.fromString(
            self.default_date.strftime("%Y-%m-%d"), "yyyy-MM-dd"
        ))
        form_layout.addRow("Due Date:", self.date_input)
        
        # 优先级选择
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        form_layout.addRow("Priority:", self.priority_input)
        
        # 分类选择
        self.category_input = QComboBox()
        self.category_input.addItem("No Category", None)
        self._load_categories()
        form_layout.addRow("Category:", self.category_input)
        
        layout.addWidget(form_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.save_btn.clicked.connect(self._save_task)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
    
    def _load_categories(self):
        """加载分类列表"""
        categories = self.session.query(__import__('src.models.category', fromlist=['Category']).Category).all()
        for cat in categories:
            self.category_input.addItem(f"{cat.icon} {cat.name}", cat.id)
    
    def _load_data(self):
        """加载任务数据 (编辑模式)"""
        if self.task:
            self.title_input.setText(self.task.title)
            self.desc_input.setText(self.task.description or "")
            self.date_input.setDate(QDate.fromString(
                self.task.due_date.strftime("%Y-%m-%d"), "yyyy-MM-dd"
            ))
            self.priority_input.setCurrentIndex(self.task.priority - 1)
            
            # 选择分类
            if self.task.category_id:
                for i in range(self.category_input.count()):
                    if self.category_input.itemData(i) == self.task.category_id:
                        self.category_input.setCurrentIndex(i)
                        break
    
    def _save_task(self):
        """保存任务"""
        title = self.title_input.text().strip()
        if not title:
            self.title_input.setStyleSheet("border: 1px solid red;")
            return
        
        description = self.desc_input.toPlainText().strip()
        due_date = self.date_input.date().toPyDate()
        priority = self.priority_input.currentIndex() + 1
        category_id = self.category_input.currentData()
        
        if self.task:
            # 编辑模式
            self.task_service.update_task(
                self.task.id,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                category_id=category_id
            )
        else:
            # 新建模式
            self.task_service.create_task(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                category_id=category_id
            )
        
        self.accept()
