package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"strconv"
	"strings"
)

func main() {
	// Get URL from user
	fmt.Print("Enter the URL (e.g., http://api.sampleapis.com/coffee/hot): ")
	var url string
	fmt.Scanln(&url)

	// Parse the URL
	host, path, err := parseURL(url)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Connect to the server
	conn, err := net.Dial("tcp", host+":80")
	if err != nil {
		fmt.Println("Error connecting to server:", err)
		return
	}
	defer conn.Close()
	fmt.Printf("Connected to %s\n", host)

	// Send HTTP GET request
	sendHTTPRequest(conn, host, path)

	// Receive and display the response
	receiveResponse(conn)
}

func parseURL(url string) (host, path string, err error) {
	if !strings.HasPrefix(url, "http://") {
		return "", "", fmt.Errorf("only http:// URLs are supported")
	}
	url = strings.TrimPrefix(url, "http://")
	slashIndex := strings.Index(url, "/")
	if slashIndex == -1 {
		host = url
		path = "/"
	} else {
		host = url[:slashIndex]
		path = url[slashIndex:]
	}
	return host, path, nil
}

func sendHTTPRequest(conn net.Conn, host, path string) {
	// Construct the HTTP GET request
	request := fmt.Sprintf(
		"GET %s HTTP/1.1\r\n"+
			"Host: %s\r\n"+
			"User-Agent: Go-Socket-Client/1.0\r\n"+
			"Connection: close\r\n\r\n",
		path, host,
	)

	// Send the request
	_, err := conn.Write([]byte(request))
	if err != nil {
		fmt.Println("Error sending request:", err)
	}
	fmt.Printf("HTTP GET request sent to %s%s\n", host, path)
}

func receiveResponse(conn net.Conn) {
	reader := bufio.NewReader(conn)

	// Read the headers
	headers := make(map[string]string)
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading headers:", err)
			return
		}
		line = strings.TrimSpace(line)

		// Break when the headers are fully read (empty line)
		if line == "" {
			break
		}

		// Parse header key-value pairs
		parts := strings.SplitN(line, ": ", 2)
		if len(parts) == 2 {
			headers[parts[0]] = parts[1]
		} else {
			fmt.Println(line) // Status line (e.g., HTTP/1.1 200 OK)
		}
	}

	// Check for Content-Length header
	contentLength := 0
	if lenStr, ok := headers["Content-Length"]; ok {
		contentLength, _ = strconv.Atoi(lenStr)
	}

	fmt.Println("\n--- Response Body ---")
	if contentLength > 0 {
		// Read the specified number of bytes from the body
		body := make([]byte, contentLength)
		_, err := io.ReadFull(reader, body)
		if err != nil {
			fmt.Println("Error reading body:", err)
			return
		}
		fmt.Println(string(body))
	} else {
		// Fallback to reading until the connection is closed
		body, err := io.ReadAll(reader)
		if err != nil {
			fmt.Println("Error reading body:", err)
			return
		}
		fmt.Println(string(body))
	}
}
