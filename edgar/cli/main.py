"""Command-line interface for EDGAR query tool."""

import argparse
import sys

from ..core import EdgarQueryEngine


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="EDGAR Query Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Load data command
    subparsers.add_parser("load-data", help="Load EDGAR filing data")

    # Query command
    query_parser = subparsers.add_parser("query", help="Query EDGAR filings")
    query_parser.add_argument("query", help="Natural language query")

    # API command
    api_parser = subparsers.add_parser("api", help="Start API server")
    api_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    api_parser.add_argument("--port", default=8000, help="Port to bind to")

    # Web command
    web_parser = subparsers.add_parser("web", help="Start web server")
    web_parser.add_argument("--port", default=3000, help="Port to bind to")

    args = parser.parse_args()

    if not hasattr(args, "command") or args.command is None:
        parser.print_help()
        return

    if args.command == "load-data":
        engine = EdgarQueryEngine()
        engine.initialize()
        if engine.load_data():
            print("Data loaded successfully")
        else:
            print("Failed to load data")
            sys.exit(1)

    elif args.command == "query":
        engine = EdgarQueryEngine()
        engine.initialize()
        result, error, _ = engine.query(args.query)
        if error:
            print(f"Error: {error}")
            sys.exit(1)
        if result:
            print(result["markdown_response"])

    elif args.command == "api":
        try:
            # Dynamic imports to avoid top-level dependencies
            uvicorn_module = __import__("uvicorn")
            from ..api.server import app

            port = int(args.port)
            print(f"Starting API server on {args.host}:{port}")
            uvicorn_module.run(app, host=args.host, port=port)
        except ImportError:
            print("Error: uvicorn not installed. Install with: uv add uvicorn")
            sys.exit(1)

    elif args.command == "web":
        try:
            import os
            from http.server import HTTPServer, SimpleHTTPRequestHandler
            from pathlib import Path

            # Change to the web static directory
            static_dir = Path(__file__).parent.parent / "web" / "static"
            if static_dir.exists():
                os.chdir(static_dir)

            port = int(args.port)
            print(f"Starting web server on http://localhost:{port}")
            print("Press Ctrl+C to quit")

            httpd = HTTPServer(("", port), SimpleHTTPRequestHandler)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")
                httpd.server_close()
                sys.exit(0)
        except Exception as e:
            print(f"Error starting web server: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
