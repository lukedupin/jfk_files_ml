import http.server
import socketserver
import json, os, sys
import threading

# Array of strings to serve
items_to_serve = []
for line in sys.stdin.readlines():
    if line.startswith("#"):
        continue
    idx, filepath = json.loads(line.strip())
    items_to_serve.append(filepath)

# Global variables
current_index = 0
lock = threading.Lock()  # For thread safety

def get_next_item():
    """Get the next item from the array and increment index"""
    global current_index
    
    with lock:
        looped = 0
        while True:
            if current_index >= len(items_to_serve):
                current_index = 0
                looped += 1

            if looped > 1:
                return None

            item = items_to_serve[current_index]
            current_index += 1

            # Check if this file exists
            if os.path.exists(item.replace('.pdf', '.txt')):
                print(f"Skipping {item} as the corresponding .txt file exists.")
                continue
            print(f"Processing {item} {current_index} of {len(items_to_serve)}")
            return item

def handle_request(handler):
    """Handle HTTP requests"""
    # Get the next item
    item = get_next_item()
    if item is None:
        # No more items to serve
        handler.send_response(404)
        handler.end_headers()
        return
    
    # Prepare JSON response
    response = json.dumps({"filename": item})
    
    # Send response headers
    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Content-Length', len(response))
    handler.end_headers()
    
    # Send response content
    handler.wfile.write(response.encode('utf-8'))
    
    # Log the response (optional)
    print(f"Served item: {item}")

class SimpleRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        handle_request(self)

def run_server(port=8000):
    """Run HTTP server that returns items from the provided array"""
    # Create and start the server
    httpd = socketserver.ThreadingTCPServer(("", port), SimpleRequestHandler)
    
    print(f"Server started at http://localhost:{port}")
    print(f"Loaded {len(items_to_serve)} items")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == "__main__":
    # Run the server
    run_server(port=8124)
