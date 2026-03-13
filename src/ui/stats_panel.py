"""
统计面板组件 - 任务数据可视化
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QProgressBar, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class StatsPanel(QWidget):
    """统计面板组件"""
    
    def __init__(self):
        super().__init__()
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("📊 Statistics")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # 基础统计卡片
        self._create_basic_stats(layout)
        
        # 进度条
        self._create_progress_section(layout)
        
        # 优先级统计
        self._create_priority_stats(layout)
        
        # 生产力得分
        self._create_productivity_score(layout)
        
        layout.addStretch()
    
    def _create_basic_stats(self, parent_layout):
        """创建基础统计卡片"""
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        stats_layout = QGridLayout(stats_frame)
        stats_layout.setSpacing(10)
        
        # 总任务数
        self.total_label = self._create_stat_item("Total", "0")
        stats_layout.addWidget(self.total_label, 0, 0)
        
        # 已完成
        self.completed_label = self._create_stat_item("Completed", "0", "#27ae60")
        stats_layout.addWidget(self.completed_label, 0, 1)
        
        # 待办
        self.pending_label = self._create_stat_item("Pending", "0", "#f39c12")
        stats_layout.addWidget(self.pending_label, 1, 0)
        
        # 完成率
        self.rate_label = self._create_stat_item("Rate", "0%")
        stats_layout.addWidget(self.rate_label, 1, 1)
        
        parent_layout.addWidget(stats_frame)
    
    def _create_stat_item(self, title: str, value: str, color: str = None) -> QLabel:
        """创建统计项"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 值
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        if color:
            value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        # 标题
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        title_label.setStyleSheet("color: #666;")
        layout.addWidget(title_label)
        
        return widget
    
    def _create_progress_section(self, parent_layout):
        """创建进度部分"""
        progress_group = QGroupBox("📈 Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        # 总体进度条
        self.total_progress = QProgressBar()
        self.total_progress.setRange(0, 100)
        self.total_progress.setValue(0)
        self.total_progress.setFormat("%p% Completed")
        self.total_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        progress_layout.addWidget(self.total_progress)
        
        # 本周进度
        week_layout = QHBoxLayout()
        week_label = QLabel("This Week:")
        week_label.setFont(QFont("Arial", 10))
        week_layout.addWidget(week_label)
        
        self.week_progress_label = QLabel("0/0")
        self.week_progress_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        week_layout.addWidget(self.week_progress_label, stretch=1)
        
        progress_layout.addLayout(week_layout)
        
        # 本月进度
        month_layout = QHBoxLayout()
        month_label = QLabel("This Month:")
        month_label.setFont(QFont("Arial", 10))
        month_layout.addWidget(month_label)
        
        self.month_progress_label = QLabel("0/0")
        self.month_progress_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        month_layout.addWidget(self.month_progress_label, stretch=1)
        
        progress_layout.addLayout(month_layout)
        
        parent_layout.addWidget(progress_group)
    
    def _create_priority_stats(self, parent_layout):
        """创建优先级统计"""
        priority_group = QGroupBox("🎯 Priority Distribution")
        priority_layout = QVBoxLayout(priority_group)
        
        # 高优先级
        high_layout = QHBoxLayout()
        high_label = QLabel("🔴 High")
        high_label.setFont(QFont("Arial", 10))
        high_layout.addWidget(high_label)
        
        self.high_priority_label = QLabel("0")
        self.high_priority_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.high_priority_label.setStyleSheet("color: #e74c3c;")
        high_layout.addWidget(self.high_priority_label, stretch=1)
        priority_layout.addLayout(high_layout)
        
        # 中优先级
        medium_layout = QHBoxLayout()
        medium_label = QLabel("🟡 Medium")
        medium_label.setFont(QFont("Arial", 10))
        medium_layout.addWidget(medium_label)
        
        self.medium_priority_label = QLabel("0")
        self.medium_priority_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.medium_priority_label.setStyleSheet("color: #f39c12;")
        medium_layout.addWidget(self.medium_priority_label, stretch=1)
        priority_layout.addLayout(medium_layout)
        
        # 低优先级
        low_layout = QHBoxLayout()
        low_label = QLabel("🔵 Low")
        low_label.setFont(QFont("Arial", 10))
        low_layout.addWidget(low_label)
        
        self.low_priority_label = QLabel("0")
        self.low_priority_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.low_priority_label.setStyleSheet("color: #27ae60;")
        low_layout.addWidget(self.low_priority_label, stretch=1)
        priority_layout.addLayout(low_layout)
        
        parent_layout.addWidget(priority_group)
    
    def _create_productivity_score(self, parent_layout):
        """创建生产力得分"""
        score_group = QGroupBox("⚡ Productivity Score")
        score_layout = QVBoxLayout(score_group)
        
        # 得分显示
        self.score_label = QLabel("0")
        self.score_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setStyleSheet("color: #3498db;")
        score_layout.addWidget(self.score_label)
        
        # 说明文字
        desc_label = QLabel("Based on completion rate, priority, and overdue tasks")
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #666;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        score_layout.addWidget(desc_label)
        
        parent_layout.addWidget(score_group)
    
    def update_stats(self, stats_data: dict):
        """
        更新统计数据
        
        Args:
            stats_data: 统计数据字典
        """
        # 基础统计
        basic = stats_data.get('basic', {})
        self.total_label.findChild(QLabel).setText(str(basic.get('total', 0)))
        self.completed_label.findChild(QLabel).setText(str(basic.get('completed', 0)))
        self.pending_label.findChild(QLabel).setText(str(basic.get('pending', 0)))
        self.rate_label.findChild(QLabel).setText(f"{basic.get('completion_rate', 0)}%")
        
        # 进度条
        self.total_progress.setValue(int(basic.get('completion_rate', 0)))
        
        # 周统计
        weekly = stats_data.get('weekly', {})
        week_total = weekly.get('total', 0)
        week_completed = weekly.get('completed', 0)
        self.week_progress_label.setText(f"{week_completed}/{week_total}")
        
        # 月统计
        monthly = stats_data.get('monthly', {})
        month_total = monthly.get('total', 0)
        month_completed = monthly.get('completed', 0)
        self.month_progress_label.setText(f"{month_completed}/{month_total}")
        
        # 优先级统计
        by_priority = stats_data.get('by_priority', {})
        self.high_priority_label.setText(str(by_priority.get(3, {}).get('total', 0)))
        self.medium_priority_label.setText(str(by_priority.get(2, {}).get('total', 0)))
        self.low_priority_label.setText(str(by_priority.get(1, {}).get('total', 0)))
        
        # 生产力得分
        score = stats_data.get('productivity_score', 0)
        self.score_label.setText(str(score))
        
        # 根据得分设置颜色
        if score >= 80:
            color = "#27ae60"  # 绿色
        elif score >= 60:
            color = "#f39c12"  # 黄色
        else:
            color = "#e74c3c"  # 红色
        self.score_label.setStyleSheet(f"color: {color};")
    
    def reset_stats(self):
        """重置统计数据"""
        self.total_label.findChild(QLabel).setText("0")
        self.completed_label.findChild(QLabel).setText("0")
        self.pending_label.findChild(QLabel).setText("0")
        self.rate_label.findChild(QLabel).setText("0%")
        self.total_progress.setValue(0)
        self.week_progress_label.setText("0/0")
        self.month_progress_label.setText("0/0")
        self.high_priority_label.setText("0")
        self.medium_priority_label.setText("0")
        self.low_priority_label.setText("0")
        self.score_label.setText("0")
        self.score_label.setStyleSheet("color: #3498db;")
