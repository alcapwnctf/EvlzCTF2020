#include"common.h"
#include"renderer.h"
#include"handler.h"

char name[64];

void initiate(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

void banner(){
    puts("Welcome to our browser, press enter to explore");
    fgets(name, sizeof(name), stdin);
    char *pos;
    if ((pos=strchr(name, '\n')) != NULL) *pos = '\0';
}

int main(){
    initiate();
    int parentPipe[2], childPipe[2], status;

    if (pipe(parentPipe) == -1)error("Parent Pipe failure");
    if (pipe(childPipe) == -1)error("Child Pipe failure");
    
    pid_t childPID, parentPID;
    parentPID = getpid();
    banner();
    childPID = fork();
    
    if (childPID < 0)error("Fork failure");
    else if (childPID == 0) renderer(parentPipe[0], childPipe[1]);
    else init_handler(childPipe[0], parentPipe[1]);

    if (childPID)waitpid(childPID, &status, 0);
}