from __future__ import annotations

import html
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


def _expected_credentials() -> tuple[str, str]:
    username = os.getenv("PW_USERNAME", "test_user")
    password = os.getenv("PW_PASSWORD", "test_password")
    return username, password


def _login_page_html(error_message: str = "") -> bytes:
    alert_html = ""
    if error_message:
        alert_html = (
            '<div id="alert" role="alert" style="color:#b00020; margin-bottom:12px;">'
            f"{html.escape(error_message)}"
            "</div>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Login</title>
</head>
<body>
  <main>
    <h1>Login Form</h1>
    {alert_html}
    <form method="post" action="/login">
      <div>
        <label for="username">Username</label>
        <input id="username" name="username" type="text" placeholder="Enter your username" />
      </div>
      <div>
        <label for="password">Password</label>
        <input id="password" name="password" type="password" placeholder="Enter your password" />
      </div>
      <div>
        <input id="remember-me" name="remember-me" type="checkbox" />
        <label for="remember-me">Remember Me</label>
      </div>
      <button id="log-in" type="submit">Log In</button>
    </form>
  </main>
</body>
</html>
""".encode()


def _app_page_html() -> bytes:
    return b"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dashboard</title>
</head>
<body>
  <main>
    <section>
      <h1>Financial Overview</h1>
      <article>
        <h2>Total Balance</h2>
        <p>350,180.00 USD</p>
      </article>
      <article>
        <h2>Credit Available</h2>
        <p>17,800.00 USD</p>
      </article>
    </section>

    <section>
      <h2>Recent Transactions</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Status</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>2026-02-10</td>
            <td>Salary</td>
            <td>Completed</td>
            <td>+ 2,500.00 USD</td>
          </tr>
          <tr>
            <td>2026-02-09</td>
            <td>Groceries</td>
            <td>Completed</td>
            <td>- 120.75 USD</td>
          </tr>
          <tr>
            <td>2026-02-08</td>
            <td>Gym Membership</td>
            <td>Completed</td>
            <td>- 49.99 USD</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path

        if path == "/":
            self._send_html(_login_page_html())
            return

        if path == "/app.html":
            self._send_html(_app_page_html())
            return

        if path == "/health":
            self._send_text("ok")
            return

        if path == "/favicon.ico":
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()
            return

        self._send_text("not found", status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        if path != "/login":
            self._send_text("not found", status=HTTPStatus.NOT_FOUND)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(body, keep_blank_values=True)

        username = form.get("username", [""])[0].strip()
        password = form.get("password", [""])[0].strip()
        expected_username, expected_password = _expected_credentials()

        if not username:
            self._send_html(_login_page_html("Username is required."))
            return

        if not password:
            self._send_html(_login_page_html("Password is required."))
            return

        if username != expected_username or password != expected_password:
            self._send_html(_login_page_html("Invalid username or password."))
            return

        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", "/app.html")
        self.end_headers()

    def _send_html(self, body: bytes, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    server = ThreadingHTTPServer((host, port), _Handler)
    print(f"Local app listening on http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
