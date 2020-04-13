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
  struct keller_LD sen;
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
   read_keller_LD(i2chandle,&sen);
   printf("Time: %f Press: %f Temp: %f\n",sen.time,sen.p,sen.T);
   printf("%x %x %x %x %x\n",sen.rx[0],sen.rx[1],sen.rx[2],sen.rx[3],sen.rx[4]);
  }
  close_keller_LD(i2chandle);

}
