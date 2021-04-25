import socket

from api import app
from api.v1.utils import HOST

if __name__ == "__main__":
    app.run(host=socket.gethostbyname(HOST), debug=True)
