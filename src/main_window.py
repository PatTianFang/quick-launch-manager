from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QListWidget, 
                           QPushButton, QHBoxLayout, QInputDialog, QMessageBox, 
                           QCheckBox, QFileDialog, QListView, QButtonGroup, QRadioButton,
                           QDialog, QLineEdit, QGridLayout, QLabel, QDialogButtonBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
from shortcuts.manager import ShortcutManager
from autostart import set_autostart, unset_autostart, is_autostart_enabled

class AddShortcutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加快捷方式")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(400)
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout(self)
        
        # 名称输入
        name_label = QLabel("名称:", self)
        self.name_edit = QLineEdit(self)
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.name_edit, 0, 1)
        
        # 类型选择
        type_label = QLabel("类型:", self)
        layout.addWidget(type_label, 1, 0)
        
        self.file_radio = QRadioButton("程序/文件", self)
        self.folder_radio = QRadioButton("文件夹", self)
        self.file_radio.setChecked(True)
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(self.file_radio)
        type_layout.addWidget(self.folder_radio)
        layout.addLayout(type_layout, 1, 1)
        
        # 路径选择
        path_label = QLabel("路径:", self)
        self.path_edit = QLineEdit(self)
        self.path_edit.setReadOnly(True)
        browse_btn = QPushButton("浏览...", self)
        browse_btn.clicked.connect(self.browse_path)
        
        layout.addWidget(path_label, 2, 0)
        layout.addWidget(self.path_edit, 2, 1)
        layout.addWidget(browse_btn, 2, 2)
        
        # 确定/取消按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 3, 0, 1, 3)
        
        self.setLayout(layout)
        
    def browse_path(self):
        if self.file_radio.isChecked():
            path, _ = QFileDialog.getOpenFileName(
                self,
                "选择程序或文件",
                "",
                "所有文件 (*.*)"
            )
        else:
            path = QFileDialog.getExistingDirectory(
                self,
                "选择文件夹"
            )
            
        if path:
            self.path_edit.setText(path)
            
            # 如果名称为空，自动使用文件/文件夹名作为快捷方式名称
            if not self.name_edit.text():
                self.name_edit.setText(os.path.basename(path))
    
    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "path": self.path_edit.text()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("快捷启动管理器")
        self.setGeometry(600, 300, 400, 300)
        
        # 设置窗口图标
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.manager = ShortcutManager()
        self.refresh_tray_menu = None  # 托盘刷新回调函数
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.refresh_list()
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("添加")
        edit_btn = QPushButton("编辑")  # 新增编辑按钮
        remove_btn = QPushButton("删除")
        
        add_btn.clicked.connect(self.add_shortcut)
        edit_btn.clicked.connect(self.edit_shortcut)  # 新增编辑功能
        remove_btn.clicked.connect(self.remove_shortcut)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(remove_btn)
        layout.addLayout(btn_layout)

        self.autostart_checkbox = QCheckBox("开机自启动")
        self.autostart_checkbox.setChecked(False)
        self.autostart_checkbox.stateChanged.connect(self.toggle_autostart)
        layout.addWidget(self.autostart_checkbox)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def refresh_list(self):
        self.list_widget.clear()
        for s in self.manager.list_shortcuts():
            self.list_widget.addItem(f"{s['name']} - {s['path']}")

    def add_shortcut(self):
        dialog = AddShortcutDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            if not data["name"] or not data["path"]:
                QMessageBox.warning(self, "错误", "请输入名称和选择路径！")
                return
                
            # 检查名称是否重复
            if any(s["name"] == data["name"] for s in self.manager.list_shortcuts()):
                QMessageBox.warning(self, "错误", "该名称已存在！")
                return
                
            # 添加快捷方式并保存
            self.manager.add_shortcut(data["name"], data["path"])
            # 刷新列表显示
            self.refresh_list()
            # 强制刷新托盘菜单
            if self.refresh_tray_menu:
                self.refresh_tray_menu()
                QMessageBox.information(self, "成功", "快捷方式已添加！")

    def edit_shortcut(self):
        row = self.list_widget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请先选择要编辑的快捷方式")
            return

        shortcuts = self.manager.list_shortcuts()
        current = shortcuts[row]
        
        dialog = AddShortcutDialog(self)
        dialog.name_edit.setText(current['name'])
        dialog.path_edit.setText(current['path'])
        dialog.file_radio.setChecked(True)  # 默认选中"程序/文件"
        
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            # 删除旧的添加新的
            self.manager.remove_shortcut(current['name'])
            self.manager.add_shortcut(data["name"], data["path"])
            
            self.refresh_list()
            if self.refresh_tray_menu:
                self.refresh_tray_menu()

    def remove_shortcut(self):
        row = self.list_widget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请先选择要删除的快捷方式")
            return

        # 获取选中项的快捷方式信息
        shortcuts = self.manager.list_shortcuts()
        if 0 <= row < len(shortcuts):
            shortcut = shortcuts[row]
            # 弹出确认对话框
            reply = QMessageBox.question(self, '确认删除', 
                                       f'确定要删除快捷方式 "{shortcut["name"]}" 吗？',
                                       QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # 使用索引删除快捷方式
                if self.manager.remove_shortcut_by_index(row):
                    self.refresh_list()
                    # 通知托盘刷新菜单
                    if self.refresh_tray_menu:
                        self.refresh_tray_menu()

    def toggle_autostart(self, state):
        if state:
            result = set_autostart()
            if result is True:
                QMessageBox.information(self, "提示", "已成功设置开机自启动。")
            else:
                QMessageBox.warning(self, "错误", f"设置开机自启动失败：{result}")
        else:
            result = unset_autostart()
            if result is True:
                QMessageBox.information(self, "提示", "已取消开机自启动。")
            else:
                QMessageBox.warning(self, "错误", f"取消开机自启动失败：{result}")

    def get_file_or_folder_path(self, default_path=""):
        """获取文件或文件夹路径的统一对话框"""
        dialog = QFileDialog(self)
        # 设置对话框选项
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)  # 使用自定义对话框
        dialog.setFileMode(QFileDialog.AnyFile)  # 允许选择任何文件
        dialog.setViewMode(QFileDialog.Detail)   # 详细视图模式
        
        # 自定义对话框UI
        sidebar = dialog.findChild(QListView, 'sidebar')
        if sidebar:
            sidebar.setVisible(True)  # 显示侧边栏
        
        # 添加自定义按钮到对话框
        layout = dialog.layout()
        file_type_widget = QWidget()
        file_type_layout = QHBoxLayout()
        
        # 创建单选按钮组
        btn_group = QButtonGroup(dialog)
        file_radio = QRadioButton("文件", dialog)
        folder_radio = QRadioButton("文件夹", dialog)
        file_radio.setChecked(True)  # 默认选中"文件"
        
        btn_group.addButton(file_radio)
        btn_group.addButton(folder_radio)
        
        file_type_layout.addWidget(file_radio)
        file_type_layout.addWidget(folder_radio)
        file_type_widget.setLayout(file_type_layout)
        
        # 将单选按钮组添加到对话框
        if layout:
            layout.addWidget(file_type_widget, layout.rowCount(), 0, 1, layout.columnCount())
        
        # 动态更新对话框模式
        def update_file_mode():
            if folder_radio.isChecked():
                dialog.setFileMode(QFileDialog.Directory)
                dialog.setOption(QFileDialog.ShowDirsOnly, True)
            else:
                dialog.setFileMode(QFileDialog.AnyFile)
                dialog.setOption(QFileDialog.ShowDirsOnly, False)
        
        # 连接信号
        btn_group.buttonClicked.connect(update_file_mode)
        
        # 如果有默认路径
        if default_path:
            dialog.selectFile(default_path)
        
        # 执行对话框
        if dialog.exec_() == QFileDialog.Accepted:
            selected_files = dialog.selectedFiles()
            if selected_files:
                return selected_files[0]
        
        return None