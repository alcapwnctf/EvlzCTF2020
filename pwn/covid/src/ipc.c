#include "ipc.h"

int get_request(msgargs* msg){
    if(msg->reqbuffer == NULL)return -1;
    return read(msg->reader, msg->reqbuffer, sizeof(request));
}

int put_request(msgargs* msg){
    if(msg->reqbuffer == NULL)return -1;
    return write(msg->writer, msg->reqbuffer, sizeof(request));
}

int get_response(msgargs* msg){
    if(msg->respbuffer == NULL)return -1;
    return read(msg->reader, msg->respbuffer, sizeof(response));
}

int put_response(msgargs* msg){
    if(msg->respbuffer == NULL)return -1;
    return write(msg->writer, msg->respbuffer, sizeof(response));
}