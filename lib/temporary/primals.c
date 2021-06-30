#include <stdio.h>

int * calculatePrimes(int n){
	static int primes[200];
	primes[0] = 2;
	int numberPrimes = 1;
	int number = 3;
	
	printf("point 5\n");
	while(numberPrimes < n){
		if(isPrime(number,primes,numberPrimes)){
			primes[numberPrimes] = number;
			++numberPrimes;
		}
		number = number + 2;
	}
	return primes;
}

int isPrime(int number, int knownPrimes[], int numberPrimes){
	register int i;
	printf("point 6\n");
	for(i = 0; (i < numberPrimes) && (number*number >= knownPrimes[i]);++i){
		if(number % knownPrimes[i] == 0)
			return 0;
	}
	return 1;
}