import http.server
import socketserver
import json

from core.utils import sign_verifier
from core.db.utils import database
from core.config import settings


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if sign_verifier(data):
            database.put_data(data)
            result = 'SUCCESS'
        else:
            result = 'FAILED'

        with open(f'./ipn_transaction_log.txt', 'a') as file:
            file.write(post_data.decode())
            file.write(f' - {result}\n')

        self.wfile.write(result.encode())


# Set the server address and port
server_address = ('', settings.PORT)

# Create an instance of the server with the defined request handler
httpd = socketserver.TCPServer(server_address, MyRequestHandler)

# Start the server
print(f'Server running on port {settings.PORT}...')
httpd.serve_forever()
