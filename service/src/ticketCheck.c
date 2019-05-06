#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
int main(int argc,char* argv[]) 
{
   printf("start checking!");
	int n = 0;
	if(argc == 2){
		n = atoi(argv[1]);
      n = -n;
		
	}else{
		return 0;
      printf("nope");
	}
	printf("%d",INT_MAX );
	if (n > INT_MAX || n < 99999999){
            printf("nope out of range");

		return 0;
	}
   int c = 2;
    
   for ( c = 2 ; c <= n - 1 ; c++ )
   {
      if ( n%c == 0 )
      {

         printf("nope! can be devided");
     break;
      }
   }
   if ( c == n ){
            printf("yup");

      return 1;
   }
                printf("nope!");

   return 0;
}