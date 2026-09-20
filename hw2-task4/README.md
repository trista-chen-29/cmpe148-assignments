# HW2 Task 4 — TCP Client-Server Application

## Language and version

- Language: Python 3
- Tested with: Python 3.14.2 (any Python 3.10+ should work)
- Standard library only (`socket`, `threading`) — no extra packages

## Transport protocol

**TCP** (`SOCK_STREAM`).

TCP is used because this assignment needs a persistent, ordered connection per client. `count` and `history` are tracked for *this client during the current connection*, and `bye` closes that connection. TCP provides a reliable byte stream and a real connection so those per-session features work correctly. UDP is connectionless and does not guarantee delivery or message order, which would make a per-connection history harder and less reliable.

## How to run

Open two terminals. From this `hw2-task4` directory:

**Terminal 1 — start the server first**

```bash
python3 server.py
```

You should see:

```text
TCP server listening on 127.0.0.1:5555
```

**Terminal 2 — start the client**

```bash
python3 client.py
```

Type a command and press Enter. Example session:

```text
You: title: this is a message
Server: This Is A Message
You: swap: CMPE is Awesome
Server: cmpe IS aWESOME
You: hello
Server: try again
You: count
Server: 4
You: history
Server: title: this is a message
swap: CMPE is Awesome
hello
count
history
You: bye
Server: Goodbye.
```

Stop the server with Ctrl+C.

## Commands

| Client input | Server response |
|---|---|
| `title: <string>` | Title-cased string (first letter of each word capitalized) |
| `swap: <string>` | Case-swapped string |
| `count` | Number of messages received from this client in the current connection |
| `history` | Past messages from this client in the current connection |
| `bye` | `Goodbye.` then the server closes the connection |
| anything else | `try again` |

`count` and `history` include every message received on that connection (including `count`, `history`, and `bye`).

## Evidence screenshots

- `screenshots/lp_evidence.png` — `title:`, `swap:`, and an invalid input that returns `try again`
- `screenshots/hp_evidence.png` — `count`, `history`, and `bye` in addition to the LP commands
