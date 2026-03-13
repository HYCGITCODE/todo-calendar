"""
周视图组件 - 按周展示任务
"""

from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout,
    QScrollArea, QFrame, QVBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QColor


class WeekView(QWidget):
    """周视图组件"""
    
    date_selected = pyqtSignal(QDate)
    week_changed = pyqtSignal(int, int)  # year, week_number
    
    def __init__(self, task_service):
        super().__init__()
        
        self.task_service = task_service
        self.current_date = QDate.currentDate()
        self.selected_date = QDate.currentDate()
        
        self._init_ui()
        self._render_week()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 周导航栏
        nav_layout = QHBoxLayout()
        
        self.prev_week_btn = QPushButton("◄ Week")
        self.prev_week_btn.setFixedHeight(30)
        self.prev_week_btn.clicked.connect(self._prev_week)
        nav_layout.addWidget(self.prev_week_btn)
        
        self.week_label = QLabel()
        self.week_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.week_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(self.week_label, stretch=1)
        
        self.next_week_btn = QPushButton("Week ►")
        self.next_week_btn.setFixedHeight(30)
        self.next_week_btn.clicked.connect(self._next_week)
        nav_layout.addWidget(self.next_week_btn)
        
        self.today_btn = QPushButton("Today")
        self.today_btn.setFixedHeight(30)
        self.today_btn.clicked.connect(self._go_to_today)
        nav_layout.addWidget(self.today_btn)
        
        layout.addLayout(nav_layout)
        
        # 周历网格
        self.week_grid = QGridLayout()
        self.week_grid.setSpacing(5)
        
        # 星期标题
        week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day_name in enumerate(week_days):
            header = QLabel(day_name)
            header.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setStyleSheet("padding: 5px; background-color: #f5f5f5;")
            self.week_grid.addWidget(header, 0, i)
        
        layout.addLayout(self.week_grid)
        layout.addStretch()
    
    def _render_week(self):
        """渲染周视图"""
        # 获取当前周的日期
        week_dates = self._get_week_dates(self.current_date)
        
        # 更新周标签
        week_number = self.current_date.weekNumber()[0]
        year = week_dates[0].year()
        self.week_label.setText(f"{year} - Week {week_number}")
        self.week_changed.emit(year, week_number)
        
        # 清除旧的日期组件
        for i in reversed(range(1, self.week_grid.count())):
            widget = self.week_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # 创建日期卡片
        for i, qdate in enumerate(week_dates):
            day_card = self._create_day_card(qdate, i + 1)
            self.week_grid.addWidget(day_card, 1, i)
    
    def _create_day_card(self, qdate: QDate, col: int) -> QFrame:
        """
        创建单日卡片
        
        Args:
            qdate: 日期
            col: 列索引
            
        Returns:
            日期卡片组件
        """
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel)
        card.setLineWidth(1)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # 日期数字
        date_label = QLabel(str(qdate.day()))
        date_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(date_label)
        
        # 获取当天任务数
        tasks = self.task_service.get_tasks_by_date(qdate.toPyDate())
        task_count = len(tasks)
        
        if task_count > 0:
            task_label = QLabel(f"{task_count} tasks")
            task_label.setFont(QFont("Arial", 9))
            task_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            task_label.setStyleSheet("color: #666;")
            layout.addWidget(task_label)
        
        # 标记今天
        if qdate == QDate.currentDate():
            card.setStyleSheet("""
                QFrame {
                    background-color: #3498db;
                    border-radius: 8px;
                }
                QLabel {
                    color: white;
                }
            """)
        # 标记选中日期
        elif qdate == self.selected_date:
            card.setStyleSheet("""
                QFrame {
                    background-color: #e3f2fd;
                    border: 2px solid #3498db;
                    border-radius: 8px;
                }
            """)
        # 标记周末
        elif qdate.dayOfWeek() >= 6:
            card.setStyleSheet("""
                QFrame {
                    background-color: #ffebee;
                    border-radius: 8px;
                }
                QLabel {
                    color: #e74c3c;
                }
            """)
        else:
            card.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }
            """)
        
        # 点击选择日期
        card.mousePressEvent = lambda event, d=qdate: self._on_date_clicked(d)
        
        return card
    
    def _get_week_dates(self, target_date: QDate) -> list:
        """
        获取指定日期所在周的日期列表
        
        Args:
            target_date: 目标日期
            
        Returns:
            日期列表 [QDate]
        """
        # 找到周一
        days_since_monday = target_date.dayOfWeek() - 1
        monday = target_date.addDays(-days_since_monday)
        
        return [monday.addDays(i) for i in range(7)]
    
    def _on_date_clicked(self, qdate: QDate):
        """日期点击事件"""
        self.selected_date = qdate
        self.date_selected.emit(qdate)
        self._render_week()  # 重新渲染以更新选中状态
    
    def _prev_week(self):
        """切换到上一周"""
        self.current_date = self.current_date.addDays(-7)
        self._render_week()
    
    def _next_week(self):
        """切换到下一周"""
        self.current_date = self.current_date.addDays(7)
        self._render_week()
    
    def _go_to_today(self):
        """跳转到本周"""
        self.current_date = QDate.currentDate()
        self.selected_date = QDate.currentDate()
        self._render_week()
    
    def navigate_to_week(self, year: int, week_number: int):
        """
        导航到指定周
        
        Args:
            year: 年份
            week_number: 周数
        """
        # 计算该周第一天的日期
        from datetime import datetime
        # 找到该年的第一周
        jan_first = QDate(year, 1, 1)
        # 计算到目标周的天数
        days_to_add = (week_number - 1) * 7
        self.current_date = jan_first.addDays(days_to_add)
        self._render_week()
