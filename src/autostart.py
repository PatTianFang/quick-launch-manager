import os
import sys
import winreg

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "QuickLaunchManager"

def get_exe_path():
    """获取当前程序的可执行文件路径，支持打包和源码运行"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的 exe 路径
        return sys.executable
    else:
        # 源码运行，使用 pythonw 启动
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        main_py = os.path.abspath(os.path.join(os.path.dirname(__file__), "main.py"))
        return f'"{pythonw}" "{main_py}"'

def set_autostart():
    """设置开机自启动"""
    exe_path = get_exe_path()
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        return True
    except Exception as e:
        return f"{e}"

def unset_autostart():
    """取消开机自启动"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP_NAME)
        return True
    except FileNotFoundError:
        return True
    except Exception as e:
        return f"{e}"

def is_autostart_enabled():
    """检测是否已设置开机自启动"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, APP_NAME)
            exe_path = get_exe_path()
            return value == exe_path
    except Exception:
        return False