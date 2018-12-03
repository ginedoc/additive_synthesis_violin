#include "load_coef.h"

synTable::synTable(){

}

synTable::synTable(int len, int midiNumber,int vol_level, vector<double> A, vector<double> B){
	midiNoteNumber = midiNumber;
	length = len;

	A_coef = A;
	B_coef = B;
}


void synTable::set_midiNoteNumber(int number){
	midiNoteNumber = number;
}

void synTable::set_length(int len){
	length = len;
}

int synTable::get_midiNoteNumber(){
	return midiNoteNumber;	
}

int synTable::get_length(){
	return length;
}

vector<double> synTable::load_A(){
	return A_coef;
}

vector<double> synTable::load_B(){
	return B_coef;
}

void synTable::set_volume_level(int vol){
	vol_level = vol;
}

void synTable::set_All(int len, int midiNumber, int vol){
	set_volume_level(len);
	set_midiNoteNumber(midiNumber);
	set_length(len);
}

void synTable::set_coef(vector<double> coef, int num){
	//num:0 ->A
	//num:1 ->B
	if(num==0){
		A_coef.resize(coef.size());
		A_coef.assign(coef.begin(), coef.end());
	}
	else if(num==1){
		B_coef.resize(coef.size());
		B_coef.assign(coef.begin(), coef.end());
	}

}
