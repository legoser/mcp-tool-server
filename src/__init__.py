"""MCP Tools Server package."""

import sys
from pathlib import Path

# Ensure parent directory is in sys.path for both relative and absolute imports
_package_root = Path(__file__).parent
_project_root = _package_root.parent

if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
