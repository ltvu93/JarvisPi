import sys

def main(filename):
	d = {}
	arr = []
	with open(filename) as f:
		lines = f.readlines()
		for line in lines:
			line = line.replace(" ", "_")
			#print line
			
			(key, val) = line.split()
			d[str(key)] = val
	for key,val in d.items():
		results = val.split("_")
		for result in results:
			if result not in arr:
				arr.append(result)
	arr.append(str("SIL"))
	arr.sort()
	fout = open("jarvispi.phone", "w")
	for item in arr:
		fout.write(item)
		fout.write("\n")
#	fout.write("\n")
	fout.close()

if __name__ == "__main__":
	main(sys.argv[1])
