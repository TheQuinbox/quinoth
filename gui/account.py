import wx
from pubsub import pub
import application

class AccountManagerDialog(wx.Dialog):
	def __init__(self):
		super().__init__(application.main_window, title="Accounts")
		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		listSizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(panel, -1, "Accounts")
		self.list = wx.ListBox(panel, wx.ID_ANY)
		listSizer.Add(label, 0, wx.ALL, 5)
		listSizer.Add(self.list, 0, wx.ALL, 5)
		sizer.Add(listSizer, 0, wx.ALL, 5)
		add = wx.Button(panel, wx.ID_ANY, "&Add")
		add.Bind(wx.EVT_BUTTON, lambda e: pub.sendMessage("account_manager.add_account"))
		switch = wx.Button(panel, wx.ID_ANY, "&Switch")
		switch.SetDefault()
		switch.Bind(wx.EVT_BUTTON, self.on_switch)
		close = wx.Button(panel, wx.ID_CANCEL, "&Close")
		close.Bind(wx.EVT_BUTTON, self.on_close)
		buttons = wx.BoxSizer(wx.HORIZONTAL)
		buttons.Add(add, 0, wx.ALL, 5)
		buttons.Add(switch, 0, wx.ALL, 5)
		buttons.Add(close, 0, wx.ALL, 5)
		sizer.Add(buttons, 0, wx.ALL, 5)
		panel.SetSizer(sizer)
		min = sizer.CalcMin()
		self.SetClientSize(min)

	def populate_list(self, accounts):
		for account in accounts:
			self.list.Append(account.credentials["username"])
		if self.list.GetCount() > 0:
			self.list.SetSelection(0)
		self.list.SetSize(self.list.GetBestSize())

	def on_close(self, event):
		self.Destroy()

	def on_switch(self, event):
		pub.sendMessage("account_manager.switch_account", id=self.list.GetSelection())
		self.Destroy()
