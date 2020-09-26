#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char *note[256];


void delete()
{
  signed char idx;

  idx = 0;
  printf("IDX : ");
  __isoc99_scanf("%hhd", &idx);
  free(note[idx]);
  note[idx] = 0LL;
 }

void show()
{
  signed char idx;
  printf("IDX : ");
  __isoc99_scanf("%hhd", &idx);
  if ( note[idx] )
    puts(note[idx]);
}

void new()
{
  signed char idx;
  signed short size;


  printf("Index : ");
  __isoc99_scanf("%hhd", &idx);
  printf("Size : ");
  __isoc99_scanf("%hd", &size);
  _IO_getc(stdin);
  note[idx] = (char *)malloc(size);
  if ( note[idx] )
  {
    printf("Content: ");
    fgets(note[idx], size, stdin);
  }
}

int take_flag()
{
  FILE *stream; // ST08_8
  char ptr[0x110];
  memset(&ptr, 0, 0x100uLL);
  stream = fopen("fake_flag", "r");
  fread(&ptr, 1uLL, 0x100uLL, stream);
  puts(&ptr);
  fclose(stream);
  return 0;
}

void menu()
{
  puts("----------------");
  puts("1. Add a Note");
  puts("2. Show a Note");
  puts("3. Remove a Note");
  puts("4. Take a Flag");
  puts("5. Good bye");
  puts("-----------------");
}

int main(int argc, const char **argv, const char **envp)
{
  signed char choice;

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  choice = 0;
  while ( 1 )
  {
    menu();
    printf(">> ");
    __isoc99_scanf("%hhd", &choice);
    switch (choice)
    {
      case 1u:
        new();
        break;
      case 2u:
        show();
        break;
      case 3u:
        delete();
        break;
      case 4u:
        take_flag();
        break;
      case 5u:
        exit(0);
        return 0;
      default:
        continue;
    }
  }
}