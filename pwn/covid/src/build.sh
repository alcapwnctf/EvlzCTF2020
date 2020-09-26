#!/bin/bash
# Built on ubuntu 16.04 with libc 2.23
# Intended to be solved on Ubuntu 16.04

gcc covid.c common.c connection.c ipc.c handler.c renderer.c seccomp.c -lpthread -no-pie -fno-stack-protector -o covid
strip -s covid
