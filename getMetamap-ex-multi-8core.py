import os
import subprocess
import re
import nltk
import argparse
import multiprocessing

def main(did, conceptdir):

	if not os.path.exists(conceptdir):
		os.makedirs(conceptdir)

	args = ['ls', conceptdir]
	args2 = ['wc','-l']
	process_echo = subprocess.Popen(args,stdout=subprocess.PIPE)
	process_metamap = subprocess.Popen(args2,stdin=process_echo.stdout,stdout=subprocess.PIPE, shell=False)
	output = process_metamap.stdout
	for count in output:

		print str(count.strip()) + " files has been done"

	inputdir = "/infolab/headnode/yuewang/PM/collection/extra_abstracts_clean/"
	# inputfile = os.path.join(inputdir, did + ".txt")
	# conceptfile = os.path.join(conceptdir, did + ".txt")
	inputfile = os.path.join(inputdir, did)
	conceptfile = os.path.join(conceptdir, did)

	with open(inputfile,"r") as infile:
		with open(conceptfile,"w") as confile:
			content=""
			for line in infile:
				line = line.strip()
				if line == "<DOC>" or line == "<TEXT>"  or line == "</DOC>":
					confile.write(line+"\n")
				elif "<DOCNO>" in line:
					confile.write(line+"\n")
				elif line == "</TEXT>":
					cuis = call_metamap(content)
					confile.write(cuis+"\n")
					confile.write("</TEXT>\n")
				else:
					content += line


def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def call_metamap(content):
	
	all_num = re.compile("^\d+$")

	cuis=""

	lines = content.split("\n")
	for line in lines:
		line = line.strip()
		if not all_num.match(line) and len(line) > 2:
			sent_text = nltk.sent_tokenize(line.decode('utf-8'))
			for sentence in sent_text: 
				if is_ascii(sentence):
					args = ['echo', sentence]
					args2 = ['/local/data/yuewang/MedTrack/UMLS_MetaMap/public_mm/bin/metamap11v2','-I']
					process_echo = subprocess.Popen(args,stdout=subprocess.PIPE)
					process_metamap = subprocess.Popen(args2,stdin=process_echo.stdout,stdout=subprocess.PIPE, shell=False)
					output = process_metamap.stdout
					pattern = re.compile("^C\d{7}")
					for line in output:
						if line.startswith("Meta Candidates"):
							candidates = True
							mapping = False
							continue
						elif line.startswith("Meta Mapping"):
							candidates = False
							mapping = True
							continue
						elif line.startswith("/local"):
							candidates = False
							mapping = False
							continue

						if candidates:
							line = line.strip()
							temp = line.split(":")
							temp = temp[0].split()
							if len(temp) == 2 and pattern.match(temp[1]):
								cuis += temp[1] + " "
	return cuis




if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", nargs='?', 
						help="Input file contains docid. ")
	parser.add_argument("-o", "--output", nargs='?', 
						 help="Output dir for text rep")
	args = parser.parse_args()	

	inputfile = args.input
	outputdir = args.output

	pool = multiprocessing.Pool(processes=8)

	with open(inputfile,"r") as infile:
		for line in infile:
			did = line.strip()
			# main(did, outputdir)
			pool.apply_async(main,(did, outputdir,))
	pool.close()
	pool.join()
