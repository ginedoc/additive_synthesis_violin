#include "load_coef.h"
#include <fstream>

using namespace std;

int main(){
	ifstream info, Af, Bf;
	info.open("../info.pkl", ios::in);
	Af.open("../A_coef.pkl", ios::in|ios::binary);
	Bf.open("../B_coef.pkl", ios::in|ios::binary);

	int vol_level = 5;
	synTable table[64][vol_level];
	int length;
	int midiNummer;
	vector<double> A; 
	vector<double> B;
	

	for (int i=0; i<64; i++){
		info >> length;
		midiNummer = i+55;
		A.resize(length);
		B.resize(length);
		
		for(int j=0; j<vol_level; j++){	
			table[i][j].set_All(length, midiNummer, j);
		
			float a[length];
			float b[length];
			Af.read((char*)&a, sizeof(a));
			Bf.read((char*)&a, sizeof(b));
			A.assign(a, a+length);
			B.assign(b, b+length);


			table[i][j].set_coef(A,0);
			table[i][j].set_coef(B,1);

		}
		
	}

	for(int i=0;i<table[0][0].get_length();i++){
		cout << table[0][0].load_A()[i] << endl;
	}

	info.close();
	Af.close();
	Bf.close();

}
