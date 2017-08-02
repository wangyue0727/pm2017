import os
import subprocess
import re
import nltk
import argparse

def main(inputdir,outputdir):
	for filename in os.listdir(inputdir):
		inputfile = os.path.join(inputdir, filename)
		outputfile = os.path.join(outputdir, filename)
		with open(outputfile, "w") as outfile:
			with open(inputfile, "r") as infile:
				content=""
				for line in infile:
					if "<PubmedArticle>" in line:
						content = line
					elif "</PubmedArticle>" in line:
						content += line
						docid,text = parse_doc(content)
						outfile.write("<DOC>\n")
						outfile.write("<DOCNO>" + docid + "</DOCNO>\n")
						outfile.write("<TEXT>\n")
						outfile.write(text + "\n")
						outfile.write("</TEXT>\n</DOC>\n\n")

					else:
						content += line

def parse_doc(content):
	parsed = ""
	found_id = False
	lines = content.split("\n")
	for line in lines:
		if not found_id:
			if "PMID" in line:
				docid = re.sub(r'\<.*?\>',' ',line)
				docid = docid.strip()
				found_id = True
		line = re.sub(r'\<.*?\>',' ',line)
		if line.strip():
			parsed += line + "\n"
	return docid, parsed

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", nargs='?', 
						help="Input dir that contains xml files. ")
	parser.add_argument("-o", "--output", nargs='?', 
						 help="Output dir for text rep")
	args = parser.parse_args()	

	inputdir = args.input
	outputdir = args.output

	main(inputdir,outputdir)