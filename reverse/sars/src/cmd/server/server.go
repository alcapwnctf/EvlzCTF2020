package main

import (
	"bufio"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"hash/fnv"
	"io"
	"net"
	"os"
	"sync/atomic"

	Channel "github.com/arush15june/protobuf-forward-compat/pkg/proto/v2"
	"github.com/pkg/errors"
	"google.golang.org/protobuf/proto"
)

const (
	Flag            = "evlz{ev0lu7i0n_1s_1mp0rt4nt_f0r_pr0t0buf}ctf"
	DefaultClientID = "0000"

	ErrorReqtype      = "error"
	FnvReqtype        = "fnv"
	UsersReqtype      = "users"
	DocumentReqtype   = "document"
	ListActionReqType = "list"
	ListFilesReqType  = "ls"
	ReadFileReqType   = "read"

	InvalidReqtypeMessage = "invalid request type."
	DocumentMessage       = "This is a usage document for the application.\nOur protocol buffers are the best in town! Both in the future and past."
)

var (
	// DefaultKey is the key for AES Handler.
	DefaultKey = []byte("HAHA_KEY_GO_BRRR")

	// TotalUsers is the total number of connections to the server.
	TotalUsers int64 = 0

	// Files is the list of files returned to user.
	Files []string
)

func randomHex(n int) (string, error) {
	bytes := make([]byte, n)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes), nil
}

func generateFileList() []string {
	file_list := []string{}
	for i := 1; i <= 10; i++ {
		file_name, _ := randomHex(6)
		file_list = append(file_list, file_name)
	}

	return file_list
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
func NewChannelMessage(reqType string, clientId string, msg string, getFlag string) *Channel.ChannelMessage {
	channelMsg := &Channel.ChannelMessage{
		ReqType:  reqType,
		ClientId: clientId,
		Message:  msg,
		GetFlag:  getFlag,
	}

	return channelMsg
}

// MarshalChannelMessage marshals a Channel.ChannelMessage to a bytestream.
func MarshalChannelMessage(channelMsg *Channel.ChannelMessage) ([]byte, error) {
	return proto.Marshal(channelMsg)
}

/*
	TCP Listener and Helpers
*/

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
func WriteMessageToConn(writer *bufio.Writer, reqType string, msg string, clientId string, getFlag string) error {
	channelMsg := NewChannelMessage(reqType, clientId, msg, getFlag)
	return WriteChannelMessageToConn(writer, channelMsg)
}

// WriteErrorToConn writes an error type ChannelMessage to the conn.
func WriteErrorToConn(writer *bufio.Writer, clientId string, msg string) error {
	return WriteMessageToConn(
		writer,
		ErrorReqtype,
		msg,
		clientId,
		"0",
	)
}

// TCPListener initializes TCP server.
func TCPListener(host string) {
	listener, err := net.Listen("tcp4", host)
	fmt.Println("Started listening at:" + host)

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
	var clientMessage *Channel.ChannelMessage

	reader := bufio.NewReader(conn)

	writer := bufio.NewWriter(conn)

	for {
		var msg []byte = make([]byte, 4096)
		var n int

		n, err = reader.Read(msg)
		if err != nil {
			if err == io.EOF {
				break
			}
		}

		clientMessage, err = ParseChannelMessage(msg[:n])
		if err != nil || clientMessage == nil {
			fmt.Printf("[%s] Error parsing channel message", conn.RemoteAddr().String())
			WriteErrorToConn(writer, DefaultClientID, errors.Wrap(err, "error parsing channel message").Error())
			break
		}

		ClientWantFlag := clientMessage.GetFlag
		messageResult, err := HandleChannelMessage(clientMessage, conn.RemoteAddr().String())
		if err != nil {
			fmt.Printf("[%s] Error handling client message", conn.RemoteAddr().String())
			WriteErrorToConn(writer, clientMessage.ClientId, errors.Wrap(err, "error during message handling").Error())
			break
		}

		if ClientWantFlag == "1" {
			messageResult.GetFlag = "1"
		}

		WriteChannelMessageToConn(writer, messageResult)
	}

	return nil

}

/*
	ChannelMessage Message Handlers.
*/

// HandleChannelMessage is the root message handler for Channel.ChannelMessage,
// it returns its result to the TCP Handler as a Channel.ChannelMessage
// If there is an error, an error message is returned.
func HandleChannelMessage(channelMessage *Channel.ChannelMessage, remoteAddr string) (*Channel.ChannelMessage, error) {
	fmt.Printf("[%s] Got message request: %s\n", remoteAddr, channelMessage.ReqType)
	switch channelMessage.ReqType {
	case FnvReqtype:
		return HandleFnvMessage(channelMessage)
	case UsersReqtype:
		return HandleUsersMessage(channelMessage)
	case DocumentReqtype:
		return HandleDocumentMessage(channelMessage)
	case ListActionReqType:
		return HandleListActionMessage(channelMessage)
	case ListFilesReqType:
		return HandleListFilesMessage(channelMessage)
	case ReadFileReqType:
		return HandleReadFileMessage(channelMessage)
	default:
		return nil, errors.New(InvalidReqtypeMessage)
	}
}

// HandleFnvMessage calculates the FNV hash of ChannelMessage.Message.
func HandleFnvMessage(channelMessage *Channel.ChannelMessage) (*Channel.ChannelMessage, error) {
	if channelMessage.Message == "" {
		return nil, errors.New("Invalid input for hashing")
	}

	msg := []byte(channelMessage.Message)

	hash := fnv.New64a()

	hashHex := hex.EncodeToString(hash.Sum(msg))

	return NewChannelMessage(
		FnvReqtype,
		channelMessage.ClientId,
		hashHex,
		"0",
	), nil
}

// HandleUsersMessage returns the number of connections on the server.
func HandleUsersMessage(channelMessage *Channel.ChannelMessage) (*Channel.ChannelMessage, error) {
	return NewChannelMessage(
		UsersReqtype,
		channelMessage.ClientId,
		fmt.Sprintf("%d", TotalUsers),
		"0",
	), nil
}

// HandleDocumentMessage returns usage document.
func HandleDocumentMessage(channelMessage *Channel.ChannelMessage) (*Channel.ChannelMessage, error) {
	return NewChannelMessage(
		DocumentReqtype,
		channelMessage.ClientId,
		fmt.Sprintf("%s", DocumentMessage),
		"0",
	), nil
}

// HandleListActionMessage returns list of available actions.
func HandleListActionMessage(channelMessage *Channel.ChannelMessage) (*Channel.ChannelMessage, error) {
	msg := fmt.Sprintf("\n%s\n%s\n%s\n%s\n%s\n%s\n",
		FnvReqtype,
		UsersReqtype,
		DocumentReqtype,
		ListActionReqType,
		ListFilesReqType,
		ReadFileReqType,
	)

	return NewChannelMessage(
		DocumentReqtype,
		channelMessage.ClientId,
		msg,
		"0",
	), nil
}

// HandleListFilesMessage handles request for listing files on server.
func HandleListFilesMessage(channelMessage *Channel.ChannelMessage) (*Channel.ChannelMessage, error) {
	msg := "\n"
	for _, file := range Files {
		msg += fmt.Sprintf("%s\n", file)
	}

	msg += "flag\n"

	return NewChannelMessage(
		ListFilesReqType,
		channelMessage.ClientId,
		msg,
		"0",
	), nil
}

// HandleReadFileMessage handles request for reading files on server.
func HandleReadFileMessage(channelMessage *Channel.ChannelMessage) (*Channel.ChannelMessage, error) {
	var msg string

	fileName := channelMessage.Message
	fileFound := false

	for _, file := range Files {
		if fileName == file {
			fileFound = true
		}
	}

	if fileName == "flag" {
		if channelMessage.GetFlag == "1" {
			msg = Flag
		} else {
			msg = "Invalid permissions to read flag!"
		}
	} else if fileFound {
		fileData, _ := randomHex(24)
		msg = fileData
	} else {
		msg = "File not found!"
	}

	return NewChannelMessage(
		ReadFileReqType,
		channelMessage.ClientId,
		msg,
		"0",
	), nil
}

func main() {
	Files = generateFileList()

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
