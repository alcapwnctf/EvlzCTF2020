// g++ -fno-stack-protector -fpermissive toscana.cpp -o ToscanaVirus
#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<vector>

#define flen 40
using namespace std;

void junk_func1(char* inputcode, vector<int> bit_array, int** init_pad){
    int index = 0;
    (*init_pad) = malloc(sizeof(int) * flen);
    for(index=0; index < flen; index++){
        (*init_pad)[index] = 0;
    }
    for(index=0; index < flen; index++){
        while(bit_array[index]!=0){
                (*init_pad)[index]++;
                bit_array[index]--;
        }
    }
}

void junk_func2(char* inputcode, int** init_pad){
    int index = 0;
    FILE *fp = fopen("/dev/null", "w");
    for(index = 0; index < flen; index ++){
            switch(inputcode[index]){
                    case 'e':
                        fprintf(fp, "%s", "BEEP");
                        break;
                    case 'v':
                        fprintf(fp, "%s", "BOOP");
                        break;
                    case 'l':
                        fprintf(fp, "%s", "BEEP");
                        break;
                    case 'z':
                        fprintf(fp, "%s", "BOOP");
                        break;
                    default:
                        break;
            }
    }

}

int junk_func3(char* inputcode){
    int i=0;
    int j=5;
    int k=40;
    while(k!=0){
        if(inputcode[i]=='_'){
            j = j & 3;
        }
        i++;
        k--;
    }
    if (j==95){
        return 0;
    }
    else {
            return 1;
    }
}
void useful_func4(char* inputcode, int** init_pad){
    int index = 0;
    int* init_pad2;
    init_pad2 = malloc(sizeof(int) * flen);
    for(index = 0; index < 40; index ++){
        (*init_pad)[index] = inputcode[index] << (*init_pad)[index];
    }
    free(init_pad2);
}
int checkthecode(int* init_pad){
    int index;
    vector<int> shifted;
    shifted.push_back(404);
    shifted.push_back(472);
    shifted.push_back(864);
    shifted.push_back(31232);
    shifted.push_back(984);
    shifted.push_back(2592);
    shifted.push_back(340);
    shifted.push_back(264);
    shifted.push_back(1712);
    shifted.push_back(48640);
    shifted.push_back(1664);
    shifted.push_back(1568);
    shifted.push_back(51200);
    shifted.push_back(13056);
    shifted.push_back(380);
    shifted.push_back(1936);
    shifted.push_back(3072);
    shifted.push_back(234);
    shifted.push_back(144);
    shifted.push_back(48640);
    shifted.push_back(200);
    shifted.push_back(1632);
    shifted.push_back(104);
    shifted.push_back(440);
    shifted.push_back(53248);
    shifted.push_back(1520);
    shifted.push_back(416);
    shifted.push_back(1792);
    shifted.push_back(7168);
    shifted.push_back(14592);
    shifted.push_back(24576);
    shifted.push_back(1664);
    shifted.push_back(50688);
    shifted.push_back(3328);
    shifted.push_back(26112);
    shifted.push_back(1696);
    shifted.push_back(250);
    shifted.push_back(198);
    shifted.push_back(3712);
    shifted.push_back(408);
    for(index=0; index< flen; index ++){
            if(shifted[index]!= init_pad[index]){
                return 0;
            }
    }
    return 1;
}


int keycodecheck(char* inputcode) {
    vector<int> bit_array;
    int check = 0;
    int* init_pad;
    int* drop;
    bit_array.push_back(2);
    bit_array.push_back(2);
    bit_array.push_back(3);
    bit_array.push_back(8);
    bit_array.push_back(3);
    bit_array.push_back(5);
    bit_array.push_back(2);
    bit_array.push_back(3);
    bit_array.push_back(4);
    bit_array.push_back(9);
    bit_array.push_back(4);
    bit_array.push_back(5);
    bit_array.push_back(9);
    bit_array.push_back(8);
    bit_array.push_back(2);
    bit_array.push_back(4);
    bit_array.push_back(6);
    bit_array.push_back(1);
    bit_array.push_back(2);
    bit_array.push_back(9);
    bit_array.push_back(1);
    bit_array.push_back(5);
    bit_array.push_back(1);
    bit_array.push_back(3);
    bit_array.push_back(9);
    bit_array.push_back(4);
    bit_array.push_back(3);
    bit_array.push_back(4);
    bit_array.push_back(6);
    bit_array.push_back(7);
    bit_array.push_back(9);
    bit_array.push_back(5);
    bit_array.push_back(9);
    bit_array.push_back(5);
    bit_array.push_back(9);
    bit_array.push_back(5);
    bit_array.push_back(1);
    bit_array.push_back(1);
    bit_array.push_back(5);
    bit_array.push_back(2);

    junk_func1(inputcode, bit_array, &init_pad);
    junk_func2(inputcode, &init_pad);
    check = junk_func3(inputcode);
    useful_func4(inputcode, &init_pad);
    if (checkthecode(init_pad) == 1)
    {
        return 1;
    }
    else
    {
        return 0;
    }
    
}

int main(int argc, char* argv[]){
    printf("++ Welcome to the hive, fellow negative-stranded RNA agent, unlike our double-stranded Rotavirus brethren,\n");
    printf("++ we depend on our notorious buddy sAnDfLy of the genus Phlebotomus to wreak havoc!!!\n");
    printf("\n");
    printf("#######################################################\n");
    printf("++ Alas, some stupid sapient has locked out our sandfly swarm in a secure cage, and it's up to you to hack it open. (╬ ಠ益ಠ) \n");
    printf("\n");
    printf("#######################################################\n");
    printf("++ Go on; it's time to pwn his immune system, there is no coming back. (⊙_◎) \n");
    fflush(stdout);
    char input[41];
    int index;
    printf("\n***** At the gates of the giant cage *****");
    printf("\n***** A lock with keypad appears, some randomness was also found closeby ***** \n");
    if(fgets(input, 41, stdin) != NULL){
        if(keycodecheck(input) == 1){
            printf("\n[+] The flies are free, run for your life homo sapiens!");
            fflush(stdout);
        }
        else {
            printf("\n[-] The cage self destructed, you've failed your mission, go brrrr!");
            fflush(stdout);
        }
    }
    else{
        return -1;
    }

}
