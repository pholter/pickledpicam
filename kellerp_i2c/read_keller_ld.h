#ifndef read_keller_ld__
#define read_keller_ld__

struct keller_LD
{
  char rx[5];
  double time;
  double p;
  double T;
};
extern int open_keller_LD(void);
extern int close_keller_LD(int i2chandle);
extern int read_keller_LD(int i2chandle, struct keller_LD *sen);

#endif

