#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include <math.h>

int main(int argc, char *argv[])
{
      printf("Checking the ticket ...\n");
      long long n = 0;
      if (argc == 2)
      {
            n = atol(argv[1]);
            n = -n;
            printf("n: %lld \n", n);
      }
      else
      {
            printf("wrong arguments :( \n");
            return 0;  
      }
      if (n < 100000000)
      {
            printf("nope out of range\n");
            return 0;
      }
      long long c = 2;
      long long l = (long long) sqrt(n);
      printf("l: %lld\n", l);
      for (c = 2; c <= l; c++)
      {
            if (n % c == 0)
            {
                  printf("nope wrong ticket!\n");
                  return 0;
            }
      }
      printf("yup valid ticket\n");
      return 2;
}