package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"os"
	"strings"
	"sync/atomic"

	"github.com/antonmedv/expr"
	"github.com/pkg/errors"
)

const (
	Flag            = "evlz{my_ch4ll3ng3_my_rul3s}ctf"
	DefaultClientID = "0000"

	ShowVariables = "1"
	ApplyRule     = "2"
	HelpMenu      = "3"

	InvalidOption  = "Invalid option selected."
	WelcomeMessage = `Welcome to finance ministry.

1. Show variables
2. Apply rule
3. Help

Select: `

	HelpMessage = `
Help
----

The finance ministry has developed this employee knowledge transfer application.
The purpose of this application is to teach the wonders of our rule programming system.

- In the menu, press 1 to get a list of all variables you can access,
- In th menu press 2 to create a rule and see its result.

Rules follow the language described at: https://github.com/antonmedv/expr/blob/master/docs/Language-Definition.md
Results of your rules are returned as either True or False after evaluation.

Ex. If the list of variables contains the variable: example_value
then you can verify if example_value is greater than 10 or not.

Rule: example_value > 10
Result: True

`

	VariableMessage = `Variables available:

- flag - str [A-z0-9{}_]
- min - int
- max - int
- example - string [A-z0-9{}_.]
- test - string [A-z0-9{}_.]

`
)

var (
	// DefaultKey is the key for AES Handler.
	DefaultKey = []byte("HAHA_KEY_GO_BRRR")

	// TotalUsers is the total number of connections to the server.
	TotalUsers int64 = 0
)

/*
	TCP Listener and Helpers
*/

// WriteMessageToConn writes a message to the connection via its writer.
func WriteMessageToConn(writer *bufio.Writer, msg string) error {
	_, err := writer.Write([]byte(msg))
	if err != nil {
		return err
	}
	writer.Flush()

	return nil
}

// TCPListener initializes TCP server.
func TCPListener(host string) {
	listener, err := net.Listen("tcp4", host)
	fmt.Println("Started listening at " + host)

	if err != nil {
		fmt.Println(err)
		return
	}
	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println(err)
			return
		}

		fmt.Printf("[%s] Got new connection\n", conn.RemoteAddr().String())
		go HandleTCP(conn)
	}
}

// HandleTCP handles any incoming TCP connections.
func HandleTCP(conn net.Conn) error {
	defer func() {
		remoteAddr := conn.RemoteAddr().String()
		conn.Close()
		conn = nil

		fmt.Printf("[%s] Connection closed\n", remoteAddr)
		atomic.AddInt64(&TotalUsers, -1)
	}()
	atomic.AddInt64(&TotalUsers, 1)

	var err error

	reader := bufio.NewReader(conn)

	writer := bufio.NewWriter(conn)

	for {
		WriteMessageToConn(writer, WelcomeMessage)

		var msg []byte = make([]byte, 4096)
		var n int

		n, err = reader.Read(msg)
		if err != nil {
			if err == io.EOF {
				break
			}
		}

		err := HandleMessage(msg[:n], reader, writer, conn.RemoteAddr().String())
		if err != nil {
			fmt.Printf("[%s] Error parsing message\n", conn.RemoteAddr().String())
			WriteMessageToConn(writer, err.Error())
			break
		}
	}

	return nil

}

/*
	Menu Handlers.
*/

// HandleMessage is the root message handler,
func HandleMessage(msg []byte, reader *bufio.Reader, writer *bufio.Writer, remoteAddr string) error {
	msgStr := string(msg[:1])

	fmt.Printf("[%s] Got message request: %s\n", remoteAddr, msgStr)

	switch msgStr {
	case ShowVariables:
		return WriteMessageToConn(writer, VariableMessage)
	case ApplyRule:
		return HandleApplyRule(reader, writer, remoteAddr)
		// return WriteMessageToConn(writer, HelpMessage)
	case HelpMenu:
		return WriteMessageToConn(writer, HelpMessage)
	default:
		return errors.New(InvalidOption)
	}
}

// Handle rule application
func HandleApplyRule(reader *bufio.Reader, writer *bufio.Writer, remoteAddr string) error {
	defer func(writer *bufio.Writer, remoteAddr string) {
		if r := recover(); r != nil {
			WriteMessageToConn(writer, "Error Occured\n")
			fmt.Printf("[%s] Recovered in HandleApplyRule %v\n", remoteAddr, r)
		}
	}(writer, remoteAddr)

	env := map[string]interface{}{
		"flag":    Flag,
		"min":     10,
		"max":     100,
		"test":    "This is a test variable",
		"example": "This is an example variable",
	}

	var msg []byte = make([]byte, 4096)

	WriteMessageToConn(writer, "Rule: ")
	n, err := reader.Read(msg)
	if err != nil {
		if err == io.EOF {
			return errors.New("Connection broke.")
		}
	}
	code := strings.TrimSuffix(string(msg[:n]), "\n")

	program, err := expr.Compile(code, expr.Env(env))
	if err != nil {
		return errors.Wrap(err, "invalid rule")
	}

	output, err := expr.Run(program, env)
	if err != nil {
		return errors.Wrap(err, "failed to run rule")
	}

	outMsg := ""
	if output.(bool) {
		outMsg = "True"
	} else {
		outMsg = "False"
	}
	fmt.Printf("[%s] Rule output: (%s) = %v (%s)\n", remoteAddr, code, output, outMsg)

	return WriteMessageToConn(writer, fmt.Sprintf("Output: %s\n", outMsg))
}

func main() {
	var host string = ""
	if len(os.Args) > 1 {
		if os.Args[1] == "-h" {
			fmt.Println("Usage: ./server BIND")
			os.Exit(1)
		}
		host = os.Args[1]
	}

	if host == "" {
		host = ":1337"
	}

	TCPListener(host)
}
