import application
import basic_config
from gui import popups
from gui.account import AccountManagerDialog
import mastodon
import webbrowser
from pathlib import Path
from loguru import logger
from pubsub import pub

class AccountManager:
	def __init__(self):
		self.accounts = []
		self.current_account = None
		self.next_account_id = 0
		self.account_path = Path.cwd() / "config" / "accounts"
		self.account_path.mkdir(parents=True, exist_ok=True)
		self.subscribe_events()
		self.load_accounts()
		if len(self.accounts) == 0:
			self.add_account()
		self.read_config

	def subscribe_events(self):
		pub.subscribe(self.add_account, "account_manager.add_account")
		pub.subscribe(self.switch_account, "account_manager.switch_account")
		pub.subscribe(self.show_gui, "account_manager.show_gui")

	def load_accounts(self):
		for path in self.account_path.iterdir():
			self.load_account(path.name)

	def load_account(self, id):
		account = Account(id)
		account.login()
		self.accounts.append(account)
		self.current_account = account
		self.next_account_id += 1

	def add_account(self):
		account = Account(self.next_account_id)
		if not account.authorize():
			if len(self.accounts) == 0:
				application.wx_app.ExitMainLoop()
			return
		self.accounts.append(account)
		self.current_account = account
		self.next_account_id += 1

	def switch_account(self, id):
		self.current_account = self.accounts[id]
		self.write_config()

	def show_gui(self):
		gui = AccountManagerDialog()
		gui.populate_list(self.accounts)
		gui.Show()

	def write_config(self):
		application.config["current_account"] = self.current_account.id
		application.config.write()

	def read_config(self):
		self.current_account = self.accounts[application.config["current_account"]]

class Account:
	def __init__(self, id):
		self.id = id
		self.access_token = ""
		self.instance_url = ""
		self.api = None
		self.credentials = {}
		config_path = Path.cwd() / "config" / "accounts" / str(self.id)
		config_path.mkdir(parents=True, exist_ok=True)
		config_file = config_path / "account.conf"
		config_file.touch()
		self.config = basic_config.load_configuration(str(config_file))

	def authorize(self):
		instance_url = popups.popup_input("Instance URL", "Enter your instance URL")
		if instance_url == "":
			return False
		try:
			client_id, client_secret = mastodon.Mastodon.create_app("Quinoth", api_base_url=instance_url)
			temporary_api = mastodon.Mastodon(client_id=client_id, client_secret=client_secret, api_base_url=instance_url)
			auth_url = temporary_api.auth_request_url()
		except mastodon.MastodonError as e:
			popups.popup_error("Could not connect to your Mastodon instance", "Please make sure you typed the URL correctly, and try again.")
			logger.error(f"Error connecting to Mastodon instance: {e}")
			return False
		webbrowser.open_new_tab(auth_url)
		code = popups.popup_input("Varification code", "Enter the varification code.")
		if code == "":
			return False
		try:
			access_token = temporary_api.log_in(code=code)
		except mastodon.MastodonError as e:
			popups.popup_error("Could not authorize your account", "Please make sure you entered the varification code correctly, and try again.")
			logger.error(f"Error authorizing account: {e}")
			return False
		self.access_token = access_token
		self.instance_url = instance_url
		self.write_config()
		self.login()

	def login(self):
		self.read_config()
		try:
			self.api = mastodon.Mastodon(access_token=self.access_token, api_base_url=self.instance_url)
			self.credentials = self.api.account_verify_credentials()
		except mastodon.MastodonError as e:
			logger.error(f"Error logging into account: {e}")

	def write_config(self):
		self.config["access_token"] = self.access_token
		self.config["instance_url"] = self.instance_url
		self.config.write()

	def read_config(self):
		self.access_token = self.config["access_token"]
		self.instance_url = self.config["instance_url"]
