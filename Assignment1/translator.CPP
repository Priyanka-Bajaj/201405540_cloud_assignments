#include<iostream>
#include<stdio.h>
#include<map>
#include<string>
#include<fstream>

using namespace std;

int main(){
	map<string,string> mapping;
	mapping["pushl	%ebp"]="pushq	%rbp";
	mapping[".cfi_def_cfa_offset 8"]=".cfi_def_cfa_offset 16";
	mapping[".cfi_offset 5, -8"]=".cfi_offset 6, -16";
	mapping["movl	%esp, %ebp"]="movq	%rsp, %rbp";
	mapping[".cfi_def_cfa_register 5"]=".cfi_def_cfa_register 6";
	mapping["andl	$-16, %esp"]="";
	mapping["subl	$16, %esp"]="";
	mapping["movl	$.LC0, (%esp)"]="movl	$.LC0, %edi";
	mapping["leave"]="popq	%rbp";
	mapping[".cfi_restore 5"]="";
	mapping[".cfi_def_cfa 4, 4"]=".cfi_def_cfa 7, 8";
	ifstream input_asm_file("32_bit.s");
	string line;
 	if(input_asm_file.is_open())
	{
		while(getline(input_asm_file,line))
		{
			int i;

			for(i=0;i<line.length();i++)
			{
				if(!isspace(line[i]))
					break;
			}
			line=line.substr(i,line.length()-i);
			if((mapping.find(line)!=mapping.end()))
			{
				if(mapping[line]!="")
					cout<<mapping[line]<<endl;

			}
			else
				cout<<line<<endl;
		}
	}
	input_asm_file.close();
	return 0;
}
