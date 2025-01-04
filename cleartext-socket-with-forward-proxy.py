import socket
import base64

def create_socket(host, port=80):
    """
    Create a socket and connect to the given host and port.
    """
    try:
        server_ip = socket.gethostbyname(host)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))
        print(f"Connected to {host} ({server_ip}) on port {port}")
        return client_socket
    except socket.gaierror:
        print(f"Error: Unable to resolve host {host}")
        return None
    except Exception as e:
        print(f"Error creating socket: {e}")
        return None

def send_http_request(sock, host, path, proxy_host=None, proxy_port=None, proxy_user=None, proxy_password=None):
    """
    Send an HTTP GET request, optionally through a proxy.
    """
    if proxy_host:
        # Construct the HTTP GET request with full URL for proxies
        request = f"GET http://{host}{path} HTTP/1.1\r\n"
        request += f"Host: {host}\r\n"
        if proxy_user and proxy_password:
            # Add Proxy-Authorization header if credentials are provided
            credentials = f"{proxy_user}:{proxy_password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            request += f"Proxy-Authorization: Basic {encoded_credentials}\r\n"
        request += "Connection: close\r\n\r\n"
    else:
        # Construct the HTTP GET request with just the path for direct connections
        request = f"GET {path} HTTP/1.1\r\n"
        request += f"Host: {host}\r\n"
        request += "Connection: close\r\n\r\n"

    try:
        sock.sendall(request.encode())
        print(f"HTTP GET request sent to {proxy_host or host}{path}")
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
    # User input for URL and proxy settings
    url = input("Enter the URL (e.g., http://api.sampleapis.com/coffee/hot): ")
    proxy = input("Enter proxy details (host:port) or leave blank for no proxy: ")
    proxy_user = None
    proxy_password = None

    if proxy:
        if proxy.startswith("http://"):
            proxy = proxy[len("http://"):]  # Remove the "http://" prefix
        if ":" in proxy:
            proxy_host, proxy_port = proxy.split(":", 1)
            proxy_port = int(proxy_port)
        else:
            proxy_host = proxy
            proxy_port = 80
        proxy_user = input("Enter proxy username (leave blank if none): ")
        proxy_password = input("Enter proxy password (leave blank if none): ")
    else:
        proxy_host = proxy_port = None

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

    # Create a socket
    connection_host = proxy_host if proxy_host else host
    connection_port = proxy_port if proxy_host else 80
    sock = create_socket(connection_host, connection_port)
    if not sock:
        return

    # Send HTTP GET request
    send_http_request(sock, host, path, proxy_host, proxy_port, proxy_user, proxy_password)

    # Receive and display the response
    receive_response(sock)

    # Close the socket
    sock.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
