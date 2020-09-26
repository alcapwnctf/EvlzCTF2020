#include"renderer.h"

char* metadata[MAX_TABS];
char* data[MAX_TABS];
char* waitmsg_metadata = "Loading";
char* waitmsg_data = "Waiting for site to load. Please wait";

char print_menu_get_choice(){
    puts("[N]ew Tab");
    puts("[V]iew Tab");
    puts("[C]lose Tab");
    puts("[E]xit");
    printf(">> ");

    char choice = getchar();
    if (choice == EOF)exit(EXIT_SUCCESS);
    getchar();
    return choice;
}

unsigned long long getNum(char* msg){
    char buf[32];
    char* nline="\n";
    printf("%s >> ",msg);
    unsigned long long val = strtoull(fgets(buf,sizeof(buf),stdin),&nline,16);
    return val;
}

int get_tab_slot(){
    for (int i=0; i<MAX_TABS; i++){
        if (metadata[i] == NULL && data[i] == NULL)return i;
    }
    return -1;
}

void closeTab(){
    unsigned long long slot = getNum("Enter Tab ID");
    if (slot < 0 || slot > MAX_TABS || metadata[slot] == NULL ||data[slot] == NULL)return;
    free(data[slot]);
    free(metadata[slot]);

    data[slot] = NULL;
    metadata[slot] = NULL;
}

void renderTab(int slot){
    printf("%s\n", metadata[slot]);
    printf("%s\n", data[slot]);
}

void viewTab(){
    unsigned long long slot = getNum("Enter Tab ID");
    if (slot < 0 || slot > MAX_TABS || metadata[slot] == NULL ||data[slot] == NULL)return;
    renderTab(slot);
}

void newTab(int reader, int writer){

    int slot = get_tab_slot();
    
    if (slot < 0){
        puts("All tabs are occupied, please close a tab");
        return;
    }else{
        printf("Using tab %d\n",slot);
    }

    char port_str[6] = {0};
    char* pos;
    request new_request = {0};
    
    printf("Enter Hostname: ");
    fgets(new_request.hostname, sizeof(new_request.hostname), stdin);
    if ((pos=strchr(new_request.hostname, '\n')) != NULL) *pos = '\0';

    printf("Enter Port: ");
    fgets(port_str, sizeof(port_str), stdin);
    if ((pos=strchr(port_str, '\n')) != NULL) *pos = '\0';
    
    new_request.port = atoi(port_str);
    new_request.slot = slot;

    data[slot] = waitmsg_data;
    metadata[slot] = waitmsg_metadata;

    msgargs reqmsg = {-1, writer, &new_request, NULL};
    put_request(&reqmsg);

    response new_response;
    msgargs respmsg = {reader, -1, NULL, &new_response};
    get_response(&respmsg);

    if (new_response.status < 0){
        data[slot] = NULL;
        metadata[slot] = NULL;
        puts("Connection failed");
        return;
    }

    while(1) if (new_response.slot == slot)break;

    char* dataptr = (char *)malloc(new_response.d_size);
    char* mdataptr = (char *)malloc(new_response.m_size);

    if  (
            (read(reader, mdataptr, new_response.m_size)!=new_response.m_size) || (read(reader, dataptr, new_response.d_size)!=new_response.d_size)
        ){
        data[slot] = NULL;
        metadata[slot] = NULL;
        puts("Connection failed");
        return;
    }

    data[slot] = dataptr;
    metadata[slot] = mdataptr;

    metadata[slot][new_response.m_size] = 0;
    data[slot][new_response.d_size] = 0;

    renderTab(slot);
}

void renderer(int reader, int writer){
    #ifndef EASYCOVID
    init_seccomp();
    #endif

    while(1){
        switch (print_menu_get_choice()){
            case 'N':
                newTab(reader, writer);
                break;
            case 'V':
                viewTab();
                break;
            case 'C':
                closeTab();
                break;
            case 'E':
                exit(EXIT_SUCCESS);
                break;
            default:
                puts("Wrong Choice");
        }
    }
}