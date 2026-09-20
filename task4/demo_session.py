#!/usr/bin/env python3
"""Non-interactive client used to capture a representative session."""

from __future__ import annotations

import socket
import sys

HOST = "127.0.0.1"
PORT = 5555


def run(messages: list[str]) -> str:
    lines: list[str] = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        lines.append(f"Connected to TCP server at {HOST}:{PORT}")
        lines.append("Commands: title: <text> | swap: <text> | count | history | bye")
        lines.append("")
        for message in messages:
            lines.append(f"You: {message}")
            sock.sendall((message + "\n").encode("utf-8"))
            data = sock.recv(4096)
            if not data:
                lines.append("Server closed the connection.")
                break
            response = data.decode("utf-8").rstrip("\n")
            if "\n" in response:
                first, *rest = response.split("\n")
                lines.append(f"Server: {first}")
                lines.extend(rest)
            else:
                lines.append(f"Server: {response}")
            if message == "bye":
                break
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else "hp"
    if kind == "lp":
        messages = [
            "title: this is a message",
            "swap: CMPE is Awesome",
            "hello world",
        ]
    else:
        messages = [
            "title: this is a message",
            "swap: CMPE is Awesome",
            "hello world",
            "count",
            "history",
            "bye",
        ]
    sys.stdout.write(run(messages))
