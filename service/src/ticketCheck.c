#include <stdlib.h>
#include <stdio.h>
 
int main(int argc,char* argv[]) 
{
	int n = 0;
	if(argc == 2){
		n = atoi(argv[1]);
		
	}else{
		return 0;
	}
	
	if (n < 999 || n > 9999){
		return 0;
	}
   int c = 2;
    
   for ( c = 2 ; c <= n - 1 ; c++ )
   {
      if ( n%c == 0 )
      {
         printf("%d isn't prime.\n", n);
     break;
      }
   }
   if ( c == n )
      return 1;
  
       
   return 0;
}