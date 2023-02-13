import wx
from account import AccountManager
from gui.main import MainWindow
import basic_config
from pathlib import Path

name = "Quinoth"
version = "Alpha 1"
wx_app = wx.App()
main_window = MainWindow()
account_manager = AccountManager()
config_path = Path.cwd() / "config" / "config.conf"
config_path.touch()
config = basic_config.load_configuration(str(config_path))
