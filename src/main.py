import sys
from PyQt5.QtWidgets import QApplication
from tray import TrayIcon
from PyQt5.QtCore import Qt

def main():
    # 确保应用程序单例运行
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    app.setQuitOnLastWindowClosed(False)
    
    # 使用单例模式获取托盘实例
    tray_icon = TrayIcon.get_instance()
    
    # 启动时显示主界面
    tray_icon.show_main_window()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()