"""
搜索栏组件 - 任务搜索 UI
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QToolButton, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction


class SearchBar(QWidget):
    """搜索栏组件"""
    
    search_triggered = pyqtSignal(str)  # 搜索关键词
    filter_changed = pyqtSignal(dict)   # 过滤条件变化
    clear_search = pyqtSignal()         # 清除搜索
    
    def __init__(self):
        super().__init__()
        
        self.current_filters = {
            'keyword': '',
            'category_id': None,
            'priority': None,
            'status': None
        }
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search tasks...")
        self.search_input.setFixedHeight(32)
        self.search_input.textChanged.connect(self._on_search_changed)
        layout.addWidget(self.search_input, stretch=1)
        
        # 清除按钮
        self.clear_btn = QToolButton()
        self.clear_btn.setText("✕")
        self.clear_btn.setFixedSize(32, 32)
        self.clear_btn.setToolTip("Clear search")
        self.clear_btn.clicked.connect(self._clear_search)
        self.clear_btn.setVisible(False)  # 初始隐藏
        layout.addWidget(self.clear_btn)
        
        # 过滤按钮
        self.filter_btn = QToolButton()
        self.filter_btn.setText("⚙️ Filter")
        self.filter_btn.setFixedHeight(32)
        self.filter_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        # InstantPopup 模式会自动显示菜单，不需要连接 clicked 信号
        layout.addWidget(self.filter_btn)
        
        # 创建过滤菜单
        self._create_filter_menu()
    
    def _create_filter_menu(self):
        """创建过滤菜单"""
        self.filter_menu = QMenu(self)
        self.filter_btn.setMenu(self.filter_menu)
        
        # 状态过滤
        status_menu = self.filter_menu.addMenu("📊 Status")
        self.status_actions = {
            None: status_menu.addAction("All"),
            0: status_menu.addAction("⏳ Pending"),
            1: status_menu.addAction("🔄 In Progress"),
            2: status_menu.addAction("✅ Completed")
        }
        
        for status, action in self.status_actions.items():
            action.setCheckable(True)
            if status is None:
                action.setChecked(True)
            action.triggered.connect(
                lambda checked, s=status: self._on_status_filter_changed(s)
            )
        
        # 优先级过滤
        priority_menu = self.filter_menu.addMenu("🎯 Priority")
        self.priority_actions = {
            None: priority_menu.addAction("All"),
            3: priority_menu.addAction("🔴 High"),
            2: priority_menu.addAction("🟡 Medium"),
            1: priority_menu.addAction("🔵 Low")
        }
        
        for priority, action in self.priority_actions.items():
            action.setCheckable(True)
            if priority is None:
                action.setChecked(True)
            action.triggered.connect(
                lambda checked, p=priority: self._on_priority_filter_changed(p)
            )
        
        # 分类过滤 (动态加载)
        self.category_menu = self.filter_menu.addMenu("📁 Category")
        self.category_actions = {}
        
        # 重置过滤
        reset_action = self.filter_menu.addAction("🔄 Reset Filters")
        reset_action.triggered.connect(self._reset_filters)
    
    def _on_search_changed(self, text: str):
        """搜索文本变化"""
        self.current_filters['keyword'] = text.strip()
        self.clear_btn.setVisible(bool(text.strip()))
        self.search_triggered.emit(text.strip())
    
    def _clear_search(self):
        """清除搜索"""
        self.search_input.clear()
        self.clear_btn.setVisible(False)
        self.clear_search.emit()
    
    def _on_status_filter_changed(self, status: int):
        """状态过滤变化"""
        # 取消其他选项
        for s, action in self.status_actions.items():
            if s != status:
                action.setChecked(False)
        
        self.current_filters['status'] = status if status is not None else None
        self._emit_filter_changed()
    
    def _on_priority_filter_changed(self, priority: int):
        """优先级过滤变化"""
        # 取消其他选项
        for p, action in self.priority_actions.items():
            if p != priority:
                action.setChecked(False)
        
        self.current_filters['priority'] = priority if priority is not None else None
        self._emit_filter_changed()
    
    def _on_category_filter_changed(self, category_id: int):
        """分类过滤变化"""
        # 取消其他选项
        for cat_id, action in self.category_actions.items():
            if cat_id != category_id:
                action.setChecked(False)
        
        self.current_filters['category_id'] = category_id if category_id is not None else None
        self._emit_filter_changed()
    
    def _emit_filter_changed(self):
        """发送过滤变化信号"""
        self.filter_changed.emit(self.current_filters.copy())
    
    def _reset_filters(self):
        """重置所有过滤"""
        # 重置状态
        for status, action in self.status_actions.items():
            action.setChecked(status is None)
        
        # 重置优先级
        for priority, action in self.priority_actions.items():
            action.setChecked(priority is None)
        
        # 重置分类
        for cat_id, action in self.category_actions.items():
            action.setChecked(cat_id is None)
        
        # 重置搜索
        self.search_input.clear()
        self.clear_btn.setVisible(False)
        
        # 重置当前过滤
        self.current_filters = {
            'keyword': '',
            'category_id': None,
            'priority': None,
            'status': None
        }
        
        self.clear_search.emit()
        self._emit_filter_changed()
    
    def load_categories(self, categories: list):
        """
        加载分类列表
        
        Args:
            categories: 分类列表 [(id, name, icon)]
        """
        self.category_menu.clear()
        self.category_actions = {}
        
        # 添加"全部"选项
        all_action = self.category_menu.addAction("📋 All")
        all_action.setCheckable(True)
        all_action.setChecked(True)
        all_action.triggered.connect(
            lambda: self._on_category_filter_changed(None)
        )
        self.category_actions[None] = all_action
        
        # 添加分类选项
        for cat_id, name, icon in categories:
            action = self.category_menu.addAction(f"{icon} {name}")
            action.setCheckable(True)
            action.triggered.connect(
                lambda checked, cid=cat_id: self._on_category_filter_changed(cid)
            )
            self.category_actions[cat_id] = action
    
    def set_filter_status(self, status: int):
        """ programmatically 设置状态过滤 """
        if status in self.status_actions:
            self.status_actions[status].trigger()
    
    def set_filter_priority(self, priority: int):
        """programmatically 设置优先级过滤"""
        if priority in self.priority_actions:
            self.priority_actions[priority].trigger()
    
    def get_current_filters(self) -> dict:
        """获取当前过滤条件"""
        return self.current_filters.copy()
