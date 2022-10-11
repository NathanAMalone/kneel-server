import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_all_orders, get_all_sizes, get_all_styles
from views import get_single_metal, get_single_order, get_single_size, get_single_style
from views import create_order, delete_order, update_order

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        try:
           id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id)  # This is a tuple

    def do_GET(self):
        """Handles GET requests to the server """
        
        response = {}

        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)
            else:
                response = get_all_metals()
            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = {
                    "message": "That metal is not currently in stock for jewelry"
                }

        elif resource == "sizes":
            if id is not None:
                response = get_single_size(id)
            else:
                response = get_all_sizes()
            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = {
                    "message": "That size is not currently available"
                }
        elif resource == "styles":
            if id is not None:
                response = get_single_style(id)
            else:
                response = get_all_styles()
            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = {
                    "message": "That style is not currently available"
                }
        elif resource == "orders":
            if id is not None:
                response = get_single_order(id)
            else:
                response = get_all_orders()
            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = {
                    "message": "That order was never placed, or was cancelled."
                }
        
        else:
            response = []

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
       
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new order
        new_item = None

        # Add a new order to the list. Don't worry about
        # the orange squiggle, you'll define the create_order
        # function next.
        if resource == "orders":
            if "metalId" in post_body and "sizeId" in post_body and "styleId" in post_body and "timestamp" in post_body:
                self._set_headers(201)
                new_item = create_order(post_body)
            else:
                self._set_headers(400)
                new_item = { 
                    "message": f'{"metalId is required" if "metalId" not in post_body else ""}' f'{"sizeId is required" if "sizeId" not in post_body else ""}'\
                    f'{"styleId is required" if "styleId" not in post_body else ""}' f'{"timestamp is required" if "timestamp" not in post_body else ""}'
                }
        
        # Encode the new order and send in response
        self.wfile.write(json.dumps(new_item).encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single order from the list
        if resource == "orders":
            self._set_headers(405)
            message = {
                "message": f'{"VERBOTEN!! Production has begun and modification of orders is not allowed"}'
            }

        # Encode the new order and send in response
        self.wfile.write(json.dumps(message).encode())
        
    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
    # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single order from the list
        if resource == "orders":
            delete_order(id)

    # Encode the new order and send in response
        self.wfile.write("".encode())




# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
