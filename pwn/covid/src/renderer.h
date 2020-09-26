#ifndef RENDERER_H
#define RENDERER_H

#include"common.h"
#include"ipc.h"
#include"seccomp.h"

#define MAX_TABS 4

void renderer(int reader, int writer);

#endif