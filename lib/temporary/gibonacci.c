#include <stdio.h>

#define ARRAY_SIZE(arr) (sizeof(arr)/sizeof(arr[0]))
int *calculateGibbonacci(int init[],int n){
	int gibbo[n];
	int i;
	int p = ARRAY_SIZE(init);
	printf("point 1\n");
	for(i = 0; i < p; ++i){
		gibbo[i] = init[i];
	}
	printf("point 2\n");
	for(i = p; i < n; ++i){
		gibbo[i] = sum(gibbo,i-p,i-1);
	}
	return gibbo;
}

int sum(int arr[],int startPos, int endPos){
	int result = 0;
	register int i;
	printf("point 3\n");
	for(i = startPos; i < endPos; ++i){
		result = result + arr[i];
	}
	return result;
}

