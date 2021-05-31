import sys

def convert_to_binary(value):
	bin_ = bin(value)[2:].zfill(16)
	return bin_
	
	
def main():
	NUMBER="0123456789"
	with open(sys.argv[1], 'r') as f:
		contents = f.read().splitlines()
		
	contents = [i for i in contents if i != ""]
	contents = [i for i in contents if i[0] != "/"]
	
	label=["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15", "SCREEN", "KBD", "SP", "LCL", "ARG", "THIS", "THAT"]
	value=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16384,24576,0,1,2,3,4]
	vn=16
	
	
	labelindex=0
	for i,j in enumerate(contents):
		
		if j[0]=="(":
			label.append(j[1:-1])
			value.append(str(labelindex))
		else: labelindex+=1
	for i,j in enumerate(contents):
		if j[0]=="@" and j[1] not in NUMBER:
			if j[1:] not in label:
				label.append(j[1:])
				value.append(vn)
				vn+=1
	r=0
	
	while r<len(contents):
		if contents[r][0]=="(":
			contents.remove(contents[r])
			
		else:
			r+=1
	
	
	for p,o in enumerate(contents):
		for i, j in enumerate(label):
			if contents[p]==("@"+j):
				contents[p]=contents[p].replace(j, str(value[i]))
		
	
	for i,com in enumerate(contents):
		#print(j[0])
		if com[0]=="@":
			if com[1] in NUMBER:
				number=""
				for x,y in enumerate(com):
					if com[x]!="@":
						number+=com[x]
				
				x=convert_to_binary(int(number))
				contents[i]="0"+x[1:]
			
		else:
		#1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3
		#dest=comp;jump
		#D=D+A;JEQ
			binary="1110000000000000"
			eqcode=""
			if "=" in com:
				eqindex = com.index("=")
				eqcode=com[eqindex:]
				if com[:2]=="M=":
					binary=binary[:10]+"001"+binary[13:]
				if com[:2]=="D=":
					binary=binary[:10]+"010"+binary[13:]
				if com[:3]=="MD=":
					binary=binary[:10]+"011"+binary[13:]
				if com[:2]=="A=":
					binary=binary[:10]+"100"+binary[13:]
				if com[:3]=="AM=":
					binary=binary[:10]+"101"+binary[13:]
				if com[:3]=="AD=":
					binary=binary[:10]+"110"+binary[13:]
				if com[:4]=="AMD=":
					binary=binary[:10]+"111"+binary[13:]
			if ";" in com:
				jindex = com.index(";")
				jcode=com[jindex+1:]
				#print(jcode)
				if jcode=="JGT":
					binary=binary[:13]+"001"
				if jcode=="JEQ":
					binary=binary[:13]+"010"
				if jcode=="JGE":
					binary=binary[:13]+"011"
				if jcode=="JLT":
					binary=binary[:13]+"100"
				if jcode=="JNE":
					binary=binary[:13]+"101"
				#print(jcode)
				if jcode=="JLE":
					binary=binary[:13]+"110"
					#print("something")
				if jcode=="JMP":
					binary=binary[:13]+"111"
			if ("0" in com and "=" not in com) or "0" in eqcode:
				binary=binary[:3]+"0101010"+binary[10:]
			if ("1" in com and "=" not in com) or "1" in eqcode:
				binary=binary[:3]+"0111111"+binary[10:]
			if ("-1" in com and "=" not in com) or "-1" in eqcode:
				binary=binary[:3]+"0111010"+binary[10:]
			if ("D" in com and "=" not in com) or "D" in eqcode:
				binary=binary[:3]+"0001100"+binary[10:]
			if ("A" in com and "=" not in com) or "A" in eqcode:
				binary=binary[:3]+"0110000"+binary[10:]
			if ("!A" in com and "=" not in com) or "!A" in eqcode:
				binary=binary[:3]+"0110001"+binary[10:]
			if ("-D" in com and "=" not in com) or "-D" in eqcode:
				binary=binary[:3]+"0001111"+binary[10:]
			if ("-A" in com and "=" not in com) or "-A" in eqcode:
				binary=binary[:3]+"0110011"+binary[10:]
			if ("D+1" in com and "=" not in com) or "D+1" in eqcode:
				binary=binary[:3]+"0011111"+binary[10:]
			if ("A+1" in com and "=" not in com) or "A+1" in eqcode:
				binary=binary[:3]+"0110111"+binary[10:]
			if ("D-1" in com and "=" not in com) or "D-1" in eqcode:
				binary=binary[:3]+"0001110"+binary[10:]
			if ("A-1" in com and "=" not in com) or "A-1" in eqcode:
				binary=binary[:3]+"0110010"+binary[10:]
			if ("D+A" in com and "=" not in com) or "D+A" in eqcode:
				binary=binary[:3]+"0000010"+binary[10:]
			if ("D-A" in com and "=" not in com) or "D-A" in eqcode:
				binary=binary[:3]+"0010011"+binary[10:]
			if ("A-D" in com and "=" not in com) or "A-D" in eqcode:
				binary=binary[:3]+"0000111"+binary[10:]
			if ("D&A" in com and "=" not in com) or "D&A" in eqcode:
				binary=binary[:3]+"0000000"+binary[10:]
			if ("M" in com and "=" not in com and "J" not in com) or "M" in eqcode and "J" not in eqcode:
				binary=binary[:3]+"1110000"+binary[10:]
			if ("!M" in com and "=" not in com) or "!M" in eqcode:
				binary=binary[:3]+"1110001"+binary[10:]
			if ("-M" in com and "=" not in com) or "-M" in eqcode:
				binary=binary[:3]+"1110011"+binary[10:]
			if ("M+1" in com and "=" not in com) or "M+1" in eqcode:
				binary=binary[:3]+"1110111"+binary[10:]
			if ("M-1" in com and "=" not in com) or "M-1" in eqcode:
				binary=binary[:3]+"1110010"+binary[10:]
			if ("D+M" in com and "=" not in com) or "D+M" in eqcode:
				binary=binary[:3]+"1000010"+binary[10:]
			if ("D-M" in com and "=" not in com) or "D-M" in eqcode:
				binary=binary[:3]+"1010011"+binary[10:]
			if ("M-D" in com and "=" not in com) or "M-D" in eqcode:
				binary=binary[:3]+"1000111"+binary[10:]
			if ("D&M" in com and "=" not in com) or "D&M" in eqcode:
				binary=binary[:3]+"1000000"+binary[10:]
			if ("D|M" in com and "=" not in com) or "D|M" in eqcode:
				binary=binary[:3]+"1010101"+binary[10:]
			if ("D|A" in com and "=" not in com) or "D|A" in eqcode:
				binary=binary[:3]+"0010101"+binary[10:]
			if ("!D" in com and "=" not in com) or "!D" in eqcode:
				binary=binary[:3]+"0001100"+binary[10:]
	
			contents[i]=binary
	output=""
	for command in contents:
		output+=command+"\n"
	with open("testfile.hack", "w") as f:
		f.write(output)
	
if __name__ == '__main__':
	main()


