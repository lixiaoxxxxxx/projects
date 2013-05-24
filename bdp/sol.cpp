#include <iostream>
using namespace std;

unsigned int BKDRHash(char *str){
    unsigned int seed = 131; // 31 131 1313 13131 131313 etc..
    unsigned int hash = 0;

    while (*str){
        hash = hash * seed + (*str++);
    }
    return (hash & 0x7FFFFFFF) % 1024;
}


int main(){
	char a[] = "fuck you";
	char b[] = "fuck me";
	cout << BKDRHash(a) << endl;
	cout << BKDRHash(b) << endl;
	return 0;
}
