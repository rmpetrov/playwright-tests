from __future__ import annotations

import os

from local_app.server import DEFAULT_HOST, DEFAULT_PORT, run


def main() -> None:
    host = os.getenv("LOCAL_APP_HOST", DEFAULT_HOST)
    port = int(os.getenv("LOCAL_APP_PORT", str(DEFAULT_PORT)))
    run(host=host, port=port)


if __name__ == "__main__":
    main()
