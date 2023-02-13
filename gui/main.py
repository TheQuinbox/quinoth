import wx
from pubsub import pub
import application

class MainWindow(wx.Frame):
	def __init__(self):
		super().__init__(None, title=f"{application.name} {application.version}")
		self.create_menu_bar()

	def create_menu_bar(self):
		menu_bar = wx.MenuBar()
		app = wx.Menu()
		manage_accounts = app.Append(wx.ID_ANY, "&Manage accounts")
		app.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("account_manager.show_gui"), manage_accounts)
		menu_bar.Append(app, f"&{application.name}")
		self.SetMenuBar(menu_bar)
