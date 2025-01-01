# Socket, TLS
`cleartext-socket.x` implement a bare-bones web client. The socket created was a cleartext socket, everything that’s transmitted between the client and the server is observable, in plaintext, to every host in between. 

`encrypted-socket` implement a protection of the transmission from eavesdroppers, where an SSL context being established to secure the line, prior to sending the GET command.

### How to run

```sh
go run cleartext-socket.go

# or
python3 cleartext-socket.py
```

### example input

```sh
http://api.sampleapis.com/coffee/hot
```