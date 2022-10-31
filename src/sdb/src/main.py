import tcp_connection as tcp
import socket

def main():
    host = "127.0.0.1"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, 56428))
        tcp_connection = tcp.TcpConnection(s)
        tcp_connection.connect()
    print("hey there")

if __name__=="__main__":
    main()