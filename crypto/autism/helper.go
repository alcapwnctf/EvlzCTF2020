package main

import (
	"fmt"
	"math/big"

	"github.com/monnand/dhkx"
)

var (
	secret       []byte
	conversation []string
	line         int
	success      bool
)

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

func getKey(g *dhkx.DHGroup, privkey *dhkx.DHKey) []byte {
	pubkey := new(big.Int)

	keynum := ""
	fmt.Scanf("%s", &keynum)
	pubkey.SetString(keynum, 10)

	dhPubKey := dhkx.NewPublicKey(pubkey.Bytes())
	key, _ := g.ComputeKey(dhPubKey, privkey)
	return genXORkey(key)
}

func main() {

	g, _ := dhkx.GetGroup(0)
	privkey, _ := g.GeneratePrivateKey(nil)
	pubkey := new(big.Int)
	pubkey.SetBytes(privkey.Bytes())
	fmt.Println(pubkey.String())

	fmt.Println(getKey(g, privkey))
	fmt.Println(getKey(g, privkey))
}
