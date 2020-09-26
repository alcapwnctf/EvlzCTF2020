#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

#define RNA_SEQUENCE_SIZE 65536


typedef struct {
    unsigned char rna_bytes[RNA_SEQUENCE_SIZE];
    int rna_size;
} rna;


rna *rna_1() {
    rna *sequencing = malloc(sizeof(rna));
    sequencing->rna_size = 0;
    return sequencing;  
}

typedef struct {
    rna *rna_bytes;
    rna *stream;
    rna *stream_output;
    rna *operations[0x20];
}   genome;

genome genome_1() {
    genome structure;
    structure.rna_bytes = rna_1();
    structure.stream = rna_1();
    structure.stream_output = rna_1();
    for(int i = 0; i < 0x20; i++){
        structure.operations[i] = rna_1();
    }
    return structure;
}

void create_sequence(rna *sequencing, char code) {
    if(sequencing->rna_size >= RNA_SEQUENCE_SIZE){
        printf("\n[-] Caution! The links are breaking.\n");
        exit(1);
    }
    sequencing->rna_size[sequencing->rna_bytes] = code;
    sequencing->rna_size++;
}

char break_sequence(rna *sequencing){
    if(sequencing->rna_size == 0) {
        printf("\n[-] Caution! The links do not exist anymore!\n");
        exit(1);
    }
    sequencing->rna_size--;
    return sequencing->rna_bytes[sequencing->rna_size];
}

void sequencing_operation(genome *gen) {
    unsigned char scode = break_sequence(gen->stream);
    if ( scode < 0x69 ) {
        create_sequence(gen->rna_bytes, scode);
        return;
    }
    if (scode == 0x69) {
        create_sequence(gen->rna_bytes, break_sequence(gen->rna_bytes) ^ 0x69);
        return;
    }
    if (scode == 0x73) {
        unsigned char pcode = break_sequence(gen->rna_bytes);
        if (pcode == 0 ) {
            create_sequence(gen->rna_bytes, 0xff);
        } else {
            create_sequence(gen->rna_bytes, 0);
        }
        return;
    }
    if (scode == 0x77) {
        unsigned char x = break_sequence(gen->rna_bytes);
        unsigned char y = break_sequence(gen->rna_bytes);
        create_sequence(gen->rna_bytes, x & y);
        return;
    }
    if (scode == 0x88) {
        unsigned char x = break_sequence(gen->rna_bytes);
        unsigned char y = break_sequence(gen->rna_bytes);
        create_sequence(gen->rna_bytes, x | y);
        return;
    }
    if (scode == 0x87) {
        unsigned char x = break_sequence(gen->rna_bytes);
        unsigned char y = break_sequence(gen->rna_bytes);
        create_sequence(gen->rna_bytes, x ^ y);
        return;
    }
    if (scode == 0x90) {
        unsigned char x = break_sequence(gen->rna_bytes);
        unsigned char y = break_sequence(gen->rna_bytes);
        create_sequence(gen->rna_bytes, x);
        create_sequence(gen->rna_bytes, y);
        return;
    }
    if (scode == 0x91) {
        unsigned char x = break_sequence(gen->rna_bytes);
        create_sequence(gen->rna_bytes, x);
        create_sequence(gen->rna_bytes, x);
        return;
    }
    if (scode == 0xa0) {
        unsigned char x = break_sequence(gen->rna_bytes);
        if (x >= 0x20) {
            printf("\n[-] Caution! The sequence is broken.");
            exit(1);
        }
        gen->operations[x]->rna_size=0;
        unsigned char y;
        while ((y = break_sequence(gen->rna_bytes))!= 0xa1){
            create_sequence(gen->operations[x], y);
        }
        return;
    }
    if (scode == 0xb0) {
        create_sequence(gen->stream_output, break_sequence(gen->rna_bytes));
        return;
    }
    if (scode >= 0xc0 && scode < 0xe0){
        unsigned char x = scode - 0xc0;
        rna *rna_2 = gen->operations[x];
        for( int i = rna_2->rna_size - 1; i >= 0; i--){
            create_sequence(gen->stream, rna_2->rna_bytes[i]);
        }
        return;
    }
    if (scode >= 0xe0) {
        unsigned char x = scode - 0xe0;
        if (break_sequence(gen->rna_bytes)) {
            rna *rna_2 = gen->operations[x];
            for( int i = rna_2->rna_size - 1; i >= 0; i--){
            create_sequence(gen->stream, rna_2->rna_bytes[i]);
            }   
        }
        return;
    }
}


int cracked(){
    puts("\n[+]Congrats!! The retrovirus has successfully invaded the host cell, here's your reward, go brr!!!\n");
    system("/bin/cat flag.txt");
    return 0;
}

int main(int argc, char* argv[]){
    int rna_length = 0;
    int i = 0;
    
    setvbuf(stdout, NULL, _IONBF,  0);
    printf("[!] Quick! Get here!! I need your help breaking into the host cell, we need to insert a copy of our RNA genome.\n");
    printf("[!] We need to perfrom some hax0r-RNA sequencing for our gene expression!\n");
    printf("[!] Caution: Don't get lost in translation, just blame the RNA :)\n");
    printf("[+] Enter the length of your RNA sequence: ");
    scanf("%d", &rna_length);
    if (rna_length <=0 || rna_length >=65535){
        puts("\n[-] Nope, you're going to break it, try again.");
        exit(1);
    }
    printf("\n[+] Enter the RNA sequence: ");
    unsigned char* rna_sequence = malloc(rna_length);
    for(i = 0; i < rna_length; i ++){
        read(0, rna_sequence + i, 1);
    }
    genome gen = genome_1();
    for(int i = rna_length - 1; i >= 0; i--){
        create_sequence(gen.stream, rna_sequence[i]);
    }
    while (gen.stream->rna_size > 0){
        sequencing_operation(&gen);
    }
    if ( rna_length != gen.stream_output->rna_size){
        printf("\n[-] Caution! The sequence is broken.");
        write(1, gen.stream_output->rna_bytes, gen.stream_output->rna_size);
        exit(1);
    }
    for (int i = 0; i < rna_length; i++){
        if(gen.stream_output->rna_bytes[i] != rna_sequence[i]){
            printf("\n[-] Caution! The sequence is broken.");
            write(1, gen.stream_output->rna_bytes, gen.stream_output->rna_size);
            exit(1);
        }
    }
    cracked();
    exit(0);    
    return 0;
}