#include "connection.h"

char* METADATA_BUFFER = NULL;
char* DATA_BUFFER = NULL;

int make_connection(char* hostname, int port){
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("Error opening socket");

    struct hostent *host = gethostbyname(hostname);
    if (host == NULL){
        close(sockfd);
        return -1;
    }

    struct sockaddr_in addr = {0};

    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr = *((struct in_addr *)host->h_addr_list[0]);

    if (connect(sockfd, (const struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(sockfd);
        return -1;
    }
    return sockfd;
}

void convert_byte_to_num(char* sizebuf, unsigned* size){
    memcpy((char*)size, sizebuf, 4);
}

void handle_request(int writer, request* reqbuffer){
    int readbytes;
    char sizebuf[4] = {0};
    char sm[8];
    char sd[64];
    
    response respbuffer = {-1, -1, 0, 0};
    msgargs respmsg = {-1, writer, NULL, &respbuffer};

    int sockfd = make_connection(reqbuffer->hostname, reqbuffer->port);
    if (sockfd < 0){
        put_response(&respmsg);
        close(sockfd);
        return;
    }
    
    readbytes = recv(sockfd, &sizebuf, sizeof(sizebuf), MSG_WAITALL);
    if (readbytes <= 0) {
        put_response(&respmsg);
        close(sockfd);
        return;
    }
    convert_byte_to_num(sizebuf, &respbuffer.m_size);
    
    readbytes = recv(sockfd, &sizebuf, sizeof(sizebuf), MSG_WAITALL);
        if (readbytes <= 0) {
        put_response(&respmsg);
        close(sockfd);
        return;
    }
    convert_byte_to_num(sizebuf, &respbuffer.d_size);

    if(respbuffer.m_size > 512 || respbuffer.d_size > 1024){
        put_response(&respmsg);
        close(sockfd);
        return;
    }

    if((reqbuffer->ss) && (respbuffer.m_size < sizeof(sm))) METADATA_BUFFER = sm;
    else METADATA_BUFFER = (char *)realloc(METADATA_BUFFER, respbuffer.m_size);

    if((reqbuffer->ss) && (respbuffer.d_size < sizeof(sd))) DATA_BUFFER = sd;
    else DATA_BUFFER = (char *)realloc(DATA_BUFFER, respbuffer.d_size);
    
    readbytes = recv(sockfd, METADATA_BUFFER, respbuffer.m_size, MSG_WAITALL);
    if (readbytes != respbuffer.m_size) {
        put_response(&respmsg);
        close(sockfd);
        return;
    }

    readbytes = recv(sockfd, DATA_BUFFER, respbuffer.d_size, MSG_WAITALL);
    if (readbytes != respbuffer.d_size) {
        put_response(&respmsg);
        close(sockfd);
        return;
    }
    close(sockfd);

    respbuffer.status = sockfd;
    respbuffer.slot = reqbuffer->slot;
    put_response(&respmsg);
    
    write(writer, METADATA_BUFFER, respbuffer.m_size);
    write(writer, DATA_BUFFER, respbuffer.d_size);
}