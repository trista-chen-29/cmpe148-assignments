#!/usr/bin/env python3
"""TCP client for the Task 4 string-processing server."""

from __future__ import annotations

import socket

HOST = "127.0.0.1"
PORT = 5555
BUFFER_SIZE = 4096


def main() -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            try:
                sock.connect((HOST, PORT))
            except ConnectionRefusedError:
                print(f"Could not connect to {HOST}:{PORT}. Is the server running?")
                return
            except socket.timeout:
                print(f"Timed out connecting to {HOST}:{PORT}.")
                return
            except OSError as exc:
                print(f"Connection error: {exc}")
                return

            sock.settimeout(None)
            print(f"Connected to TCP server at {HOST}:{PORT}")
            print("Commands: title: <text> | swap: <text> | count | history | bye")
            print("Press Ctrl+C to quit.\n")

            while True:
                try:
                    message = input("You: ").strip()
                except EOFError:
                    print("\nNo more input; closing.")
                    break
                except KeyboardInterrupt:
                    print("\nInterrupted; closing.")
                    break

                if not message:
                    print("Please enter a message.")
                    continue

                try:
                    sock.sendall((message + "\n").encode("utf-8"))
                except BrokenPipeError:
                    print("Connection closed by server.")
                    break
                except OSError as exc:
                    print(f"Send failed: {exc}")
                    break

                try:
                    data = sock.recv(BUFFER_SIZE)
                except ConnectionResetError:
                    print("Connection reset by server.")
                    break
                except OSError as exc:
                    print(f"Receive failed: {exc}")
                    break

                if not data:
                    print("Server closed the connection.")
                    break

                try:
                    response = data.decode("utf-8").rstrip("\n")
                except UnicodeDecodeError:
                    print("Server: (could not decode response)")
                    continue

                print(f"Server: {response}")

                if message == "bye":
                    break
    except KeyboardInterrupt:
        print("\nClient exiting.")
    except Exception as exc:  # noqa: BLE001 - report unexpected client errors
        print(f"Unexpected client error: {exc}")


if __name__ == "__main__":
    main()
