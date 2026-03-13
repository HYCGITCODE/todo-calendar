"""
日历视图组件
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QToolTip
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QColor, QDragEnterEvent, QDropEvent


class CalendarView(QWidget):
    """日历视图组件"""
    
    date_selected = pyqtSignal(QDate)
    date_double_clicked = pyqtSignal(QDate)  # 双击创建任务信号
    month_changed = pyqtSignal(int, int)
    
    def __init__(self, year: int, month: int, task_service, on_task_dropped_callback=None):
        super().__init__()
        
        self.year = year
        self.month = month
        self.task_service = task_service
        self.selected_date = QDate.currentDate()
        self.on_task_dropped = on_task_dropped_callback  # 拖拽回调
        
        self._init_ui()
        self._render_calendar()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 月份导航栏
        nav_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("◄")
        self.prev_btn.setFixedSize(40, 30)
        self.prev_btn.clicked.connect(self._prev_month)
        nav_layout.addWidget(self.prev_btn)
        
        self.month_label = QLabel()
        self.month_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(self.month_label, stretch=1)
        
        self.next_btn = QPushButton("►")
        self.next_btn.setFixedSize(40, 30)
        self.next_btn.clicked.connect(self._next_month)
        nav_layout.addWidget(self.next_btn)
        
        layout.addLayout(nav_layout)
        
        # 日历表格
        self.calendar_table = QTableWidget()
        self.calendar_table.setRowCount(6)
        self.calendar_table.setColumnCount(7)
        self.calendar_table.horizontalHeader().setVisible(True)
        self.calendar_table.verticalHeader().setVisible(False)
        self.calendar_table.setShowGrid(True)
        self.calendar_table.horizontalHeader().setStretchLastSection(True)
        
        # 设置列标题 (周一到周日)
        headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.calendar_table.setHorizontalHeaderLabels(headers)
        
        # 设置列宽相等
        for i in range(7):
            self.calendar_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        # 连接双击信号
        self.calendar_table.cellDoubleClicked.connect(self._on_cell_double_clicked)
        
        # 启用拖拽接受
        self.calendar_table.setAcceptDrops(True)
        self.calendar_table.setDropIndicatorShown(True)
        
        layout.addWidget(self.calendar_table)
    
    def _render_calendar(self):
        """渲染日历"""
        from calendar import monthrange
        
        # 更新月份标签
        self.month_label.setText(f"{self.year}年{self.month}月")
        self.month_changed.emit(self.year, self.month)
        
        # 获取当月信息
        days_in_month = monthrange(self.year, self.month)[1]
        first_day = QDate(self.year, self.month, 1)
        start_weekday = first_day.dayOfWeek() - 1  # Qt: 1=周一，转换为 0=周一
        
        # 清空表格
        self.calendar_table.clearContents()
        
        # 计算需要显示的总天数 (前月 + 当月 + 后月)
        current_row = 0
        current_col = 0
        
        # 填充前一个月的日期
        prev_month = 12 if self.month == 1 else self.month - 1
        prev_year = self.year - 1 if self.month == 1 else self.year
        prev_month_days = monthrange(prev_year, prev_month)[1]
        
        for day in range(prev_month_days - start_weekday + 1, prev_month_days + 1):
            item = QTableWidgetItem(str(day))
            item.setForeground(QColor("#CCCCCC"))
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.calendar_table.setItem(current_row, current_col, item)
            current_col += 1
        
        # 填充当月日期
        for day in range(1, days_in_month + 1):
            current_date = QDate(self.year, self.month, day)
            item = QTableWidgetItem(str(day))
            
            # 获取当天任务数
            tasks = self.task_service.get_tasks_by_date(current_date.toPyDate())
            if tasks:
                item.setText(f"{day}\n({len(tasks)})")
            
            # 标记今天
            if current_date == QDate.currentDate():
                item.setBackground(QColor("#3498db"))
                item.setForeground(QColor("#FFFFFF"))
                item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            
            # 标记选中日期
            if current_date == self.selected_date:
                item.setBackground(QColor("#2980b9"))
            
            # 标记周末
            if current_date.dayOfWeek() >= 6:
                if current_date != QDate.currentDate():
                    item.setForeground(QColor("#e74c3c"))
            
            self.calendar_table.setItem(current_row, current_col, item)
            
            current_col += 1
            if current_col == 7:
                current_col = 0
                current_row += 1
        
        # 填充后一个月的日期
        next_month = 1 if self.month == 12 else self.month + 1
        next_year = self.year + 1 if self.month == 12 else self.year
        remaining = 42 - (current_row * 7 + current_col)
        
        for day in range(1, remaining + 1):
            item = QTableWidgetItem(str(day))
            item.setForeground(QColor("#CCCCCC"))
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.calendar_table.setItem(current_row, current_col, item)
            current_col += 1
            if current_col == 7:
                current_col = 0
                current_row += 1
    
    def _prev_month(self):
        """切换到上月"""
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self._render_calendar()
    
    def _next_month(self):
        """切换到下月"""
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self._render_calendar()
    
    def navigate_to(self, year: int, month: int):
        """导航到指定年月"""
        self.year = year
        self.month = month
        self._render_calendar()
    
    def _on_cell_double_clicked(self, row: int, col: int):
        """双击单元格事件 - 创建任务"""
        item = self.calendar_table.item(row, col)
        if item and item.text().isdigit():
            day = int(item.text())
            # 判断是当月还是前后月
            current_date = QDate(self.year, self.month, day)
            self.date_double_clicked.emit(current_date)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasFormat('task/id'):
            event.acceptProposedAction()
            # 高亮显示目标格子
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            super().dragEnterEvent(event)
    
    def dragLeaveEvent(self, event):
        """拖拽离开事件"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().dragLeaveEvent(event)
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放置事件 - 修改任务日期"""
        if event.mimeData().hasFormat('task/id'):
            task_id = int(event.mimeData().data('task/id').data())
            
            # 获取放置位置的日期
            pos = self.calendar_table.viewport().mapFromGlobal(event.globalPos())
            item = self.calendar_table.itemAt(pos)
            
            if item and item.text().isdigit():
                day = int(item.text())
                new_date = QDate(self.year, self.month, day).toPyDate()
                
                # 发射信号通知主窗口更新
                self.date_selected.emit(QDate(self.year, self.month, day))
                
                # 更新任务日期 (通过主窗口回调)
                if hasattr(self, 'on_task_dropped'):
                    self.on_task_dropped(task_id, new_date)
                
                event.acceptProposedAction()
                
                # 显示提示
                QToolTip.showText(event.globalPos(), f"任务已移动到 {new_date}")
        else:
            super().dropEvent(event)
