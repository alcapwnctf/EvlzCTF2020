#include"handler.h"

void* request_handler(void* rw){
    request request_buffer = *((struct msgargs*)rw)->reqbuffer;
    int writer = ((struct msgargs*)rw)->writer;
    handle_request(writer, &request_buffer);
}

void* handler(void* rw){

    int reader = ((struct msgargs*)rw)->reader;
    int writer = ((struct msgargs*)rw)->writer;

    pthread_t req_tids[MAX_TABS];
    request genreqbuffer, reqbuffers[MAX_TABS];
    msgargs genmsgargs={reader, -1, &genreqbuffer, NULL}, msgbuffers[MAX_TABS]={-1, writer, NULL, NULL, -1, writer, NULL, NULL, -1, writer, NULL, NULL, -1, writer, NULL, NULL};

    for (;;){
        if (get_request(&genmsgargs) > 0){
            if((genreqbuffer.slot>=0) &&(genreqbuffer.slot<=MAX_TABS)){
                reqbuffers[genreqbuffer.slot] = genreqbuffer;
                msgbuffers[genreqbuffer.slot].reqbuffer = &reqbuffers[genreqbuffer.slot];
                pthread_create(&req_tids[genreqbuffer.slot], NULL, request_handler, &msgbuffers[genreqbuffer.slot]);
            }
        }
    }
}

void init_handler(int reader, int writer){
    msgargs rw = {reader, writer, NULL, NULL};
    pthread_t handler_tid;
    pthread_create(&handler_tid, NULL, handler, (void *)&rw);
}