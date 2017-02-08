//
//  main.c
//  Streamingport tuto
//
//  Created by Arnaud Le Boyer on 1/5/17.
//  Copyright © 2017 Arnaud Le Boyer. All rights reserved.
//


// following en.wikibooks.org/wiki/Serial_Programming/termios

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>
#include <errno.h>

struct termios  config;

int main() {
    int fd;
    const char *device = "/dev/tty.usbserial-FTXOY2MY";
    int compt=0;
    uint8_t buffer;
    uint8_t cr=0x13;
    
    fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
    if(fd == -1) {
        printf( "failed to open port\n" );
        }
    else{
        printf( "fd = %i\n",fd );
    }
    
    if(!isatty(fd)) {printf(" fd is not a tty ");}
    else{
        printf(" fd is a tty \n");
    };
    
    
    if(tcgetattr(fd, &config) < 0) { printf(" no tty configuration");}
    else{
        printf("config.c_iflag=%lx\n",config.c_iflag);
        printf("config.c_oflag=%lx\n",config.c_oflag);
        printf("config.c_cflag=%lx\n",config.c_cflag);
        printf("config.c_lflag=%lx\n",config.c_lflag);
        printf("config.c_ispeed=%lx\n",config.c_ispeed);
        printf("config.c_ospeed=%lx\n",config.c_ospeed);
    }
    
    //config.c_lflag &= ~(ECHO | ECHONL | ICANON | IEXTEN | ISIG);
    //config.c_cflag &= ~(CSIZE | PARENB);
    //config.c_cflag |= CS8;
    
    //TODO
    
    config.c_cc[VMIN]  = 1;
    config.c_cc[VTIME] = 0;
    
    
    if(config.c_ispeed == B9600 || config.c_ispeed == B9600) {
        printf(" baud rate is not 115200\n");
        config.c_ispeed = B115200;
        config.c_ospeed = B115200;
        
    }
    else{
        printf(" baud rate is 115200\n");
    }
    printf("config.c_ispeed=%lx\n",config.c_ispeed);
    printf("config.c_ospeed=%lx\n",config.c_ospeed);

//the configuration is changed any data received and not read will be discarded.
    tcsetattr(fd, TCSAFLUSH, &config);
    printf("config.c_ospeed=%lx\n",config.c_ospeed);
    while(1){
        if (read(fd,&buffer,1)>0){
            write(STDOUT_FILENO,&buffer,1);
            write(STDOUT_FILENO,&cr,1);
            printf("streaming data : %x\n",buffer);
            printf("compt = %i\n", compt);
            compt++;
    }
    //close(fd);
    
    //return (0);
}
