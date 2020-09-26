#!/bin/bash
# Built on ubuntu 16.04 with libc 2.23
# Intended to be solved on Ubuntu 16.04

gcc -DEASYCOVID=1 covid.c common.c connection.c ipc.c handler.c renderer.c seccomp.c -lpthread -no-pie -o easycovid
strip -s easycovid
