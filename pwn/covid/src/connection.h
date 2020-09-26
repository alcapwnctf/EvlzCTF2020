#ifndef CONNECTION_H
#define CONNECTION_H

#include<sys/socket.h>
#include<netinet/in.h>
#include<netdb.h>
#include"common.h"
#include"ipc.h"

int make_connection(char* hostname, int port);
void handle_request(int writer, request* reqbuffer);

#endif