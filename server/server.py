import http.server
import socketserver
import json
from dotenv import load_dotenv

from server.utils import sign_verificator
from server.db.utils import database


load_dotenv()


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if sign_verificator(data):
            database.put_data(data)
            result = 'SUCCESS'
        else:
            result = 'FAILED'

        with open(f'./ipn_transactions_log.txt', 'a') as file:
            file.write(post_data.decode())
            file.write(f' - {result}\n')

        self.wfile.write(result.encode())


# Set the server address and port
server_address = ('', 8000)

# Create an instance of the server with the defined request handler
httpd = socketserver.TCPServer(server_address, MyRequestHandler)

# Start the server
print('Server running on port 8000...')
httpd.serve_forever()
