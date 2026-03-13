"""
搜索结果面板 - 现代简约设计
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QPushButton, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor


class SearchResultsPanel(QWidget):
    """搜索结果面板"""
    
    result_selected = pyqtSignal(int)  # task_id
    clear_search = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.setFixedWidth(400)
        self.setMaximumHeight(500)
        self.setVisible(False)
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        self.setObjectName("searchResultsPanel")
        
        # 设置现代化样式
        self.setStyleSheet("""
            QWidget#searchResultsPanel {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题栏
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(16, 12, 16, 12)
        
        self.title_label = QLabel("🔍 搜索结果")
        self.title_label.setFont(QFont("Microsoft YaHei", 13, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #1F2937;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        # 清除按钮
        self.clear_btn = QPushButton("✕")
        self.clear_btn.setFixedSize(28, 28)
        self.clear_btn.setToolTip("关闭搜索结果")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 14px;
                background-color: #F3F4F6;
                color: #6B7280;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
                color: #1F2937;
            }
            QPushButton:pressed {
                background-color: #D1D5DB;
            }
        """)
        self.clear_btn.clicked.connect(lambda: self.clear_search.emit())
        header_layout.addWidget(self.clear_btn)
        
        layout.addLayout(header_layout)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #E5E7EB; max-height: 1px;")
        layout.addWidget(separator)
        
        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #FFFFFF;
            }
            QScrollBar:vertical {
                background-color: #F3F4F6;
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #D1D5DB;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9CA3AF;
            }
        """)
        
        # 内容容器
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(12)
        self.content_layout.addStretch()
        
        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)
        
        # 空状态提示
        self.empty_label = QLabel("暂无搜索结果")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("""
            color: #9CA3AF;
            font-size: 14px;
            padding: 40px;
        """)
        self.empty_label.setVisible(False)
    
    def show_results(self, tasks, keyword: str = ""):
        """显示搜索结果"""
        # 清空现有内容
        self._clear_content()
        
        if not tasks:
            self.empty_label.setVisible(True)
            self.title_label.setText(f"🔍 搜索结果 (0)")
        else:
            self.empty_label.setVisible(False)
            self.title_label.setText(f"🔍 搜索结果 ({len(tasks)})")
            
            # 添加搜索结果项
            for task in tasks:
                self._add_result_item(task)
        
        self.setVisible(True)
    
    def _add_result_item(self, task):
        """添加搜索结果项"""
        item_widget = QWidget()
        item_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }
            QWidget:hover {
                background-color: #F9FAFB;
                border: 1px solid #3B82F6;
            }
        """)
        
        layout = QVBoxLayout(item_widget)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)
        
        # 标题行
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        
        # 优先级标记
        priority_dot = QLabel("●")
        priority_colors = {3: "#EF4444", 2: "#F59E0B", 1: "#10B981"}
        priority_text = {3: "P0", 2: "P1", 1: "P2"}
        priority_dot.setStyleSheet(f"""
            color: {priority_colors.get(task.priority, '#10B981')};
            font-size: 12px;
            font-weight: bold;
        """)
        title_layout.addWidget(priority_dot)
        
        # 任务标题
        title_label = QLabel(task.title)
        title_label.setFont(QFont("Microsoft YaHei", 13, QFont.Weight.Medium))
        title_label.setStyleSheet("color: #1F2937;")
        title_label.setWordWrap(True)
        title_layout.addWidget(title_label, stretch=1)
        
        layout.addLayout(title_layout)
        
        # 描述 (如果有)
        if task.description:
            desc_label = QLabel(task.description[:80] + ("..." if len(task.description) > 80 else ""))
            desc_label.setStyleSheet("""
                color: #6B7280;
                font-size: 12px;
            """)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # 元信息行
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(12)
        
        # 日期
        date_label = QLabel(f"📅 {task.due_date.strftime('%Y-%m-%d')}")
        date_label.setStyleSheet("""
            color: #9CA3AF;
            font-size: 11px;
        """)
        meta_layout.addWidget(date_label)
        
        # 状态
        status_colors = {0: "#F59E0B", 1: "#3B82F6", 2: "#10B981"}
        status_text = {0: "待处理", 1: "进行中", 2: "已完成"}
        status_label = QLabel(f"● {status_text.get(task.status, '待处理')}")
        status_label.setStyleSheet(f"""
            color: {status_colors.get(task.status, '#F59E0B')};
            font-size: 11px;
            font-weight: 500;
        """)
        meta_layout.addWidget(status_label)
        
        # 分类 (如果有)
        if task.category:
            category_label = QLabel(f"{task.category.icon} {task.category.name}")
            category_label.setStyleSheet("""
                color: #6B7280;
                font-size: 11px;
            """)
            meta_layout.addWidget(category_label)
        
        meta_layout.addStretch()
        layout.addLayout(meta_layout)
        
        # 添加到布局
        self.content_layout.insertWidget(self.content_layout.count() - 1, item_widget)
        
        # 点击事件
        item_widget.mousePressEvent = lambda e: self._on_item_clicked(task.id)
        item_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 悬停效果
        self._add_hover_effect(item_widget)
    
    def _on_item_clicked(self, task_id: int):
        """点击结果项"""
        self.result_selected.emit(task_id)
        self.setVisible(False)
    
    def _clear_content(self):
        """清空内容"""
        while self.content_layout.count() > 1:
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.empty_label.setVisible(False)
    
    def _add_hover_effect(self, widget):
        """添加悬停效果"""
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(1.0)
        widget.setGraphicsEffect(effect)
        
        widget.enterEvent = lambda e: self._on_hover_enter(widget)
        widget.leaveEvent = lambda e: self._on_hover_leave(widget)
    
    def _on_hover_enter(self, widget):
        """鼠标进入"""
        pass  # 通过样式表处理
    
    def _on_hover_leave(self, widget):
        """鼠标离开"""
        pass
