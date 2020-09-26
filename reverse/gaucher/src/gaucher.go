package main

import (
	"bufio"
	"fmt"
	"os"
)

type node struct {
	value int
	label rune
	next  *node
	prev  *node
}

var node39 = node{value: 39, label: '}', next: nil, prev: nil}
var node38 = node{value: 38, label: '{', next: &node39, prev: nil}
var node37 = node{value: 37, label: '0', next: &node38, prev: nil}
var node36 = node{value: 36, label: '9', next: &node37, prev: nil}
var node35 = node{value: 35, label: '8', next: &node36, prev: nil}
var node34 = node{value: 34, label: '7', next: &node35, prev: nil}
var node33 = node{value: 33, label: '6', next: &node34, prev: nil}
var node32 = node{value: 32, label: '5', next: &node33, prev: nil}
var node31 = node{value: 31, label: '4', next: &node32, prev: nil}
var node30 = node{value: 30, label: '3', next: &node31, prev: nil}
var node29 = node{value: 29, label: '2', next: &node30, prev: nil}
var node28 = node{value: 28, label: '1', next: &node29, prev: nil}
var node27 = node{value: 27, label: 'e', next: &node28, prev: nil}
var node26 = node{value: 26, label: 'c', next: &node27, prev: nil}
var node25 = node{value: 25, label: 'y', next: &node26, prev: nil}
var node24 = node{value: 24, label: 'a', next: &node25, prev: nil}
var node23 = node{value: 23, label: 'd', next: &node24, prev: nil}
var node22 = node{value: 22, label: 'r', next: &node23, prev: nil}
var node21 = node{value: 21, label: 'o', next: &node22, prev: nil}
var node20 = node{value: 20, label: 't', next: &node21, prev: nil}
var node19 = node{value: 19, label: 'j', next: &node20, prev: nil}
var node18 = node{value: 18, label: 'v', next: &node19, prev: nil}
var node17 = node{value: 17, label: 'p', next: &node18, prev: nil}
var node16 = node{value: 16, label: 'q', next: &node17, prev: nil}
var node15 = node{value: 15, label: 'u', next: &node16, prev: nil}
var node14 = node{value: 14, label: 'm', next: &node15, prev: nil}
var node13 = node{value: 13, label: 'n', next: &node14, prev: nil}
var node12 = node{value: 12, label: 'h', next: &node13, prev: nil}
var node11 = node{value: 11, label: 'k', next: &node12, prev: nil}
var node10 = node{value: 10, label: 's', next: &node11, prev: nil}
var node9 = node{value: 9, label: 'i', next: &node10, prev: nil}
var node8 = node{value: 8, label: 'l', next: &node9, prev: nil}
var node7 = node{value: 7, label: 'w', next: &node8, prev: nil}
var node6 = node{value: 6, label: 'f', next: &node7, prev: nil}
var node5 = node{value: 5, label: '_', next: &node6, prev: nil}
var node4 = node{value: 4, label: 'g', next: &node5, prev: nil}
var node3 = node{value: 3, label: 'z', next: &node4, prev: nil}
var node2 = node{value: 2, label: 'b', next: &node3, prev: nil}
var node1 = node{value: 1, label: 'x', next: &node2, prev: &node39}

var nodeNext = &node1
var nodePrev = &node1

var flag = []byte{27, 18, 8, 3, 38, 26, 12, 15, 26, 11, 5, 2, 30, 22, 22, 25, 5, 12, 9, 20, 10, 39, 26, 20, 6}

func findNode(letter rune) int {
	for nodeNext != nil {
		if nodeNext.label == letter {
			return nodeNext.value
		}
		nodeNext = nodeNext.next

		if nodePrev.label == letter {
			return nodePrev.value
		}
		nodePrev = nodePrev.next
	}
	return -1
}

func parseInput(input string) bool {
	if len(input) < len(flag) {
		return false
	}
	for i := range flag {
		value := findNode(rune(input[i]))
		if value != int(flag[i]) {
			return false
		}
	}
	if len(input) > len(flag) {
		return false
	}
	return true
}

func main() {

	node39.next = &node1
	node39.prev = &node38
	node38.prev = &node37
	node37.prev = &node36
	node36.prev = &node35
	node35.prev = &node34
	node34.prev = &node33
	node33.prev = &node32
	node32.prev = &node31
	node31.prev = &node30
	node30.prev = &node29
	node29.prev = &node28
	node28.prev = &node27
	node27.prev = &node26
	node26.prev = &node25
	node25.prev = &node24
	node24.prev = &node23
	node23.prev = &node22
	node22.prev = &node21
	node21.prev = &node20
	node20.prev = &node19
	node19.prev = &node18
	node18.prev = &node17
	node17.prev = &node16
	node16.prev = &node15
	node15.prev = &node14
	node14.prev = &node13
	node13.prev = &node12
	node12.prev = &node11
	node11.prev = &node10
	node10.prev = &node9
	node9.prev = &node8
	node8.prev = &node7
	node7.prev = &node6
	node6.prev = &node5
	node5.prev = &node4
	node4.prev = &node3
	node3.prev = &node2
	node2.prev = &node1

	fmt.Println("Enter password: ")
	user_input, _, err := bufio.NewReader(os.Stdin).ReadLine()
	if err != nil {
		fmt.Println("Error reading input:", err)
		os.Exit(1)
	}
	if len(user_input) < 17 {
		fmt.Println("Password too short!")
		os.Exit(1)
	}

	if parseInput(string(user_input)) == true {
		fmt.Println("Correct password! That's your flag.")
	} else {
		fmt.Println("Wrong password!")
	}
}
