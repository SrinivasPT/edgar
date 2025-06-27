import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 3000


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def start_web_server():
    """Start the web server."""
    handler = Handler
    httpd = HTTPServer(("", PORT), handler)
    print(f"Server running at http://localhost:{PORT}")
    print("Press Ctrl+C to quit")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()
        sys.exit(0)


def main():
    """Main entry point for the web server."""
    start_web_server()


if __name__ == "__main__":
    main()
