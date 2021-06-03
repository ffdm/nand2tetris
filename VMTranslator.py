
import sys



# vm to hack assembly language translator
# usage: python VMTranslator.py inputfile.vm
# outputs in same dir: inputfile.asm        


#opens file and isolates content
def parser():

	#read file
	with open(sys.argv[1], 'r') as f:
		lines = f.readlines()
		
	#remove comments
	for i, line in enumerate(lines):
		if line.find("//")!=-1:
			line=line[:line.index("//")]
		lines[i]=line.strip()
		
	#remove blank lines
	lines = list(filter(None, lines))
	
	return lines
	
def codewriter(lines):
	tl=""
	
	#label counter
	lc=0
	
	for i, line in enumerate(lines):
		
			
		#split line by spaces
		line=line.split(" ")
			
		#translate push command
		if line[0] == "push":
			if line[1]=="static":
				tl+= f"\n//push static {line[2]}\n@Xxx.{line[2]}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			elif line[1]=="temp":
				tl+= f"\n//push temp {line[2]}\n@{line[2]}\nD=A\n@5\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			elif line[1]=="pointer":
				tl+= f"\n//push pointer {line[2]}\n@{line[2]}\nD=A\n@3\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			elif line[1]=="local":
				tl+= f"\n//push local {line[2]}\n@{line[2]}\nD=A\n@LCL\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			elif line[1]=="argument":
				tl+= f"\n//push argument {line[2]}\n@{line[2]}\nD=A\n@ARG\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			elif line[1]=="this":
				tl+= f"\n//push this {line[2]}\n@{line[2]}\nD=A\n@THIS\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			elif line[1]=="that":
				tl+= f"\n//push that {line[2]}\n@{line[2]}\nD=A\n@THAT\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			elif line[1]=="constant":
				tl+= f"\n//push constant {line[2]}\n@{line[2]}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
				
		#translate pop command
		elif line[0] == "pop":
			if line[1]=="static":
				tl+=f"\n//pop static {line[2]}\n@SP\nM=M-1\nA=M\nD=M\n@Xxx.{line[2]}\nM=D\n"
			elif line[1]=="temp":
				tl+=f"\n//pop temp {line[2]}\n@SP\nM=M-1\nA=M\nD=M\n@{int(line[2])+5}\nM=D\n"
			elif line[1]=="pointer":
				tl+=f"\n//pop pointer {line[2]}\n@SP\nM=M-1\nA=M\nD=M\n@{int(line[2])+3}\nM=D\n"
			elif line[1]=="local":
				tl+=f"\n//pop local {line[2]}\n@{line[2]}\nD=A\n@LCL\nA=M\nD=D+A\n@LCL\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@LCL\nA=M\nM=D\n@{line[2]}\nD=A\n@LCL\nA=M\nD=A-D\n@LCL\nM=D\n"
			elif line[1]=="argument":
				tl+=f"\n//pop argument {line[2]}\n@{line[2]}\nD=A\n@ARG\nA=M\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
			elif line[1]=="this":
				tl+=f"\n//pop this {line[2]}\n@{line[2]}\nD=A\n@THIS\nA=M\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
			elif line[1]=="that":
				tl+=f"\n//pop that {line[2]}\n@{line[2]}\nD=A\n@THAT\nA=M\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
		
		#add
		elif line[0] == "add":
			tl+=f"\n//add\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M\n"
			
		#sub
		elif line[0] == "sub":
			tl+=f"\n//sub\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\n"
			
		#neg
		elif line[0] == "neg":
			tl+=f"\n//neg\n@SP\nA=M-1\nM=-M\n"
		
		#and
		elif line[0] == "and":
			tl+=f"\n//and\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M&D\n"
			
		#or
		elif line[0] == "or":
			tl+=f"\n//or\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M|D\n"
			
		#not
		elif line[0] == "not":
			tl+=f"\n//not\n@SP\nA=M-1\nM=!M"
			
		#eq
		elif line[0] == "eq":
			tl+=f"\n//eq\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D-M\nD=M\n@eq.true.{lc}\nD;JEQ\n@SP\nA=M-1\nM=0\n@eq.after.{lc}\n0;JMP\n(eq.true.{lc})\n@SP\nA=M-1\nM=-1\n(eq.after.{lc})\n"
			lc+=1
			
		#gt
		elif line[0] == "gt":
			tl+=f"\n//gt\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D-M\nD=M\n@gt.true.{lc}\nD;JGT\n@SP\nA=M-1\nM=0\n@gt.after.{lc}\n0;JMP\n(gt.true.{lc})\n@SP\nA=M-1\nM=-1\n(gt.after.{lc})\n"
			lc+=1
		#gt
		elif line[0] == "gt":
			tl+=f"\n//lt\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D-M\nD=M\n@lt.true.{lc}\nD;JLT\n@SP\nA=M-1\nM=0\n@lt.after.{lc}\n0;JMP\n(lt.true.{lc})\n@SP\nA=M-1\nM=-1\n(lt.after.{lc})\n"
			lc+=1
	
	return tl+"\n(END)\n@END\n0;JMP"

def main():
	lines=parser()
	output=codewriter(lines)
	
	with open(f"{sys.argv[1][:-3]}.asm", "w") as f:
		f.write(output)
	
	
if __name__ == "__main__":
    # execute only if run as a script
    main()
