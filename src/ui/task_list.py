"""
任务列表组件

支持：
- 拖拽修改日期（带视觉反馈）
- ESC 取消拖拽
- 双击编辑任务
- 优先级颜色编码
"""

import logging
from PyQt6.QtWidgets import (
    QListWidget, QListWidgetItem, QCheckBox, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QMenu, QApplication, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QPoint, QPropertyAnimation, QEasingCurve, QDate
from PyQt6.QtGui import QColor, QFont, QPalette, QDrag, QPixmap, QPainter, QCursor

# 日志记录器
logger = logging.getLogger(__name__)


class TaskListWidget(QListWidget):
    """任务列表组件 - 支持拖拽修改日期、批量操作"""
    
    task_completed = pyqtSignal(int, bool)  # task_id, completed
    task_edited = pyqtSignal(int)  # task_id
    task_deleted = pyqtSignal(int)  # task_id
    tasks_bulk_deleted = pyqtSignal(list)  # [task_id]
    task_dropped = pyqtSignal(int, object)  # task_id, new_date
    drag_started = pyqtSignal()  # 拖拽开始信号（用于视觉反馈）
    drag_cancelled = pyqtSignal()  # 拖拽取消信号
    
    def __init__(self, task_service):
        super().__init__()
        
        self.task_service = task_service
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self.itemClicked.connect(self._on_item_clicked)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # 启用拖拽
        self.setDragEnabled(True)
        self.setAcceptDrops(False)  # 列表本身不接受 drop，由日历视图接受
        self.setDropIndicatorShown(True)  # 显示拖拽指示器
        
        # 拖拽状态跟踪
        self._is_dragging = False
        self._dragged_item = None
        
        # 批量操作
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self._selected_task_ids = []
        
        # 现代化样式
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 12px;
                background-color: #FFFFFF;
                outline: none;
            }
            QListWidget::item {
                padding: 14px 16px;
                margin: 6px 0;
                border-radius: 8px;
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
            }
            QListWidget::item:selected {
                background-color: #DBEAFE;
                border: 2px solid #3B82F6;
            }
            QListWidget::item:hover {
                background-color: #F9FAFB;
                border: 1px solid #3B82F6;
            }
            QListWidget::item::drag-indicator {
                background-color: #3B82F6;
                height: 3px;
                border-radius: 2px;
            }
            QListWidget::item:selected:hover {
                background-color: #BFDBFE;
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
        logger.debug(f"任务项被点击：{item}")
    
    def _on_item_double_clicked(self, item):
        """
        双击编辑任务
        
        Args:
            item: 被双击的列表项
        """
        widget = self.itemWidget(item)
        if widget and hasattr(widget, 'task'):
            logger.info(f"双击编辑任务：ID={widget.task.id}")
            self.task_edited.emit(widget.task.id)
    
    def _show_context_menu(self, pos):
        """显示右键菜单"""
        # 检查是否有多个选中项
        selected_items = self.selectedItems()
        
        if len(selected_items) > 1:
            # 批量操作菜单
            menu = QMenu(self)
            menu.setStyleSheet("""
                QMenu {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 8px 0;
                }
                QMenu::item {
                    padding: 10px 20px;
                    margin: 2px 8px;
                    border-radius: 4px;
                    font-size: 13px;
                }
                QMenu::item:selected {
                    background-color: #2196F3;
                    color: white;
                }
                QMenu::separator {
                    height: 1px;
                    background: #e0e0e0;
                    margin: 4px 0;
                }
            """)
            
            bulk_delete_action = menu.addAction(f"🗑️ 删除选中 ({len(selected_items)} 个)")
            bulk_delete_action.triggered.connect(self._bulk_delete)
            
            menu.addSeparator()
            
            cancel_action = menu.addAction("取消")
            cancel_action.triggered.connect(lambda: None)
            
            menu.exec(self.mapToGlobal(pos))
        elif len(selected_items) == 1:
            # 单个任务菜单
            item = selected_items[0]
            widget = self.itemWidget(item)
            if widget and hasattr(widget, 'task'):
                menu = QMenu(self)
                menu.setStyleSheet("""
                    QMenu {
                        background-color: #FFFFFF;
                        border: 1px solid #E5E7EB;
                        border-radius: 8px;
                        padding: 8px 0;
                    }
                    QMenu::item {
                        padding: 10px 20px;
                        margin: 2px 8px;
                        border-radius: 4px;
                        font-size: 13px;
                    }
                    QMenu::item:selected {
                        background-color: #3B82F6;
                        color: #FFFFFF;
                    }
                """)
                
                edit_action = menu.addAction("✏️ 编辑")
                edit_action.triggered.connect(lambda: self.task_edited.emit(widget.task.id))
                
                delete_action = menu.addAction("🗑️ 删除")
                delete_action.triggered.connect(lambda: self._delete_task(widget.task.id))
                
                menu.addSeparator()
                
                # 添加批量操作提示
                select_all_action = menu.addAction("📋 全选 (Ctrl+A)")
                select_all_action.triggered.connect(self.selectAll)
                
                menu.exec(self.mapToGlobal(pos))
    
    def _delete_task(self, task_id):
        """删除单个任务"""
        try:
            # 先获取任务信息（在删除前）
            task = self.task_service.get_task(task_id)
            due_date = task.due_date if task else None
            
            # 删除任务
            if self.task_service.delete_task(task_id):
                # 发送删除信号
                self.task_deleted.emit(task_id)
                
                # 重新加载任务列表
                if due_date:
                    self.load_tasks(self.task_service.get_tasks_by_date(due_date))
                else:
                    # 如果任务不存在，刷新当前视图
                    self.clear()
        except Exception as e:
            logger.error(f"删除任务失败：{e}")
    
    def _bulk_delete(self):
        """批量删除选中的任务"""
        try:
            selected_items = self.selectedItems()
            if not selected_items:
                return
            
            # 收集所有要删除的任务 ID
            task_ids_to_delete = []
            for item in selected_items:
                widget = self.itemWidget(item)
                if widget and hasattr(widget, 'task'):
                    task_ids_to_delete.append(widget.task.id)
            
            if not task_ids_to_delete:
                return
            
            # 批量删除
            deleted_count = 0
            for task_id in task_ids_to_delete:
                if self.task_service.delete_task(task_id):
                    deleted_count += 1
            
            # 发送批量删除信号
            self.tasks_bulk_deleted.emit(task_ids_to_delete)
            
            # 刷新列表
            self.load_tasks(self.task_service.get_tasks_by_date(
                QDate.currentDate().toPyDate()
            ))
            
            logger.info(f"批量删除完成：{deleted_count}/{len(task_ids_to_delete)} 个任务")
            
        except Exception as e:
            logger.error(f"批量删除失败：{e}")


class TaskItemWidget(QWidget):
    """单个任务项组件 - 现代简约设计"""
    
    def __init__(self, task):
        super().__init__()
        self.task = task
        self.drag_start_position = QPoint()
        self._is_dragging = False
        
        # 设置简洁样式 - 白色背景，无边框
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: none;
                border-radius: 8px;
            }
            QWidget:hover {
                background-color: #F9FAFB;
            }
            QWidget[dragging="true"] {
                background-color: #F3F4F6;
                opacity: 0.6;
            }
        """)
        
        # 设置拖拽属性
        self.setProperty('dragging', 'false')
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(12)
        
        # 复选框
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(task.status == 2)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 5px;
                border: 2px solid #E5E7EB;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:hover {
                border-color: #3B82F6;
            }
            QCheckBox::indicator:checked {
                background-color: #3B82F6;
                border-color: #3B82F6;
            }
        """)
        layout.addWidget(self.checkbox)
        
        # 任务信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        
        # 标题行
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        
        # 优先级标记
        priority_dot = QLabel("●")
        priority_colors = {3: "#EF4444", 2: "#F59E0B", 1: "#10B981"}
        priority_dot.setStyleSheet(f"""
            color: {priority_colors.get(task.priority, '#10B981')};
            font-size: 12px;
            font-weight: bold;
        """)
        title_layout.addWidget(priority_dot)
        
        # 标题
        title_label = QLabel(task.title)
        title_label.setFont(QFont("Microsoft YaHei", 13, QFont.Weight.Medium))
        title_label.setStyleSheet("color: #1F2937;")
        title_label.setWordWrap(True)
        
        if task.status == 2:
            # 已完成：删除线 + 灰色
            title_label.setStyleSheet("color: #9CA3AF; text-decoration: line-through;")
        
        title_layout.addWidget(title_label, stretch=1)
        info_layout.addLayout(title_layout)
        
        # 描述 (如果有)
        if task.description:
            desc_label = QLabel(task.description[:80] + ("..." if len(task.description) > 80 else ""))
            desc_label.setFont(QFont("Microsoft YaHei", 12))
            desc_label.setStyleSheet("color: #6B7280;")
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
        
        # 元信息行
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(12)
        
        # 日期
        date_label = QLabel(f"📅 {task.due_date.strftime('%Y-%m-%d')}")
        date_label.setStyleSheet("color: #9CA3AF; font-size: 11px;")
        meta_layout.addWidget(date_label)
        
        # 优先级
        priority_text = {3: "P0 高", 2: "P1 中", 1: "P2 低"}
        priority_label = QLabel(f"{priority_text.get(task.priority, 'P2 低')}")
        priority_label.setStyleSheet(f"""
            color: {priority_colors.get(task.priority, '#10B981')};
            font-size: 11px;
            font-weight: 500;
        """)
        meta_layout.addWidget(priority_label)
        
        # 分类 (如果有)
        if task.category:
            category_label = QLabel(f"{task.category.icon} {task.category.name}")
            category_label.setStyleSheet("color: #6B7280; font-size: 11px;")
            meta_layout.addWidget(category_label)
        
        meta_layout.addStretch()
        info_layout.addLayout(meta_layout)
        
        layout.addLayout(info_layout, stretch=1)
        info_layout.addLayout(meta_layout)
        
        layout.addLayout(info_layout, stretch=1)
    
    def _lighten_color(self, hex_color: str, percent: int) -> str:
        """
        调亮颜色
        
        Args:
            hex_color: 十六进制颜色（如 #FEE2E2）
            percent: 调亮百分比（0-100）
            
        Returns:
            调亮后的十六进制颜色
        """
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        factor = 1 + (percent / 100.0)
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _set_dragging_visual(self, is_dragging: bool):
        """
        设置拖拽视觉反馈
        
        Args:
            is_dragging: 是否正在拖拽
        """
        self._is_dragging = is_dragging
        self.setProperty('dragging', 'true' if is_dragging else 'false')
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        
        if is_dragging:
            # 拖拽开始：降低透明度，显示虚线边框
            logger.debug(f"拖拽开始：任务 '{self.task.title}'")
        else:
            # 拖拽结束：恢复原状
            logger.debug(f"拖拽结束：任务 '{self.task.title}'")
    
    def mousePressEvent(self, event):
        """鼠标按下事件 - 记录拖拽起始位置"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """
        鼠标移动事件 - 启动拖拽
        
        支持 ESC 键取消拖拽
        """
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        
        # 检查移动距离，避免误触
        if (event.pos() - self.drag_start_position).manhattanLength() < 10:
            return
        
        # 拖拽开始：设置视觉反馈
        self._set_dragging_visual(True)
        
        try:
            # 创建拖拽对象
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setData('task/id', str(self.task.id).encode())
            mime_data.setData('task/date', self.task.due_date.isoformat().encode())
            drag.setMimeData(mime_data)
            
            # 创建拖拽预览图（半透明效果）
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.GlobalColor.transparent)
            self.render(pixmap)
            
            # 应用半透明效果到预览图
            painter = QPainter(pixmap)
            painter.setOpacity(0.7)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()
            
            drag.setPixmap(pixmap)
            
            # 设置自定义拖拽光标
            self._drag_cursor = QCursor(Qt.CursorShape.OpenHandCursor)
            drag.setHotSpot(self.rect().center())
            
            # 执行拖拽（MoveAction）
            logger.info(f"开始拖拽任务：ID={self.task.id}, title='{self.task.title}'")
            drop_action = drag.exec(Qt.DropAction.MoveAction)
            
            # 拖拽结束：恢复视觉状态
            self._set_dragging_visual(False)
            
            if drop_action == Qt.DropAction.MoveAction:
                logger.info(f"拖拽成功：任务 '{self.task.title}'")
            elif drop_action == Qt.DropAction.IgnoreAction:
                logger.warning(f"拖拽被取消或忽略：任务 '{self.task.title}'")
            else:
                logger.debug(f"拖拽结束，动作：{drop_action}")
                
        except Exception as e:
            logger.error(f"拖拽过程中发生错误：{e}", exc_info=True)
            self._set_dragging_visual(False)
            raise
    
    def keyPressEvent(self, event):
        """
        键盘事件 - 支持 ESC 取消拖拽
        
        Args:
            event: 键盘事件
        """
        if event.key() == Qt.Key.Key_Escape and self._is_dragging:
            logger.info("ESC 键取消拖拽")
            self._set_dragging_visual(False)
            # 注意：Qt 的拖拽一旦开始就无法真正取消，但我们可以恢复视觉状态
            event.accept()
        else:
            super().keyPressEvent(event)
