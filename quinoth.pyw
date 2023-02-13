import application
import logger

def main():
	logger.setup()
	application.main_window.Show()
	application.wx_app.MainLoop()

if __name__ == "__main__":
	main()
