from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import traceback
import threading
from urllib import parse
from mastodon import Mastodon

def find_unused_port():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	sock.bind(("", 0))
	sock.listen(socket.SOMAXCONN)
	ipaddr, port = sock.getsockname()
	sock.close()
	return port

class OAuthHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		path = [i for i in self.path.split("/") if i]
		if path[0] != "oauth":
			raise ValueError("Unable to process non-OAuth request.")
		callback_data = "?".join(path[1].split("?")[1:])
		parsed_data = parse.parse_qs(callback_data)
		access_token = Mastodon.log_in(client_id=self.server.client_id, client_secret=self.server.client_secret, redirect_uri=self.server.get_oauth_callback_url(), code=parsed_data["code"][0])
		self.server.callback(access_token)
		self.send_response(200)
		self.end_headers()
		self.wfile.write(self.server.success_msg.encode())
		t = threading.Thread(target=self.server.shutdown)
		t.daemon = True
		t.start()

class OAuthServer(HTTPServer):
    allow_reuse_address = 0

    def __init__(self, client_id, client_secret, host='localhost', port=None, handler_class=OAuthHandler, callback=None):
        if not callable(callback):
            raise TypeError("Must provide a callable callback.")
        if port is None:
            port = find_unused_port()
        HTTPServer.__init__(self, (host, port), handler_class)
        self.host, self.port = host, port
        self.callback = callback
        self.client_id = client_id
        self.client_secret = client_secret

    def get_oauth_callback_url(self):
        return f"http://{self.host}:{self.port}/oauth/callback"

	success_msg = """<html>
<head>
<title>Successful login!</title>
</head>
<body>
<h1>Login successful!</h1>
<p>
You have been logged in!
You can now close this window and enjoy the app.
</p>
</body>
</html>"""
