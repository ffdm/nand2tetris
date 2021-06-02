
import sys

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
	
	
	print(lines)
	
def codewriter:
	pass

def main():
	parser()
	
if __name__ == "__main__":
    # execute only if run as a script
    main()