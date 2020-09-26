#!/bin/bash
# Built on ubuntu 16.04 with libc 2.23
# Intended to be solved on Ubuntu 18.04

gcc hiv.c seccomp.c -pie -fPIC -o hiv
