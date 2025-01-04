# Socket, TLS
`cleartext-socket.x` implement a bare-bones web client. The socket created was a cleartext socket, everything that’s transmitted between the client and the server is observable, in plaintext, to every host in between. 

`cleartext-socket-with-forward-proxy.x` the client funnel its requests through the proxy (all its requests to the proxy server instead of directly contacting the target server. The proxy then forwards these requests to their intended destinations and relays the responses back to the client.). The client establishes a socket connection with the proxy server ﬁrst, and issues a GET request to it. After the proxy receives the GET request, the proxy examines the request to determine the host name, resolves the IP address, connects to that IP address on behalf of the client, re-issues the GET request, and forwards the response back to the client.

`encrypted-socket.x` implement a protection of the transmission from eavesdroppers, where an SSL context being established to secure the line, prior to sending the GET command.


### How to run
```sh
go run cleartext-socket.go

# or
python3 cleartext-socket.py
```

## example input

```sh
http://api.sampleapis.com/coffee/hot
```

## cleartext-socket-with-forward-proxy
- Install a local forward-proxy `privoxy`
```sh
# on MacOS
brew services list

brew install privoxy
brew services start privoxy
# it's configs
code /opt/homebrew/etc/privoxy/config
brew services restart privoxy


# test it
lsof -i :8118
curl -v -x http://127.0.0.1:8118 http://example.com

# when you done
brew services stop privoxy
brew uninstall privoxy
```

- How to run it
```sh
python3 cleartext-socket-with-forward-proxy.py 
Enter the URL (e.g., http://api.sampleapis.com/coffee/hot): http://api.sampleapis.com/coffee/hot
Enter proxy details (host:port) or leave blank for no proxy: http://127.0.0.1:8118
Enter proxy username (leave blank if none): 
Enter proxy password (leave blank if none):
# ...
```

## Test Authentication
To add authentication to the local proxy `privoxy`, we will use nginx(reverse proxy) in front of the `privoxy`. Nginx acts as a reverse proxy, and it handles the authentication, while Privoxy sits behind Nginx and performs the actual proxying and filtering tasks.
```sh
brew install nginx
brew services start nginx
sudo lsof -i :8080
curl http://127.0.0.1:8080 

# check if htpasswd is not installed
htpasswd -h
brew install httpd-tools


brew services list

# check location of nginx config file, e.g /opt/homebrew/etc/nginx/nginx.conf
nginx -t
htpasswd -c /opt/homebrew/etc/nginx/.htpasswd jnasser
ls /opt/homebrew/etc/nginx/.htpasswd
cp /opt/homebrew/etc/nginx/nginx.conf /opt/homebrew/etc/nginx/nginx.conf.bckup
nano /opt/homebrew/etc/nginx/nginx.conf
nginx -t -c /opt/homebrew/etc/nginx/nginx.conf


```

Set `accept-intercepted-requests 1` in `code /opt/homebrew/etc/privoxy/config `

add/modify the server listens on 8080 in the nginx config to be like this
```json
http {
    include       mime.types;
    default_type  application/octet-stream;

    server {
        listen 8080;

        # Basic Authentication
        auth_basic "Protected Proxy";
        auth_basic_user_file /opt/homebrew/etc/nginx/.htpasswd;

        # Proxy to Privoxy
        location / {
            proxy_pass http://127.0.0.1:8118;  # Ensure Privoxy is running
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            # Ensure the Proxy-Connection header is removed
            proxy_set_header Proxy "";  
        }
    }
}
```

```sh
# Ensure there are no syntax errors
nginx -t -c /opt/homebrew/etc/nginx/nginx.conf
sudo nginx -s reload

# test to curl Privoxy directly, should work without authentication (on port 8118)
curl -v -x http://127.0.0.1:8118 http://example.com

# test to curl Nginx, should work with authentication (on port 8080) 
curl -v -x http://127.0.0.1:8080 http://example.com

curl -x http://myuser:password@127.0.0.1:8080 http://api.sampleapis.com/coffee/hot
```

Now using the socket with forward proxy in this repo:
```sh
python3 cleartext-socket-with-forward-proxy.py 
Enter the URL (e.g., http://api.sampleapis.com/coffee/hot): http://api.sampleapis.com/coffee/hot
Enter proxy details (host:port) or leave blank for no proxy: http://127.0.0.1:8080
Enter proxy username (leave blank if none): myuser
Enter proxy password (leave blank if none): password
Connected to 127.0.0.1 (127.0.0.1) on port 8080
HTTP GET request sent to 127.0.0.1/coffee/hot
Server response:
HTTP/1.1 200 ok
Server: nginx/1.27.3
Date: Sat, 04 Jan 2025 13:50:31 GMT
Content-Type: text/html
Content-Length: 179
Connection: close
WWW-Authenticate: Basic realm="Protected Proxy"
#....
```