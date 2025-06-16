from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QUrl, QObject, QEvent
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QSizePolicy, QWhatsThis  # 添加此导入
from functools import partial
import os
import subprocess
import win32api
import win32con
from win32com.client import Dispatch
from win32com.shell import shell, shellcon
from main_window import MainWindow
from autostart import unset_autostart
from shortcuts.manager import ShortcutManager

class TrayIcon:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if TrayIcon._instance is not None:
            raise Exception("TrayIcon 是单例类，请使用 get_instance() 方法获取实例")
            
        self.tray_icon = QtWidgets.QSystemTrayIcon()
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        self.tray_icon.setIcon(QtGui.QIcon(icon_path))
        
        self.manager = ShortcutManager()
        self.menu = None
        self.main_window = None
        self.current_process = None
        
        self.create_menu()
        self.tray_icon.setVisible(True)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def create_menu(self):
        """创建新的菜单实例"""
        self.menu = QtWidgets.QMenu()
        self.populate_menu()
        self.tray_icon.setContextMenu(self.menu)

    def populate_menu(self):
        """填充菜单内容"""
        if not self.menu:
            return
            
        self.menu.clear()
        self.menu.addAction("管理快捷方式", self.show_main_window)
        self.menu.addSeparator()
        
        # 添加快捷方式菜单项
        for shortcut in self.manager.list_shortcuts():
            action = QtWidgets.QAction(shortcut['name'], self.menu)
            action.triggered.connect(partial(self.open_shortcut, shortcut['path']))
            self.menu.addAction(action)
            
        self.menu.addSeparator()
        self.menu.addAction("关于", self.show_about)  # 添加关于菜单项
        self.menu.addAction("卸载", self.uninstall_app)
        self.menu.addAction("退出", self.exit_application)

    def show_main_window(self):
        if self.main_window is None:
            self.main_window = MainWindow()
            self.main_window.refresh_tray_menu = self.refresh_and_update_menu
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()

    def refresh_and_update_menu(self):
        """强制刷新菜单"""
        # 重新加载快捷方式
        self.manager = ShortcutManager()
        # 重新创建并显示菜单
        self.create_menu()
        # 立即显示更新后的菜单
        if self.tray_icon.isVisible():
            self.menu.popup(QtGui.QCursor.pos())

    def on_tray_icon_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.menu.exec_(QtGui.QCursor.pos())

    def open_shortcut(self, path):
        """打开快捷方式指向的文件或文件夹"""
        try:
            if not os.path.exists(path):
                QtWidgets.QMessageBox.warning(
                    None,
                    "错误",
                    f"路径不存在：{path}"
                )
                return
                
            if os.path.isdir(path):
                # 使用 win32api.ShellExecute 打开文件夹
                win32api.ShellExecute(
                    0,          # hwnd
                    'explore',  # 操作
                    path,       # 文件/文件夹路径
                    None,      # 参数
                    None,      # 工作目录
                    win32con.SW_SHOWNORMAL  # 显示方式
                )
            else:
                # 如果是文件，使用 win32api.ShellExecute 打开
                win32api.ShellExecute(
                    0,        # hwnd
                    'open',   # 操作
                    path,     # 文件路径
                    None,     # 参数
                    None,     # 工作目录
                    win32con.SW_SHOWNORMAL  # 显示方式
                )
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                None,
                "错误",
                f"无法打开路径：{str(e)}"
            )

    def exit_application(self):
        """退出程序时确保清理所有子进程"""
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=1)
            except Exception:
                pass
        QtWidgets.QApplication.quit()

    def uninstall_app(self):
        unset_autostart()
        self.tray_icon.hide()
        QtWidgets.QMessageBox.information(None, "卸载", "卸载完成，程序即将退出。")
        self.exit_application()

    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h3>快捷启动管理器</h3>
        <p>版本：1.0.0</p>
        <p>一个简单的快捷方式管理工具，帮助你快速启动常用程序和文件夹。</p>
        <p>作者：埃及猪肉</p>
        <p><a href="https://pattianfang.github.io/">Blog</a></p>
        """
        
        about_dialog = QtWidgets.QDialog()
        about_dialog.setWindowTitle("关于")
        about_dialog.setFixedSize(400, 300)
        about_dialog.setSizeGripEnabled(False)
        
        # 移除问号按钮
        about_dialog.setWindowFlags(
            about_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint
        )

        # 设置对话框图标
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            about_dialog.setWindowIcon(QtGui.QIcon(icon_path))
        
        layout = QtWidgets.QVBoxLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)  # 设置布局大小约束
        
        # 添加图标
        icon_label = QtWidgets.QLabel()
        icon = QtGui.QIcon(icon_path)
        if not icon.isNull():
            icon_label.setPixmap(icon.pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # 添加文本
        text_label = QtWidgets.QLabel(about_text)
        text_label.setOpenExternalLinks(True)
        text_label.setTextFormat(Qt.RichText)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 文本标签大小策略
        layout.addWidget(text_label)
        
        # 添加确定按钮
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
        )
        button_box.accepted.connect(about_dialog.accept)
        layout.addWidget(button_box)
        
        about_dialog.setLayout(layout)
        about_dialog.exec_()
