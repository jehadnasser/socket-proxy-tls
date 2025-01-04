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

    brew install privoxy
    brew services start privoxy

    # test it
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
