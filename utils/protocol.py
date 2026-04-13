import struct
from typing import Tuple


def send_message(sock, message_type: str, payload: bytes) -> None:
    """
    Формат сообщения:
    [4 байта длина message_type][message_type bytes][4 байта длина payload][payload bytes]
    """
    message_type_bytes = message_type.encode("utf-8")
    sock.sendall(struct.pack("!I", len(message_type_bytes)))
    sock.sendall(message_type_bytes)
    sock.sendall(struct.pack("!I", len(payload)))
    sock.sendall(payload)


def recv_exact(sock, n: int) -> bytes:
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed while receiving data")
        data += chunk
    return data


def recv_message(sock) -> Tuple[str, bytes]:
    type_len_bytes = recv_exact(sock, 4)
    type_len = struct.unpack("!I", type_len_bytes)[0]

    message_type = recv_exact(sock, type_len).decode("utf-8")

    payload_len_bytes = recv_exact(sock, 4)
    payload_len = struct.unpack("!I", payload_len_bytes)[0]

    payload = recv_exact(sock, payload_len)
    return message_type, payload
