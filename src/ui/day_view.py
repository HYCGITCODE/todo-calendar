"""
日视图组件 - 按日详细展示任务
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton,
    QScrollArea, QFrame, QTimeEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt6.QtGui import QFont, QColor


class DayView(QWidget):
    """日视图组件"""
    
    date_selected = pyqtSignal(QDate)
    task_requested = pyqtSignal(int)  # 请求编辑任务
    
    def __init__(self, task_service):
        super().__init__()
        
        self.task_service = task_service
        self.current_date = QDate.currentDate()
        
        self._init_ui()
        self._render_day()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 日导航栏
        nav_layout = QHBoxLayout()
        
        self.prev_day_btn = QPushButton("◄")
        self.prev_day_btn.setFixedSize(40, 30)
        self.prev_day_btn.clicked.connect(self._prev_day)
        nav_layout.addWidget(self.prev_day_btn)
        
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(self.date_label, stretch=1)
        
        self.next_day_btn = QPushButton("►")
        self.next_day_btn.setFixedSize(40, 30)
        self.next_day_btn.clicked.connect(self._next_day)
        nav_layout.addWidget(self.next_day_btn)
        
        self.today_btn = QPushButton("Today")
        self.today_btn.setFixedHeight(30)
        self.today_btn.clicked.connect(self._go_to_today)
        nav_layout.addWidget(self.today_btn)
        
        layout.addLayout(nav_layout)
        
        # 日期信息
        info_layout = QHBoxLayout()
        
        # 星期
        self.weekday_label = QLabel()
        self.weekday_label.setFont(QFont("Arial", 12))
        info_layout.addWidget(self.weekday_label)
        
        info_layout.addStretch()
        
        # 任务统计
        self.task_count_label = QLabel()
        self.task_count_label.setFont(QFont("Arial", 11))
        self.task_count_label.setStyleSheet("color: #666;")
        info_layout.addWidget(self.task_count_label)
        
        layout.addLayout(info_layout)
        
        # 时间轴容器
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.time_axis_widget = QWidget()
        self.time_axis_layout = QVBoxLayout(self.time_axis_widget)
        self.time_axis_layout.setContentsMargins(0, 0, 0, 0)
        self.time_axis_layout.setSpacing(5)
        
        scroll_area.setWidget(self.time_axis_widget)
        layout.addWidget(scroll_area, stretch=1)
    
    def _render_day(self):
        """渲染日视图"""
        # 更新日期标签
        self.date_label.setText(self.current_date.toString("MMMM d, yyyy"))
        
        # 更新星期
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                        "Friday", "Saturday", "Sunday"]
        weekday = weekday_names[self.current_date.dayOfWeek() - 1]
        self.weekday_label.setText(weekday)
        
        # 标记今天
        if self.current_date == QDate.currentDate():
            self.date_label.setStyleSheet("color: #3498db;")
            self.weekday_label.setStyleSheet("color: #3498db; font-weight: bold;")
        else:
            self.date_label.setStyleSheet("")
            self.weekday_label.setStyleSheet("")
        
        # 获取当天任务
        tasks = self.task_service.get_tasks_by_date(self.current_date.toPyDate())
        self.task_count_label.setText(f"{len(tasks)} tasks")
        
        # 清空时间轴
        for i in reversed(range(self.time_axis_layout.count())):
            widget = self.time_axis_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # 创建时间槽 (每小时)
        for hour in range(24):
            time_slot = self._create_time_slot(hour, tasks)
            self.time_axis_layout.addWidget(time_slot)
    
    def _create_time_slot(self, hour: int, tasks: list) -> QFrame:
        """
        创建时间槽
        
        Args:
            hour: 小时 (0-23)
            tasks: 任务列表
            
        Returns:
            时间槽组件
        """
        slot = QFrame()
        slot.setFrameStyle(QFrame.Shape.StyledPanel)
        slot.setMinimumHeight(60)
        
        layout = QHBoxLayout(slot)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # 时间标签
        time_label = QLabel(f"{hour:02d}:00")
        time_label.setFont(QFont("Arial", 10))
        time_label.setFixedWidth(60)
        time_label.setStyleSheet("color: #999;")
        layout.addWidget(time_label)
        
        # 任务区域
        tasks_frame = QFrame()
        tasks_layout = QVBoxLayout(tasks_frame)
        tasks_layout.setContentsMargins(5, 5, 5, 5)
        tasks_layout.setSpacing(5)
        
        # 筛选这个小时的任务 (简化：假设任务没有具体时间)
        # TODO: 当任务模型支持时间后，这里可以按时间过滤
        
        # 显示所有任务 (简化版)
        if hour == 9:  # 示例：在 9 点显示所有任务
            for task in tasks:
                task_widget = self._create_task_widget(task)
                tasks_layout.addWidget(task_widget)
        
        # 时间线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #eee;")
        line.setFixedHeight(1)
        layout.addWidget(line, stretch=1)
        
        layout.addWidget(tasks_frame, stretch=1)
        
        return slot
    
    def _create_task_widget(self, task) -> QFrame:
        """
        创建任务小部件
        
        Args:
            task: 任务对象
            
        Returns:
            任务组件
        """
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # 任务标题
        title_label = QLabel(task.title)
        title_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        if task.status == 2:  # 已完成
            title_label.setStyleSheet("color: #999; text-decoration: line-through;")
        elif task.priority == 3:  # 高优先级
            title_label.setStyleSheet("color: #e74c3c;")
        elif task.priority == 2:  # 中优先级
            title_label.setStyleSheet("color: #f39c12;")
        
        layout.addWidget(title_label)
        
        # 任务描述
        if task.description:
            desc_label = QLabel(task.description[:80] + "..." if len(task.description) > 80 else task.description)
            desc_label.setFont(QFont("Arial", 9))
            desc_label.setStyleSheet("color: #666;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # 分类和优先级
        meta_layout = QHBoxLayout()
        
        priority_text = {1: "🔵 Low", 2: "🟡 Medium", 3: "🔴 High"}
        priority_label = QLabel(priority_text.get(task.priority, "🔵 Low"))
        priority_label.setFont(QFont("Arial", 9))
        meta_layout.addWidget(priority_label)
        
        if task.category:
            category_label = QLabel(f"{task.category.icon} {task.category.name}")
            category_label.setFont(QFont("Arial", 9))
            meta_layout.addWidget(category_label)
        
        meta_layout.addStretch()
        layout.addLayout(meta_layout)
        
        # 根据状态设置样式
        if task.status == 2:
            widget.setStyleSheet("""
                QFrame {
                    background-color: #f5f5f5;
                    border-left: 3px solid #999;
                    border-radius: 4px;
                }
            """)
        elif task.priority == 3:
            widget.setStyleSheet("""
                QFrame {
                    background-color: #ffebee;
                    border-left: 3px solid #e74c3c;
                    border-radius: 4px;
                }
            """)
        else:
            widget.setStyleSheet("""
                QFrame {
                    background-color: #e3f2fd;
                    border-left: 3px solid #3498db;
                    border-radius: 4px;
                }
            """)
        
        return widget
    
    def _prev_day(self):
        """切换到前一天"""
        self.current_date = self.current_date.addDays(-1)
        self._render_day()
    
    def _next_day(self):
        """切换到后一天"""
        self.current_date = self.current_date.addDays(1)
        self._render_day()
    
    def _go_to_today(self):
        """跳转到今天"""
        self.current_date = QDate.currentDate()
        self._render_day()
    
    def navigate_to_date(self, qdate: QDate):
        """
        导航到指定日期
        
        Args:
            qdate: 目标日期
        """
        self.current_date = qdate
        self._render_day()
