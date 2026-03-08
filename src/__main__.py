"""Entry point for running the MCP server via: python -m src"""

import sys

from .main import server_main


def main():
    """Main entry point for the MCP server."""
    try:
        server_main.run(transport="stdio")
    except KeyboardInterrupt:
        print("\nServer stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
