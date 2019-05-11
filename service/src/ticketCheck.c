#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
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
      if (n < 10000000000)
      {
            printf("nope out of range\n");
            return 0;
      }
      long long c = 2;

      for (c = 2; c <= n - 1; c++)
      {
            if (n % c == 0)
            {
                  break;
            }
      }
      if (c == n)
      {
            printf("yup valid ticket\n");
            return 1;
      }
      printf("nope wrong ticket!\n");

      return 0;
}