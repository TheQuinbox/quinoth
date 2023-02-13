import wx
import application

def popup_input(title, text, value=""):
	dlg = wx.TextEntryDialog(application.main_window, text, title, value=value)
	result = dlg.ShowModal()
	dlg.Destroy()
	if result != wx.ID_OK:
		return ""
	return dlg.GetValue()

def popup_error(title, text):
	wx.MessageBox (text, title, wx.ICON_ERROR)
