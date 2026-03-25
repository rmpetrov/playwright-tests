from __future__ import annotations

import base64
import hashlib
import hmac
import html
import os
import time
from http import HTTPStatus
from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
SESSION_COOKIE_NAME = "local_app_session"
REMEMBER_ME_MAX_AGE = 7 * 24 * 60 * 60


def _cookie_secret() -> bytes:
    return os.getenv("LOCAL_APP_SECRET", "local-demo-secret").encode("utf-8")


def _expected_credentials() -> tuple[str, str]:
    username = os.getenv("PW_USERNAME", "test_user")
    password = os.getenv("PW_PASSWORD", "test_password")
    return username, password


def _encode_payload(value: str) -> str:
    return base64.urlsafe_b64encode(value.encode("utf-8")).decode("utf-8").rstrip("=")


def _decode_payload(value: str) -> str | None:
    padding = "=" * (-len(value) % 4)
    try:
        return base64.urlsafe_b64decode(f"{value}{padding}").decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None


def _create_session_token(username: str) -> str:
    issued_at = str(int(time.time()))
    payload = _encode_payload(f"{username}:{issued_at}")
    return f"{payload}.{_sign_payload(payload)}"


def _sign_payload(payload: str) -> str:
    return hmac.new(
        _cookie_secret(),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _get_authenticated_username(cookie_header: str | None) -> str | None:
    if not cookie_header:
        return None

    cookies = SimpleCookie()
    try:
        cookies.load(cookie_header)
    except (CookieError, KeyError, ValueError):
        return None

    morsel = cookies.get(SESSION_COOKIE_NAME)
    if morsel is None:
        return None

    try:
        payload, provided_signature = morsel.value.split(".", 1)
    except ValueError:
        return None

    expected_signature = _sign_payload(payload)
    if not hmac.compare_digest(provided_signature, expected_signature):
        return None

    decoded_payload = _decode_payload(payload)
    if not decoded_payload:
        return None

    username, _, _issued_at = decoded_payload.partition(":")
    return username or None


def _build_session_cookie(token: str, remember: bool) -> str:
    parts = [
        f"{SESSION_COOKIE_NAME}={token}",
        "Path=/",
        "HttpOnly",
        "SameSite=Lax",
    ]
    if remember:
        parts.append(f"Max-Age={REMEMBER_ME_MAX_AGE}")
    return "; ".join(parts)


def _clear_session_cookie() -> str:
    return f"{SESSION_COOKIE_NAME}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0"


def _login_page_html(
    error_message: str = "",
    username: str = "",
    remember_me_checked: bool = False,
) -> bytes:
    alert_html = ""
    if error_message:
        alert_html = (
            '<div id="alert" role="alert" style="color:#b00020; margin-bottom:12px;">'
            f"{html.escape(error_message)}"
            "</div>"
        )

    remember_me_attr = " checked" if remember_me_checked else ""
    escaped_username = html.escape(username)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Login</title>
</head>
<body>
  <main id="login-page" data-testid="login-page">
    <h1 id="login-title">Login Form</h1>
    {alert_html}
    <form id="login-form" method="post" action="/login">
      <div>
        <label for="username">Username</label>
        <input id="username" name="username" type="text" placeholder="Enter your username" value="{escaped_username}" />
      </div>
      <div>
        <label for="password">Password</label>
        <input id="password" name="password" type="password" placeholder="Enter your password" />
      </div>
      <div>
        <input id="remember-me" name="remember-me" type="checkbox"{remember_me_attr} />
        <label for="remember-me">Remember Me</label>
      </div>
      <button id="log-in" type="submit">Log In</button>
    </form>
  </main>
</body>
</html>
""".encode()


def _app_page_html(username: str) -> bytes:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dashboard</title>
</head>
<body>
  <main id="dashboard-page" data-testid="dashboard-page">
    <section>
      <h1 id="dashboard-title">Financial Overview</h1>
      <p id="session-banner">Signed in as {html.escape(username)}</p>
      <form id="logout-form" method="post" action="/logout">
        <button id="log-out" type="submit">Log Out</button>
      </form>
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
""".encode()


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        username = _get_authenticated_username(self.headers.get("Cookie"))

        if path == "/":
            if username:
                self._redirect("/app.html")
                return
            self._send_html(_login_page_html())
            return

        if path == "/app.html":
            if not username:
                self._redirect("/")
                return
            self._send_html(_app_page_html(username))
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
        if path == "/login":
            self._handle_login()
            return

        if path == "/logout":
            self._redirect("/", cookie=_clear_session_cookie())
            return

        self._send_text("not found", status=HTTPStatus.NOT_FOUND)

    def _handle_login(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(body, keep_blank_values=True)

        username = form.get("username", [""])[0].strip()
        password = form.get("password", [""])[0].strip()
        remember_requested = "remember-me" in form
        expected_username, expected_password = _expected_credentials()

        if not username:
            self._send_login_error(
                "Username is required.",
                username=username,
                remember_me_checked=remember_requested,
            )
            return

        if not password:
            self._send_login_error(
                "Password is required.",
                username=username,
                remember_me_checked=remember_requested,
            )
            return

        if username != expected_username or password != expected_password:
            self._send_login_error(
                "Invalid username or password.",
                username=username,
                remember_me_checked=remember_requested,
            )
            return

        token = _create_session_token(username)
        self._redirect(
            "/app.html",
            cookie=_build_session_cookie(token, remember=remember_requested),
        )

    def _send_login_error(
        self,
        message: str,
        username: str,
        remember_me_checked: bool,
    ) -> None:
        self._send_html(
            _login_page_html(
                message,
                username=username,
                remember_me_checked=remember_me_checked,
            )
        )

    def _send_html(self, body: bytes, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, location: str, cookie: str | None = None) -> None:
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", location)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()

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
