import cv2

from client.camera import Camera
from client.tcp.tcp_client import TcpClient


def main():
    host = "127.0.0.1"
    port = 5001

    camera = Camera(camera_index=0)
    client = TcpClient(host=host, port=port)

    try:
        client.connect()
        print(f"Connected to server {host}:{port}")

        while True:
            frame = camera.read()

            try:
                result = client.send_frame(frame)
                print("Server result:", result)
            except Exception as e:
                print("Error sending frame:", e)

            # простое окно для контроля
            cv2.imshow("Client Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        client.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
