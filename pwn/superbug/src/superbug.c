#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char name[100] = {0};

unsigned long long getNum(char* msg){
    char buf[32];
    char* nline="\n";
    printf("%s >> ",msg);
    unsigned long long val = strtoull(fgets(buf,sizeof(buf),stdin),&nline,16);
    return val;
}

void myworld(){
    int rSize=8,wSize=8,exit=0,i=0,j=0;
    unsigned long long location;
    printf("What is your ultimate?? >> ");
    fgets(name,sizeof(name),stdin);
    name[strlen(name)-1]=0;
    
    for(i=0,j=0;i<strlen(name);i++){
        if (name[i]!='n'){
            name[j]=name[i];
            j++;
        }
    }
    name[j]=0;
    printf("We hope to see ");
    printf(name);
    printf(" in action\n");

    while(1){
        if(exit)break;
        printf("1. Read\n2. Write\n");
        switch(getNum("Choice")){
            case 1:
                location = getNum("Read from address");
                write(1,(void *)location,rSize);
                break;
            case 2:
                location = getNum("Write to address");
                read(0,(void *)location,wSize);
                break;
            default:
                exit=1;
        }
    }
}

int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    myworld();
    return 0;
}