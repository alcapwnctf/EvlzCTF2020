package main

import (
	"fmt"
	"io"
	"log"
	"math/rand"
	"os"
	"sync"
	"time"

	"math/big"

	"github.com/monnand/dhkx"
)

var (
	secret       []byte
	conversation []string
	line         int
	success      bool
)

const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
const flagfile = "/home/autism/flag.txt"

func randomstring(b byte, n int) string {
	randomString := make([]byte, n)
	randomString[0] = b
	for i := 1; i < n; i++ {
		randomString[i] = charset[rand.Intn(len(charset))]
	}
	return string(randomString)
}

func printByAlice(message string) {
	fmt.Printf("Alice: %v\n", message)
}
func printByBob(message string) {
	fmt.Printf("Bob: %v\n", message)
}

func genXORkey(key *dhkx.DHKey) []byte {
	xorkey := make([]byte, 32)
	keybytes := key.Bytes()

	for i := 0; i < 8; i++ {
		for j := 0; j < 32; j++ {
			xorkey[j] ^= keybytes[32*i+j]
		}
	}
	return xorkey
}

func encrypt(key []byte, pt string) string {

	bytePT := []byte(pt)
	byteCT := make([]byte, 32)

	for i := 0; i < 32; i++ {
		byteCT[i] = bytePT[i] ^ key[i]
	}

	ct := new(big.Int)
	ct.SetBytes(byteCT)

	return ct.String()
}
func decrypt(key []byte, ct string) string {

	ctb := new(big.Int)
	ctb.SetString(ct, 10)

	byteCT := ctb.Bytes()
	bytePT := make([]byte, 32)

	for i := 0; i < 32; i++ {
		bytePT[i] = byteCT[i] ^ key[i]
	}

	return string(bytePT)
}

func alice(g *dhkx.DHGroup, sync chan bool, wg *sync.WaitGroup) {
	defer wg.Done()
	privkey, _ := g.GeneratePrivateKey(nil)
	pubkey := new(big.Int)
	pubkey.SetBytes(privkey.Bytes())

	printByAlice("Hi, I am Alice")
	sync <- true
	<-sync

	printByAlice(fmt.Sprintf("\n\tG: %v\n\tP: %v\n", g.G(), g.P()))
	sync <- true
	<-sync

	printByAlice("since We are going with Diffie Hellman, we can generate secure channel in an unsecured network, hence we aren't much bothered about you")

	printByAlice(fmt.Sprintf("Here is my public key: %v", pubkey))
	sync <- true
	<-sync

	printByAlice("Please give me Bob's Public key")
	bobkey := ""
	fmt.Scanf("%s", &bobkey)
	bobPubKey := new(big.Int)
	bobPubKey.SetString(bobkey, 10)
	B := dhkx.NewPublicKey(bobPubKey.Bytes())

	key, _ := g.ComputeKey(B, privkey)
	xorkey := genXORkey(key)

	sync <- true

	bobmsg := ""
	for line != len(conversation) {
		<-sync
		printByAlice("Please give me Bob's Message")
		fmt.Scanf("%s", &bobmsg)
		if decrypt(xorkey, bobmsg) != conversation[line] {
			line = len(conversation)
			sync <- true
			return
		}
		line++
		sync <- true
	}
	success = true
}

func bob(g *dhkx.DHGroup, sync chan bool, wg *sync.WaitGroup) {
	defer wg.Done()
	privkey, _ := g.GeneratePrivateKey(nil)
	pubkey := new(big.Int)
	pubkey.SetBytes(privkey.Bytes())

	<-sync

	printByBob("and I am Bob")
	printByBob("We met one day and exchanged our p and g, here it is for your your convinience")
	sync <- true
	<-sync

	printByBob("We want you to handle our key exchanges.")
	sync <- true
	<-sync

	printByBob(fmt.Sprintf("Here is my public key: %v", pubkey))

	printByBob("Please give me Alice's Public key")
	alicekey := ""
	fmt.Scanf("%s", &alicekey)
	alicePubKey := new(big.Int)
	alicePubKey.SetString(alicekey, 10)
	A := dhkx.NewPublicKey(alicePubKey.Bytes())

	key, _ := g.ComputeKey(A, privkey)
	xorkey := genXORkey(key)
	sync <- true
	<-sync

	for line != len(conversation) {
		printByBob(fmt.Sprintf("Please give this to Alice: %v", encrypt(xorkey, conversation[line])))
		sync <- true
		<-sync
	}
}

func main() {
	flag := make([]byte, 100)
	file, err := os.Open(flagfile)
	if err != nil {
		log.Fatalf("Please contact admin with the error: %v", err)
	}

	n, err := file.Read(flag)
	if err != nil {
		if err == io.EOF {
			file.Close()
		} else {
			log.Fatalf("Please contact admin with the error: %v", err)
		}
	}

	rand.Seed(time.Now().Unix())
	for i := 0; i < n; i++ {
		if i > 9 && i < 24 {
			secret = append(secret, flag[i])
			flag[i] = byte('?')
		}
		conversation = append(conversation, randomstring(flag[i], 32))
	}

	var wg sync.WaitGroup
	sync := make(chan bool)
	g, _ := dhkx.GetGroup(0)

	wg.Add(1)
	go alice(g, sync, &wg)

	wg.Add(1)
	go bob(g, sync, &wg)

	wg.Wait()

	if success {
		fmt.Printf("Thank you for you contribution, here is your cut: %v\n", string(secret))
	} else {
		fmt.Println("Go away you spy")
	}
}
