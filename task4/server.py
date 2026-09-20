#!/usr/bin/env python3
"""TCP string-processing server for Task 4.

Each connected client is handled independently so count/history stay
per-connection. Commands:

  title: <text>  -> title-case the text
  swap: <text>   -> swap letter case
  count          -> number of messages from this client
  history        -> past messages from this client
  bye            -> close this client's connection
  anything else  -> "try again"
"""

from __future__ import annotations

import socket
import threading

HOST = "127.0.0.1"
PORT = 5555
BUFFER_SIZE = 4096


def process_message(message: str, history: list[str]) -> tuple[str, bool]:
    """Return (response, should_close)."""
    if message == "bye":
        return "Goodbye.", True

    if message == "count":
        return str(len(history)), False

    if message == "history":
        if not history:
            return "(no messages yet)", False
        return "\n".join(history), False

    if message.startswith("title:"):
        text = message[len("title:") :].lstrip()
        return text.title(), False

    if message.startswith("swap:"):
        text = message[len("swap:") :].lstrip()
        return text.swapcase(), False

    return "try again", False


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    history: list[str] = []
    print(f"[+] Connected: {addr}")

    try:
        with conn:
            while True:
                try:
                    data = conn.recv(BUFFER_SIZE)
                except ConnectionResetError:
                    print(f"[-] Connection reset by {addr}")
                    break
                except OSError as exc:
                    print(f"[-] Socket error from {addr}: {exc}")
                    break

                if not data:
                    print(f"[-] Client {addr} disconnected")
                    break

                try:
                    message = data.decode("utf-8").strip()
                except UnicodeDecodeError:
                    conn.sendall(b"try again\n")
                    continue

                if not message:
                    conn.sendall(b"try again\n")
                    continue

                history.append(message)
                response, should_close = process_message(message, history)

                try:
                    conn.sendall((response + "\n").encode("utf-8"))
                except OSError as exc:
                    print(f"[-] Failed to send to {addr}: {exc}")
                    break

                if should_close:
                    print(f"[-] Client {addr} said bye; closing")
                    break
    except Exception as exc:  # noqa: BLE001 - log unexpected errors, keep server up
        print(f"[-] Unexpected error handling {addr}: {exc}")
    finally:
        print(f"[-] Closed: {addr}")


def main() -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen()
            print(f"TCP server listening on {HOST}:{PORT}")
            print("Press Ctrl+C to stop.")

            while True:
                try:
                    conn, addr = server.accept()
                except OSError as exc:
                    print(f"Accept failed: {exc}")
                    continue

                thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    except OSError as exc:
        print(f"Could not start server: {exc}")


if __name__ == "__main__":
    main()
