import json
import socket
import threading

from server.tcp.inference import InferenceService
from utils.protocol import send_message, recv_message


class TcpServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 5001):
        self.host = host
        self.port = port
        self.server_sock = None
        self.inference_service = InferenceService()
        self.running = False

    def start(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(1)
        self.running = True

        print(f"TCP server listening on {self.host}:{self.port}")

        while self.running:
            client_sock, client_addr = self.server_sock.accept()
            print(f"Client connected: {client_addr}")

            thread = threading.Thread(
                target=self.handle_client,
                args=(client_sock, client_addr),
                daemon=True
            )
            thread.start()

    def handle_client(self, client_sock: socket.socket, client_addr):
        try:
            while True:
                msg_type, payload = recv_message(client_sock)

                if msg_type == "FRAME":
                    try:
                        result = self.inference_service.process_frame_bytes(payload)
                        result_json = json.dumps(result, ensure_ascii=False).encode("utf-8")
                        send_message(client_sock, "RESULT", result_json)
                    except Exception as e:
                        error_json = str(e).encode("utf-8")
                        send_message(client_sock, "ERROR", error_json)
                else:
                    send_message(client_sock, "ERROR", f"Unknown message type: {msg_type}".encode("utf-8"))

        except Exception as e:
            print(f"Client {client_addr} disconnected: {e}")
        finally:
            client_sock.close()


if __name__ == "__main__":
    server = TcpServer()
    server.start()
