"""
主窗口组件
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QStatusBar,
    QSplitter, QFrame, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QAction

from src.database.db_manager import get_session
from src.services.task_service import TaskService
from src.services.calendar_service import CalendarService
from src.services.search_service import SearchService
from src.services.filter_service import FilterService
from src.services.reminder_service import ReminderService
from src.services.stats_service import StatsService
from src.ui.calendar_view import CalendarView
from src.ui.task_list import TaskListWidget
from src.ui.category_panel import CategoryPanel
from src.ui.task_dialog import TaskDialog
from src.ui.search_bar import SearchBar
from src.ui.week_view import WeekView
from src.ui.day_view import DayView
from src.ui.stats_panel import StatsPanel
import src.models.category


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化服务
        self.session = get_session().__enter__()
        self.task_service = TaskService(self.session)
        self.calendar_service = CalendarService()
        self.search_service = SearchService(self.session)
        self.filter_service = FilterService(self.session)
        self.reminder_service = ReminderService(self.session)
        self.stats_service = StatsService(self.session)
        
        # 当前选中的日期
        self.current_year = QDate.currentDate().year()
        self.current_month = QDate.currentDate().month()
        self.selected_date = QDate.currentDate()
        
        # 当前视图模式
        self.current_view = "month"  # month, week, day
        
        # 初始化 UI
        self._init_ui()
        self._create_menu_bar()
        self._create_status_bar()
        
        # 加载数据
        self._load_data()
    
    def _init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Todo Calendar - Phase 2")
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 顶部：搜索栏 + 视图切换
        top_bar_layout = QHBoxLayout()
        
        # 搜索栏 (P1-2, P1-3)
        self.search_bar = SearchBar()
        self.search_bar.search_triggered.connect(self._on_search_triggered)
        self.search_bar.filter_changed.connect(self._on_filter_changed)
        self.search_bar.clear_search.connect(self._on_clear_search)
        top_bar_layout.addWidget(self.search_bar, stretch=1)
        
        # 视图切换按钮 (P1-1)
        view_btn_layout = QHBoxLayout()
        view_btn_layout.setSpacing(5)
        
        self.month_view_btn = QPushButton("📅 Month")
        self.month_view_btn.setFixedHeight(32)
        self.month_view_btn.clicked.connect(lambda: self._switch_view("month"))
        view_btn_layout.addWidget(self.month_view_btn)
        
        self.week_view_btn = QPushButton("📆 Week")
        self.week_view_btn.setFixedHeight(32)
        self.week_view_btn.clicked.connect(lambda: self._switch_view("week"))
        view_btn_layout.addWidget(self.week_view_btn)
        
        self.day_view_btn = QPushButton("📋 Day")
        self.day_view_btn.setFixedHeight(32)
        self.day_view_btn.clicked.connect(lambda: self._switch_view("day"))
        view_btn_layout.addWidget(self.day_view_btn)
        
        top_bar_layout.addLayout(view_btn_layout)
        
        main_layout.addLayout(top_bar_layout)
        
        # 创建分割器 (左侧分类 + 中间视图 + 右侧统计)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：分类面板
        self.category_panel = CategoryPanel(self.session, self.task_service)
        self.category_panel.category_selected.connect(self._on_category_selected)
        splitter.addWidget(self.category_panel)
        
        # 中间：视图区域 (月/周/日)
        self.view_container = QWidget()
        self.view_layout = QVBoxLayout(self.view_container)
        self.view_layout.setContentsMargins(0, 0, 0, 0)
        
        # 日历视图 (默认)
        self.calendar_view = CalendarView(
            self.current_year, 
            self.current_month,
            self.task_service,
            on_task_dropped_callback=self._on_task_dropped
        )
        self.calendar_view.date_selected.connect(self._on_date_selected)
        self.calendar_view.date_double_clicked.connect(self._add_task_on_date)
        self.calendar_view.month_changed.connect(self._on_month_changed)
        self.view_layout.addWidget(self.calendar_view, stretch=1)
        
        # 周视图 (P1-1)
        self.week_view = WeekView(self.task_service)
        self.week_view.date_selected.connect(self._on_date_selected)
        self.week_view.hide()
        self.view_layout.addWidget(self.week_view, stretch=1)
        
        # 日视图 (P1-1)
        self.day_view = DayView(self.task_service)
        self.day_view.date_selected.connect(self._on_date_selected)
        self.day_view.hide()
        self.view_layout.addWidget(self.day_view, stretch=1)
        
        splitter.addWidget(self.view_container)
        
        # 右侧：统计面板 (P1-6)
        self.stats_panel = StatsPanel()
        self.stats_panel.setFixedWidth(280)
        splitter.addWidget(self.stats_panel)
        
        # 设置分割器初始比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)
        
        main_layout.addWidget(splitter)
        
        # 底部：任务列表
        task_list_frame = QFrame()
        task_list_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        task_list_layout = QVBoxLayout(task_list_frame)
        task_list_layout.setContentsMargins(10, 10, 10, 10)
        
        # 任务列表标题栏
        title_layout = QHBoxLayout()
        self.task_count_label = QLabel("Today's Tasks")
        self.task_count_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_layout.addWidget(self.task_count_label)
        
        title_layout.addStretch()
        
        self.add_task_btn = QPushButton("+ Add Task")
        self.add_task_btn.clicked.connect(self._add_task)
        title_layout.addWidget(self.add_task_btn)
        
        task_list_layout.addLayout(title_layout)
        
        # 任务列表
        self.task_list = TaskListWidget(self.task_service)
        self.task_list.task_completed.connect(self._on_task_completed)
        self.task_list.task_edited.connect(self._edit_task)
        self.task_list.task_deleted.connect(self._on_task_deleted)
        self.task_list.tasks_bulk_deleted.connect(self._on_tasks_bulk_deleted)
        
        # 添加 Ctrl+A 全选快捷键
        from PyQt6.QtGui import QShortcut, QKeySequence
        select_all_shortcut = QShortcut(QKeySequence("Ctrl+A"), self.task_list)
        select_all_shortcut.activated.connect(self.task_list.selectAll)
        
        task_list_layout.addWidget(self.task_list, stretch=1)
        
        main_layout.addWidget(task_list_frame, stretch=1)
    
    def _create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("&File")
        
        export_action = QAction("&Export Data", self)
        export_action.triggered.connect(self._export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("&Edit")
        
        add_task_action = QAction("&Add Task", self)
        add_task_action.triggered.connect(self._add_task)
        edit_menu.addAction(add_task_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("&View")
        
        month_action = QAction("&Month View", self)
        month_action.triggered.connect(lambda: self._switch_view("month"))
        view_menu.addAction(month_action)
        
        week_action = QAction("&Week View", self)
        week_action.triggered.connect(lambda: self._switch_view("week"))
        view_menu.addAction(week_action)
        
        day_action = QAction("&Day View", self)
        day_action.triggered.connect(lambda: self._switch_view("day"))
        view_menu.addAction(day_action)
        
        view_menu.addSeparator()
        
        today_action = QAction("&Today", self)
        today_action.triggered.connect(self._go_to_today)
        view_menu.addAction(today_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu("&Tools")
        
        reminder_action = QAction("📢 Show Reminders", self)
        reminder_action.triggered.connect(self._show_reminders)
        tools_menu.addAction(reminder_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self._update_status_bar()
    
    def _update_status_bar(self):
        """更新状态栏信息"""
        stats = self.task_service.get_task_count_by_status()
        self.status_bar.showMessage(
            f"Tasks: {stats['total']} | Completed: {stats['completed']} | Pending: {stats['pending']}"
        )
    
    def _load_data(self):
        """加载初始数据"""
        self._refresh_task_list()
        self._update_stats()
        self._load_categories_to_search()
    
    def _load_categories_to_search(self):
        """加载分类到搜索栏"""
        categories = self.session.query(src.models.category.Category).all()
        cat_list = [(cat.id, cat.name, cat.icon) for cat in categories]
        self.search_bar.load_categories(cat_list)
    
    def _update_stats(self):
        """更新统计面板"""
        stats_report = self.stats_service.get_full_report()
        self.stats_panel.update_stats(stats_report)
    
    def _switch_view(self, view_mode: str):
        """切换视图模式 (P1-1)"""
        self.current_view = view_mode
        
        # 隐藏所有视图
        self.calendar_view.hide()
        self.week_view.hide()
        self.day_view.hide()
        
        # 显示选中视图
        if view_mode == "month":
            self.calendar_view.show()
            self.month_view_btn.setStyleSheet("background-color: #3498db; color: white;")
            self.week_view_btn.setStyleSheet("")
            self.day_view_btn.setStyleSheet("")
        elif view_mode == "week":
            self.week_view.show()
            self.month_view_btn.setStyleSheet("")
            self.week_view_btn.setStyleSheet("background-color: #3498db; color: white;")
            self.day_view_btn.setStyleSheet("")
        elif view_mode == "day":
            self.day_view.show()
            self.month_view_btn.setStyleSheet("")
            self.week_view_btn.setStyleSheet("")
            self.day_view_btn.setStyleSheet("background-color: #3498db; color: white;")
        
        # 刷新任务列表
        self._refresh_task_list()
    
    def _on_search_triggered(self, keyword: str):
        """搜索触发 (P1-2)"""
        if not keyword:
            self._refresh_task_list()
            return
        
        # 使用搜索服务
        tasks = self.search_service.search_by_keyword(keyword)
        self.task_list.load_tasks(tasks)
        self.task_count_label.setText(f"Search results for '{keyword}'")
    
    def _on_filter_changed(self, filters: dict):
        """过滤条件变化 (P1-3)"""
        # 应用过滤
        tasks = self.filter_service.apply_multiple_filters(
            category_id=filters.get('category_id'),
            priority=filters.get('priority'),
            status=filters.get('status')
        )
        self.task_list.load_tasks(tasks)
        self.task_count_label.setText(f"Filtered tasks ({len(tasks)})")
    
    def _on_clear_search(self):
        """清除搜索"""
        self._refresh_task_list()
        self.task_count_label.setText(f"Tasks for {self.selected_date.toString('MMMM d, yyyy')}")
    
    def _show_reminders(self):
        """显示提醒 (P1-5)"""
        reminder_message = self.reminder_service.generate_daily_reminder_message()
        self.status_bar.showMessage(reminder_message, 10000)
    
    def _refresh_task_list(self):
        """刷新任务列表"""
        tasks = self.task_service.get_tasks_by_date(self.selected_date.toPyDate())
        self.task_list.load_tasks(tasks)
        self.task_count_label.setText(f"Tasks for {self.selected_date.toString('MMMM d, yyyy')}")
        self._update_status_bar()
        self._update_stats()
    
    def _on_date_selected(self, qdate: QDate):
        """日期选择事件"""
        self.selected_date = qdate
        
        # 如果切换到日视图，同步日期
        if self.current_view == "day":
            self.day_view.navigate_to_date(qdate)
        
        self._refresh_task_list()
    
    def _on_month_changed(self, year: int, month: int):
        """月份切换事件"""
        self.current_year = year
        self.current_month = month
        self._update_stats()
    
    def _on_category_selected(self, category_id: int):
        """分类选择事件"""
        # 使用过滤服务
        tasks = self.filter_service.filter_by_category(category_id)
        self.task_list.load_tasks(tasks)
        self.task_count_label.setText(f"Category tasks ({len(tasks)})")
        self._update_stats()
    
    def _on_task_completed(self, task_id: int, completed: bool):
        """任务完成状态变更"""
        if completed:
            self.task_service.mark_complete(task_id)
        else:
            self.task_service.update_task(task_id, status=0, completed_at=None)
        self._refresh_task_list()
        self._update_stats()
    
    def _on_task_deleted(self, task_id: int):
        """任务删除"""
        self._refresh_task_list()
        self._update_stats()
        self.status_bar.showMessage(f"✓ 任务已删除", 2000)
    
    def _on_tasks_bulk_deleted(self, task_ids: list):
        """批量删除任务"""
        self._refresh_task_list()
        self._update_stats()
        self.status_bar.showMessage(f"✓ 已删除 {len(task_ids)} 个任务", 3000)
    
    def _on_task_dropped(self, task_id: int, new_date):
        """任务拖拽到日期 - 更新任务日期"""
        self.task_service.update_task(task_id, due_date=new_date)
        self._refresh_task_list()
        self._update_stats()
        self.status_bar.showMessage(f"✓ 任务已移动到 {new_date}", 3000)
    
    def _add_task(self):
        """添加新任务"""
        dialog = TaskDialog(self.session, self.selected_date.toPyDate())
        if dialog.exec():
            self._refresh_task_list()
            self._update_stats()
    
    def _add_task_on_date(self, qdate: QDate):
        """在指定日期创建任务 (双击日历)"""
        dialog = TaskDialog(self.session, qdate.toPyDate())
        if dialog.exec():
            self._refresh_task_list()
            self._update_stats()
    
    def _edit_task(self, task_id: int):
        """编辑任务"""
        task = self.task_service.get_task(task_id)
        if task:
            dialog = TaskDialog(self.session, task.due_date, task)
            if dialog.exec():
                self._refresh_task_list()
                self._update_stats()
    
    def _go_to_today(self):
        """跳转到今天"""
        today = QDate.currentDate()
        self.selected_date = today
        
        # 根据当前视图切换
        if self.current_view == "month":
            self.calendar_view.navigate_to(today.year(), today.month())
        elif self.current_view == "week":
            self.week_view.navigate_to_week(today.year(), today.weekNumber()[0])
        elif self.current_view == "day":
            self.day_view.navigate_to_date(today)
        
        self._refresh_task_list()
    
    def _export_data(self):
        """导出数据"""
        # TODO: 实现数据导出功能
        pass
    
    def _show_about(self):
        """显示关于对话框"""
        # TODO: 实现关于对话框
        pass
    
    def closeEvent(self, event):
        """关闭窗口时清理资源"""
        self.session.close()
        event.accept()
