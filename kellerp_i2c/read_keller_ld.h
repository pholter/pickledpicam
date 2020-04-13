#ifndef read_keller_ld__
#define read_keller_ld__

extern int open_keller_LD(void);
extern int close_keller_LD(int i2chandle);
extern int read_keller_LD(int i2chandle, char *retrx, double *retp, double *retT, double *rettime);

#endif

