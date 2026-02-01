#!/usr/bin/env python3
"""Generate landing page for GitHub Pages with links to test reports."""

from pathlib import Path

HTML_REPORT_DIR = Path("html-report")

INDEX_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Reports</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
        }
        h1 { color: #333; }
        ul { list-style: none; padding: 0; }
        li { margin: 15px 0; }
        a {
            display: inline-block;
            padding: 12px 24px;
            background: #0366d6;
            color: white;
            text-decoration: none;
            border-radius: 6px;
        }
        a:hover { background: #0256b9; }
    </style>
</head>
<body>
    <h1>Test Reports</h1>
    <ul>
        <li><a href="./ui/">UI HTML report</a></li>
        <li><a href="./api/">API HTML report</a></li>
    </ul>
</body>
</html>
"""


def main() -> None:
    """Generate index.html in html-report directory."""
    HTML_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    index_path = HTML_REPORT_DIR / "index.html"
    index_path.write_text(INDEX_HTML, encoding="utf-8")
    print(f"Generated {index_path}")


if __name__ == "__main__":
    main()
