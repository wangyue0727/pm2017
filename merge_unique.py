import os
import argparse

def main(inputfiles, outputfile):
	unique_id={}
	for file in inputfiles:
		with open(file, "r") as inputfile:
			for lines in inputfile:
				lines = lines.strip("\n")
				eles = lines.split()
				if eles[2] in unique_id:
					continue
				else:
					unique_id[eles[2]]=1
	with open(outputfile,"w") as outfile:
		for ids in unique_id:
			outfile.write(ids+"\n")



if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--input",nargs=4)
	parser.add_argument("-o","--output",nargs="?")

	args = parser.parse_args()
	inputfiles = args.input
	outputfile = args.output

	main(inputfiles,outputfile)
