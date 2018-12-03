#include <vector>
#include <cstdlib>
#include <iostream>

using namespace std;


class synTable{
	public:
		synTable();
		synTable(int, int, int,vector<double>, vector<double>);

		void set_All(int len, int midiNumber, int vol);
		void set_volume_level(int vol);
		void set_midiNoteNumber(int number);
		void set_length(int len);
		int get_midiNoteNumber();
		int get_length();
		void set_coef(vector<double>, int);
		vector<double> load_A();
		vector<double> load_B();
	private:
		int midiNoteNumber;
		int length;
		int vol_level;
		vector<double> A_coef;
		vector<double> B_coef;
};

