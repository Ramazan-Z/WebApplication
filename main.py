from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

HOST_NAME = "localhost"
SERVER_PORT = 8080
# Типы контента
TYPES = {
    "html": "text/html",
    "css": "text/css",
    "svg": "image/svg+xml",
    "jpg": "image/jpg",
    "ico": "image/ico",
    "js": "application/JavaScript",
}


class MyServer(BaseHTTPRequestHandler):
    """Класс для обработки входящих запросов"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Инициализация экземпляра класса"""
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        """Метод для обработки входящих GET-запросов"""
        try:
            with open(self.path[1:], "rb") as file:
                content = file.read()
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("Not Found", "utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", self.get_content_type())
            self.end_headers()
            self.wfile.write(content)

    def get_content_type(self) -> str:
        """Метод для получения типа контента"""
        suffix = self.path.split(".")[-1]
        return TYPES.get(suffix, "text/html")


def run_server() -> None:
    """Запуск http сервера с обработчиком запросов"""
    web_server = HTTPServer((HOST_NAME, SERVER_PORT), MyServer)
    print(f"Откройте в браузере: http://{HOST_NAME}:{SERVER_PORT}/sites/home.html")
    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
    web_server.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    run_server()
