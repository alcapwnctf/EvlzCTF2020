#ifndef HANDLER_H
#define HANDLER_H

#include"common.h"
#include"ipc.h"
#include"connection.h"
#include"renderer.h"
#include<sys/wait.h>

// void handler(int reader, int writer);
void init_handler(int reader, int writer);

#endif