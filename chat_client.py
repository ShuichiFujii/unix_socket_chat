import socket
import sys

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        
        server_address = '/tmp/socket_file'
        print(f"Connecting to {server_address}")
        
        try:
            self.sock.connect(server_address)
        except Exception as err:
            print(f"Error: {err}")
            sys.exit(1)
            
    def run(self):
        try:
            message = input("Please enter a new message: ")
            self.sock.sendall(message.encode())
            
            if message == "exit":
                sys.exit(1)
            
            self.sock.settimeout(2)
            
            try:
                while True:
                    data = str(self.sock.recv(32))
                    
                    if data:
                        print(f"Server response: {data}")
                    else:
                        break
                    
            except TimeoutError:
                print("Socket timeout, ending listening for server messages")
                
        finally:
            print("Closing socket")
            self.sock.close()
            

def main():
    client = ChatClient()
    client.run()
    
if __name__ == "__main__":
    main()