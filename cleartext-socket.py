import socket


def create_socket(host, port=80):
    """
    Create a socket and connect to the server.
    """
    try:
        # Resolve host to IP
        server_ip = socket.gethostbyname(host)

        # Create a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((server_ip, port))
        print(f"Connected to {host} ({server_ip}) on port {port}")

        return client_socket
    except socket.gaierror:
        print(f"Error: Unable to resolve host {host}")
        return None
    except Exception as e:
        print(f"Error creating socket: {e}")
        return None


def send_http_request(sock, host, path="/"):
    """
    Send an HTTP GET request.
    """
    try:
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Connection: close\r\n\r\n"
        )
        sock.sendall(request.encode())
        print(f"HTTP request sent to {host}{path}")
    except Exception as e:
        print(f"Error sending HTTP request: {e}")


def receive_response(sock):
    """
    Receive and print the server response.
    """
    try:
        response = b""
        while True:
            data = sock.recv(1024)
            if not data:
                break
            response += data
        print("Server response:")
        print(response.decode())
    except Exception as e:
        print(f"Error receiving response: {e}")


def main():
    url = input("Enter the URL (e.g., http://api.sampleapis.com/coffee/hot): ")
    if not url.startswith("http://"):
        print("Error: Only http:// URLs are supported.")
        return

    # Parse the URL
    try:
        host, path = url[7:].split("/", 1)
        path = "/" + path
    except ValueError:
        host = url[7:]
        path = "/"

    # Create a socket and connect
    sock = create_socket(host)
    if sock is None:
        return

    # Send HTTP GET request
    send_http_request(sock, host, path)

    # Receive and display the response
    receive_response(sock)

    # Close the socket
    sock.close()
    print("Connection closed.")


if __name__ == "__main__":
    main()
