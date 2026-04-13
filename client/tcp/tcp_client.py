import json
import socket
from typing import Any

import cv2

from utils.protocol import send_message, recv_message


class TcpClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 5001, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

    def close(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None

    def send_frame(self, frame) -> dict[str, Any]:
        """
        Кодирует кадр в JPEG, отправляет на сервер и получает JSON-ответ.
        """
        if self.sock is None:
            raise RuntimeError("Socket is not connected")

        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            raise RuntimeError("Failed to encode frame to JPEG")

        payload = buffer.tobytes()
        send_message(self.sock, "FRAME", payload)

        msg_type, response_payload = recv_message(self.sock)

        if msg_type == "RESULT":
            return json.loads(response_payload.decode("utf-8"))
        elif msg_type == "ERROR":
            raise RuntimeError(response_payload.decode("utf-8"))
        else:
            raise RuntimeError(f"Unexpected message type: {msg_type}")
