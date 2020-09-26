#include <stdio.h>
#include <stdlib.h>

unsigned count=0,target = 0xdeadbeef;
void* ptrlist[16] = {0};

int getNum(char* msg){
    char buf[10];
    printf("%s >> ",msg);
    int val = atoi(fgets(buf,sizeof(buf),stdin));
    if (val<0) return -1*val;
    return val;
}

int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    
    int idx, exit=0;
    
    while(1){
        if(exit)break;
        switch(getNum("Choice")){
            case 1:
                ptrlist[count] = malloc((getNum("Size")%100)+2000);
                count+=1;
                break;
            case 2:
                idx = getNum("Index");
                if (idx < 15){
                   printf("Data >> ");
                   fgets(ptrlist[idx],50,stdin);
                }
                break;
            case 3:
                idx = getNum("Index");
                if ((idx < 15)&&(ptrlist[idx]!=NULL))free(ptrlist[idx]);
                break;
            default:
                exit=1;
                break;
        }
    }
    if (target != 0xdeadbeef)system("/bin/sh");
    return 0;
}