"""
任务列表组件
"""

from PyQt6.QtWidgets import (
    QListWidget, QListWidgetItem, QCheckBox, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QMenu, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QPoint
from PyQt6.QtGui import QColor, QFont, QPalette, QDrag, QPixmap, QPainter


class TaskListWidget(QListWidget):
    """任务列表组件 - 支持拖拽修改日期"""
    
    task_completed = pyqtSignal(int, bool)  # task_id, completed
    task_edited = pyqtSignal(int)  # task_id
    task_dropped = pyqtSignal(int, object)  # task_id, new_date
    
    def __init__(self, task_service):
        super().__init__()
        
        self.task_service = task_service
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self.itemClicked.connect(self._on_item_clicked)
        
        # 启用拖拽
        self.setDragEnabled(True)
        self.setAcceptDrops(False)  # 列表本身不接受 drop，由日历视图接受
        
        # 设置样式
        self.setStyleSheet("""
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
    
    def load_tasks(self, tasks):
        """加载任务列表"""
        self.clear()
        
        for task in tasks:
            item = QListWidgetItem()
            widget = TaskItemWidget(task)
            
            # 连接复选框信号
            widget.checkbox.toggled.connect(
                lambda checked, t=task: self.task_completed.emit(t.id, checked)
            )
            
            # 设置 item 大小
            item.setSizeHint(widget.sizeHint())
            
            self.addItem(item)
            self.setItemWidget(item, widget)
    
    def _on_item_clicked(self, item):
        """item 点击事件"""
        # 双击编辑
        pass
    
    def _show_context_menu(self, pos):
        """显示右键菜单"""
        item = self.itemAt(pos)
        if item:
            widget = self.itemWidget(item)
            if widget and hasattr(widget, 'task'):
                menu = QMenu(self)
                
                edit_action = menu.addAction("Edit")
                edit_action.triggered.connect(lambda: self.task_edited.emit(widget.task.id))
                
                delete_action = menu.addAction("Delete")
                delete_action.triggered.connect(lambda: self._delete_task(widget.task.id))
                
                menu.exec(self.mapToGlobal(pos))
    
    def _delete_task(self, task_id):
        """删除任务"""
        if self.task_service.delete_task(task_id):
            self.load_tasks(self.task_service.get_tasks_by_date(
                self.task_service.get_task(task_id).due_date if self.task_service.get_task(task_id) 
                else QDate.currentDate().toPyDate()
            ))


class TaskItemWidget(QWidget):
    """单个任务项组件 - 支持优先级颜色编码和拖拽"""
    
    def __init__(self, task):
        super().__init__()
        self.task = task
        self.drag_start_position = QPoint()
        
        # 优先级颜色配置 (P0 红/P1 黄/P2 绿)
        self.priority_colors = {
            3: {'bg': '#FEE2E2', 'border': '#EF4444', 'text': '#EF4444'},  # P0 高
            2: {'bg': '#FEF3C7', 'border': '#F59E0B', 'text': '#F59E0B'},  # P1 中
            1: {'bg': '#D1FAE5', 'border': '#10B981', 'text': '#10B981'},  # P2 低
        }
        
        # 设置背景色和左边框
        colors = self.priority_colors.get(task.priority, self.priority_colors[1])
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors['bg']};
                border-left: 4px solid {colors['border']};
                border-radius: 4px;
                margin: 2px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # 复选框
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(task.status == 2)
        layout.addWidget(self.checkbox)
        
        # 任务信息
        info_layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel(task.title)
        title_label.setFont(QFont("Arial", 11, QFont.Weight.Bold if task.priority == 3 else QFont.Weight.Normal))
        
        if task.status == 2:
            # 已完成：删除线 + 灰色
            title_label.setStyleSheet("color: #999; text-decoration: line-through;")
        else:
            # 未完成：根据优先级显示颜色
            title_label.setStyleSheet(f"color: {colors['text']};")
        
        info_layout.addWidget(title_label)
        
        # 描述 (如果有)
        if task.description:
            desc_label = QLabel(task.description[:50] + "..." if len(task.description) > 50 else task.description)
            desc_label.setStyleSheet("color: #666; font-size: 10px;")
            info_layout.addWidget(desc_label)
        
        # 分类和优先级
        meta_layout = QHBoxLayout()
        
        # 优先级标签
        priority_text = {3: "P0 高", 2: "P1 中", 1: "P2 低"}
        priority_label = QLabel(f"● {priority_text.get(task.priority, 'P2 低')}")
        priority_label.setStyleSheet(f"color: {colors['text']}; font-size: 10px; font-weight: bold;")
        meta_layout.addWidget(priority_label)
        
        # 分类 (如果有)
        if task.category:
            category_label = QLabel(f"{task.category.icon} {task.category.name}")
            category_label.setStyleSheet(f"color: {task.category.color}; font-size: 10px;")
            meta_layout.addWidget(category_label)
        
        meta_layout.addStretch()
        info_layout.addLayout(meta_layout)
        
        layout.addLayout(info_layout, stretch=1)
    
    def mousePressEvent(self, event):
        """鼠标按下事件 - 记录拖拽起始位置"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 启动拖拽"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        
        # 检查移动距离，避免误触
        if (event.pos() - self.drag_start_position).manhattanLength() < 10:
            return
        
        # 创建拖拽对象
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setData('task/id', str(self.task.id).encode())
        mime_data.setData('task/date', self.task.due_date.isoformat().encode())
        drag.setMimeData(mime_data)
        
        # 创建拖拽预览图
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        
        # 执行拖拽
        drop_action = drag.exec(Qt.DropAction.MoveAction)
        
        if drop_action == Qt.DropAction.MoveAction:
            # 拖拽成功，可选：显示成功提示
            pass
