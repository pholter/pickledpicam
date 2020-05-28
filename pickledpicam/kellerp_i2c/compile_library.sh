LIBDIR=/home/pi/pickledpicam/kellerp_i2c
# Makes a library
gcc -c -Wall -Werror -fpic read_keller_ld.c
gcc -shared -o libread_keller_ld.so read_keller_ld.o
gcc -L${LIBDIR} -Wl,-rpath=$LIBDIR -Wall -o test_read_keller test_read_keller.c -lread_keller_ld 

#export LD_LIBRARY_PATH=${LIBDIR}:$LD_LIBRARY_PATH

