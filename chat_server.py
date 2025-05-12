import socket
import sys
import os

class ChatServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        
        server_address = '/tmp/socket_file'
        
        try:
            os.unlink(server_address)
        except FileNotFoundError:
            pass
        
        self.sock.bind(server_address)
        self.sock.listen(2)
        
    def run(self):
        clients = []
        
        while True:
            conn, addr = self.sock.accept()
            
            if len(clients) < 2:
                clients.append(conn)
            else:
                conn.sendall(b"Server full! Sorry!")
                conn.close()
            
            try:
                print(f"Connection from {addr}")
                
                while True:
                    data = conn.recv(256)
                    data_str = data.decode('utf-8')
                    
                    if data and data == 'exit':
                        sys.exit(1)
                    elif data:
                        print(f"Received {data_str}")
                        
                        response = "Processing " + data_str
                        conn.sendall(response.encode())
                    else:
                        print(f"No data from {addr}")
                        break
                    
                    
            finally:
                print("Closing current connection")
                conn.close()
                break
            
def main():
    server = ChatServer()
    server.run()
    
if __name__ == "__main__":
    main()
                