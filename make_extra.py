import os
import argparse

def main(inputdir, outputdir):

	if not os.path.exists(outputdir):
		os.makedirs(outputdir)
	for filename in os.listdir(inputdir):
		inputfile = os.path.join(inputdir, filename)
		docid = os.path.splitext(filename)[0]
		outputfile = os.path.join(outputdir, filename)

		with open(outputfile,"w") as outfile:
			with open(inputfile, "r") as infile:
				outfile.write("<DOC>\n<DOCNO>"+docid+"</DOCNO>\n")
				outfile.write("<TEXT>\n")
				for line in infile:
					outfile.write(line)
				outfile.write("</TEXT>\n")
				outfile.write("</DOC>")

if __name__ == '__main__':
	# Convert the extra abstract to Indri document format
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", nargs="?")
	parser.add_argument("-o", "--output", nargs="?")

	args = parser.parse_args()

	inputdir = args.input
	outputdir = args.output

	main(inputdir, outputdir)	