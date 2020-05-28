#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include "read_keller_ld.h"

int main(void)
{
  int i;
  char devpath[11];
  double p,T,stime;
  char rx[5];
  struct timespec ts;
  ts.tv_sec = 0;
  ts.tv_nsec = 500 * 1000000;
  
  printf("Opening I2C device\n");
  sprintf(devpath,"/dev/i2c-1");
  int i2chandle = open_keller_LD();

  for(i=0;i<500000;i++)
  {
   printf("Hallo %d\n",i);
   nanosleep(&ts,&ts);
   read_keller_LD(i2chandle,rx,&p,&T,&stime);
   //extern int read_keller_LD(int i2chandle, char *retrx, double retp, double retT, double rettime);
   printf("Time: %f Press: %f Temp: %f\n",stime,p,T);
   printf("%x %x %x %x %x\n",rx[0],rx[1],rx[2],rx[3],rx[4]);
  }
  close_keller_LD(i2chandle);

}
