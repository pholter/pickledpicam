#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include "read_keller_ld.h"

int open_keller_LD(void)
{
  char devpath[11];
  printf("Opening I2C device\n");
  sprintf(devpath,"/dev/i2c-1");
  int i2chandle = open(devpath,O_RDWR);
  return i2chandle;
}

int close_keller_LD(int i2chandle)
{
    close(i2chandle);
    return 0;
}


int read_keller_LD(int i2chandle, char *retrx, double *retp, double *retT, double *rettime)
{
  struct timespec ts_10ms;
  struct timeval sampletime;
  double stime;
  float sen_range_up = 30; // 30 bar sensor
  float sen_range_low = 00;
  int bar_raw;
  float bar;
  int i;
  int T_raw;
  float T;
  char rxbuffer[50];
  char conv_cmd[1];  
  char status;
  conv_cmd[0] = 0xAC;  
  ts_10ms.tv_sec = 0;
  ts_10ms.tv_nsec = 10 * 1000000;

  gettimeofday(&sampletime,NULL);  
  int opresult = ioctl(i2chandle,I2C_SLAVE, 0x40);  
  opresult = write(i2chandle,conv_cmd,1);
  nanosleep(&ts_10ms,&ts_10ms);
  opresult = read(i2chandle,rxbuffer,5);
  // TODO check for error
  if(opresult)
    {}
  //printf("%x %x %x %x %x\n",rxbuffer[0],rxbuffer[1],rxbuffer[2],rxbuffer[3],rxbuffer[4]);

  status = rxbuffer[0];
  bar_raw = rxbuffer[2] + rxbuffer[1] * 256;
  bar = (bar_raw - 16384) * (sen_range_up - sen_range_low)/32768 + sen_range_low;
  //stime = sampletime.tv_sec + sampletime.tv_usec / 1000000;
  stime = (double) sampletime.tv_sec + ((double) sampletime.tv_usec) / 1000000;
  //printf("Time: %ld %ld\n",sampletime.tv_sec,sampletime.tv_usec);   
  printf("Time: %f Bar raw: %d Bar: %f\n",stime,bar_raw,bar);   
  T_raw = rxbuffer[4] + rxbuffer[3] * 256;
  T = (T_raw/16 - 24) * 0.05 - 50;
  *retT = T;
  *retp = bar;
  *rettime = stime;
  for (i=0;i<5;i++)
    retrx[i] = rxbuffer[i];
  //printf("T raw: %d T: %f\n",T_raw,T);
  return (int) status;
}

