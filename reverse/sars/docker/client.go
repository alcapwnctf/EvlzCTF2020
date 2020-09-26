package main

import (
	"bufio"
	"crypto/rand"
	"encoding/hex"
	"flag"
	"fmt"
	"io"
	"net"
	"os"
	"strings"

	Channel "github.com/arush15june/protobuf-forward-compat/pkg/proto/v1"
	"github.com/pkg/errors"
	"google.golang.org/protobuf/proto"
)

const (
	ErrorReqType      = "error"
	FnvReqType        = "fnv"
	UsersReqType      = "users"
	ListActionReqType = "list"
	DocumentReqType   = "document"
)

type RequestConfig struct {
	ReqType      string
	takeInput    bool
	inputMessage string
}

func randomHex(n int) (string, error) {
	bytes := make([]byte, n)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes), nil
}

/*
   ChannelMessage Helpers
*/

// ParseChannelMessage parses a channel message from a bytestream, returns error if parsing is invalid.
func ParseChannelMessage(msg []byte) (*Channel.ChannelMessage, error) {
	channelMessage := &Channel.ChannelMessage{}
	if err := proto.Unmarshal(msg, channelMessage); err != nil {
		return nil, err
	}

	return channelMessage, nil
}

// NewChannelMessage creates a Channel.ChannelMessage with passed arguments and returns it.
func NewChannelMessage(ReqType string, clientId string, msg string) *Channel.ChannelMessage {
	channelMsg := &Channel.ChannelMessage{
		ReqType:  ReqType,
		ClientId: clientId,
		Message:  msg,
	}

	return channelMsg
}

// MarshalChannelMessage marshals a Channel.ChannelMessage to a bytestream.
func MarshalChannelMessage(channelMsg *Channel.ChannelMessage) ([]byte, error) {
	return proto.Marshal(channelMsg)
}

var (
	// Host is the server hostname
	Host string
	// Port is the server port
	Port string

	// Configuration of requests
	ReqConfigStore map[string]RequestConfig = map[string]RequestConfig{
		FnvReqType: RequestConfig{
			ReqType:      FnvReqType,
			takeInput:    true,
			inputMessage: "Input to hash: ",
		},
		UsersReqType: RequestConfig{
			ReqType:   UsersReqType,
			takeInput: false,
		},
		DocumentReqType: RequestConfig{
			ReqType:   DocumentReqType,
			takeInput: false,
		},
		ListActionReqType: RequestConfig{
			ReqType:   ListActionReqType,
			takeInput: false,
		},
	}

	reader   *bufio.Reader
	clientID string
)

func main() {
	var Host string
	var Port string
	flag.StringVar(&Host, "host", "localhost", "Server hostname")
	flag.StringVar(&Port, "port", "8000", "Server port")

	flag.Parse()

	clientID, _ = randomHex(10)
	fmt.Println(clientID)

	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%s", Host, Port))

	if err != nil {
		fmt.Println(errors.Wrap(err, "Error contacting server"))
		os.Exit(1)
	}

	reader = bufio.NewReader(os.Stdin)
	for {
		fmt.Print("\nRequest for server:\n\nfnv - Calculate FNV Hash\nusers - Number of users on the server\ndocument - Document from server\nlist - list online actions\n\nSelection: ")

		ReqType, _ := reader.ReadString('\n')
		ReqType = strings.TrimSuffix(ReqType, "\n")

		switch ReqType {
		case FnvReqType, UsersReqType, DocumentReqType, ListActionReqType:
			DoRequest(conn, ReqConfigStore[ReqType])
		default:
			fmt.Printf("Invalid input: %s!\n", ReqType)
		}
	}
}

func getConnReaderWriter(conn net.Conn) (*bufio.Reader, *bufio.Writer) {
	return bufio.NewReader(conn), bufio.NewWriter(conn)
}

// WriteChannelMessageToConn marshals and writes a Channel.ChannelMessage to the connection via its Writer.
func WriteChannelMessageToConn(writer *bufio.Writer, channelMsg *Channel.ChannelMessage) error {
	channelMsgBytes, err := MarshalChannelMessage(channelMsg)
	if err != nil {
		return errors.Wrap(err, "failed marshaling channel message")
	}

	writer.Write(channelMsgBytes)
	writer.Flush()

	return nil
}

// WriteMessageToConn writes a message to the connection via its writer.
func WriteMessageToConn(writer *bufio.Writer, ReqType string, msg string, clientId string) error {
	channelMsg := NewChannelMessage(ReqType, clientId, msg)
	return WriteChannelMessageToConn(writer, channelMsg)
}

// DoRequest performs request according to reqConfig.
func DoRequest(conn net.Conn, reqConfig RequestConfig) {
	var inp string

	r, w := getConnReaderWriter(conn)

	if reqConfig.takeInput {
		fmt.Print(fmt.Sprintf("[%s] %s", reqConfig.ReqType, reqConfig.inputMessage))
		inp, _ = reader.ReadString('\n')
		inp = strings.TrimSuffix(inp, "\n")
	}

	WriteMessageToConn(w, reqConfig.ReqType, inp, clientID)

	var msg []byte = make([]byte, 4096)
	var n int

	n, err := r.Read(msg)
	if err != nil {
		if err == io.EOF {
			return
		}
	}

	serverMessage, err := ParseChannelMessage(msg[:n])

	if err != nil || serverMessage == nil {
		fmt.Println(errors.Wrap(err, "Fatal error, failed parsing server message, exiting"))
		os.Exit(1)
	}

	fmt.Printf("[%s][%s] Response: %s\n", serverMessage.ClientId, serverMessage.ReqType, serverMessage.Message)
}
