.PHONY: build/



all: build
build: v1-proto v2-proto bins

bins: server client

server:
	go build -o ./build/server ./cmd/server
	chmod +x ./build/server

client:
	go build -o ./build/client ./cmd/client
	chmod +x ./build/client

v1-proto:
	protoc --go_out=. pkg/proto/v1/channel.proto

v2-proto:
	protoc --go_out=. pkg/proto/v2/channel.proto
