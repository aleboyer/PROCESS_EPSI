
//
//  main.c
//  Streaming Port
//
//  Created by Arnaud Le Boyer on 1/4/17.
//  Copyright © 2017 Arnaud Le Boyer. All rights reserved.
//

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>
#include <errno.h>

struct termios  config;

int main() {
    int fReadData; FILE *fileData;FILE *fileDatadouble;
//    const char *device = "/dev/tty.usbserial-FTYVXOH6";
    const char *device = "/dev/tty.usbserial-FTXOY2MY";
    
    uint8_t buffer;
    uint32_t biggerBuffer;
    uint8_t * buf_ptr;
    int32_t count_endian;
    
    fReadData  = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
    //   fReadData  = open(device, O_RDWR | O_NOCTTY );
    
    fileData=fopen("/Users/aleboyer/ARNAUD/SCRIPPS/SHEAR_PROBE/julia/READ_EPSILOMETER/data_c_streaming.txt","w+");
    fileDatadouble=fopen("/Users/aleboyer/ARNAUD/SCRIPPS/SHEAR_PROBE/julia/READ_EPSILOMETER/data_c_streaming_double.txt","w+");
    
    if(fReadData == -1) {
        printf( "failed to open port\n" );
    }
    else{
        printf( "fd = %i\n",fReadData );
    }
    
    if(!isatty(fReadData)) {printf(" fd is not a tty ");}
    else{
        printf(" fd is a tty \n");
    };
    
    
    if(tcgetattr(fReadData, &config) < 0) { printf(" no tty configuration");}
    else{
        printf("config.c_iflag=%lx\n",config.c_iflag);
        printf("config.c_oflag=%lx\n",config.c_oflag);
        printf("config.c_cflag=%lx\n",config.c_cflag);
        printf("config.c_lflag=%lx\n",config.c_lflag);
        printf("config.c_ispeed=%lx\n",config.c_ispeed);
        printf("config.c_ospeed=%lx\n",config.c_ospeed);
    }
    
    config.c_lflag &= ICANON ;
    config.c_cc[VMIN]  = 1;
    config.c_cc[VTIME] = 0;
    
    printf("config.c_lflag=%lx\n",config.c_lflag);
    printf("config.c_cflag=%lx\n",config.c_cflag);
    
    
    if(config.c_ispeed != B115200 || config.c_ispeed != B115200) {
        printf(" baud rate is not 115200\n");
        config.c_ispeed = B115200;
        config.c_ospeed = B115200;
        printf("config.c_ispeed=%lx\n",config.c_ispeed);
        printf("config.c_ospeed=%lx\n",config.c_ospeed);
        printf(" now baud rate is 115200\n");
        
        
    }
    else{
        printf(" baud rate is 115200\n");
    }
    
    //the configuration is changed any data received and not read will be discarded.
    tcsetattr(fReadData, TCSAFLUSH, &config);

    
    biggerBuffer=0;
    while(1){
        if (read(fReadData,&buffer,1)>0){
           if (buffer==0x1e){
                printf("coucou");
                buf_ptr= (uint8_t*) &biggerBuffer;
                biggerBuffer=0;
                count_endian=2;
                // the port is open as non block
                // we nee a while to hang in the loop until the new bye can be read
                while(count_endian>=0){
                    if (read(fReadData,&buffer,1)>0){
                         buf_ptr[count_endian] = buffer;
                        printf("streaming data : 0x%02x\n",buffer);  // screen print
                        printf("streaming data : 0x%08x\n",biggerBuffer);  // screen print
                        count_endian--;
                    }
                }
                fprintf(fileData,"0x%08x\n",biggerBuffer);  // file print
                fprintf(fileDatadouble,"%d\n",biggerBuffer);  // file print
                fflush(fileData);
                fflush(fileDatadouble);
            }
        }
    }
}
