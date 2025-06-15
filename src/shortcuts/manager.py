import os
import json

def get_data_path():
    # 推荐用 APPDATA 目录
    appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
    data_dir = os.path.join(appdata, 'QuickLaunchManager')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, "shortcuts.json")

SHORTCUTS_FILE = get_data_path()

class ShortcutManager:
    def __init__(self):
        self.shortcuts = self.load_shortcuts()

    def load_shortcuts(self):
        if os.path.exists(SHORTCUTS_FILE):
            with open(SHORTCUTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_shortcuts(self):
        with open(SHORTCUTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.shortcuts, f, ensure_ascii=False, indent=2)

    def add_shortcut(self, name, path):
        self.shortcuts.append({'name': name, 'path': path})
        self.save_shortcuts()

    def remove_shortcut(self, name):
        self.shortcuts = [s for s in self.shortcuts if s['name'] != name]
        self.save_shortcuts()

    def list_shortcuts(self):
        return self.shortcuts

    def find_shortcut(self, name):
        for s in self.shortcuts:
            if s['name'] == name:
                return s
        return None

    def remove_shortcut_by_index(self, index):
        """按索引删除快捷方式"""
        if 0 <= index < len(self.shortcuts):
            self.shortcuts.pop(index)
            self.save_shortcuts()
            return True
        return False