#ifndef IPC_H
#define IPC_H

#include "common.h"

typedef struct request{
    char hostname[56];
    int port;
    int slot;
    int ss;
} request;

typedef struct response{
    int status;
    int slot;
    unsigned m_size;
    unsigned d_size;
} response;

typedef struct msgargs {
    int reader;
    int writer;
    request* reqbuffer;
    response* respbuffer;
} msgargs;

int get_request(msgargs* msg);
int put_request(msgargs* msg);
int get_response(msgargs* msg);
int put_response(msgargs* msg);

#endif