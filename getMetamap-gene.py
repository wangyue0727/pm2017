import os
import subprocess
import re
import nltk
import argparse
from lxml import etree
import string

def main(inputfile,outputfile):
	with open(outputfile, "w") as outfile:
		with open(inputfile, "r") as infile:
			queries = read_input(inputfile)
			keylist = queries.keys()
			keylist.sort()	
			outfile.write("<topics task=\"2017 TREC Precision Medicine\">\n")

			for query in keylist:
				outfile.write("<topic number=\""+str(query)+"\">")
				outfile.write("<disease>")
				outfile.write(call_metamap(queries[query]["disease"]))
				outfile.write("</disease>\n")
				outfile.write("<gene>")
				outfile.write(call_metamap(queries[query]["gene"]))
				outfile.write("</gene>\n")
				outfile.write("<demographic>")
				outfile.write(call_metamap(queries[query]["demographic"]))
				outfile.write("</demographic>\n")
				outfile.write("<other>")
				outfile.write(call_metamap(queries[query]["other"]))
				outfile.write("</other>\n")	
				outfile.write("</topic>\n")			
			outfile.write("</topics>\n")
			# content=""
			# for line in infile:
			# 	if "<text>" in line:
			# 		content = line
				
			# 		text = parse_doc(content)
			# 		cuis = call_metamap(text)
			# 		outfile.write("<text>#combine(" + cuis + ")</text>\n")
			# 	else:
			# 		outfile.write(line)


def read_input(inputfile):
	queries={}
	with open(inputfile) as infile:
		for line in infile:
			lines =line + line.strip("\n")
	tree = etree.parse(inputfile)
	root = tree.getroot()
	for topics in root:
		q_id = topics.attrib["number"]
		# q_type = topics.attrib["type"]

		for items in topics:
			table = string.maketrans("","")
			items.text = items.text.translate(table, string.punctuation)
			if items.tag == "disease":
				disease = items.text
			if items.tag == "gene":
				gene = items.text
			if items.tag == "demographic":
				demographic = items.text
			if items.tag == "other":
				other = items.text
				if other == "None":
					other = ""
		query={}
		q_disease = disease
		q_gene = gene
		q_demographic=demographic
		q_other = other

		query["qid"]=q_id

		query["disease"] = q_disease
		query["gene"] = q_gene
		query["demographic"]=q_demographic
		query["other"]=q_other
		queries[int(q_id)]=query
	return queries

def parse_doc(content):
	parsed = ""
	lines = content.split("\n")
	for line in lines:
		line = re.sub(r'\<.*?\>',' ',line)
		line = re.sub(r'#combine\(',' ',line)
		line = re.sub(r'\)',' ',line)
		if line.strip():
			parsed += line + "\n"
	return parsed
		# print "+++++" + line

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def call_metamap(content):
	
	all_num = re.compile("^\d+$")

	cuis=""

	lines = content.split("\n")
	for line in lines:
		line = line.strip()
		if not all_num.match(line) and len(line) > 2:
			sent_text = nltk.sent_tokenize(line)
			for sentence in sent_text: 
				if is_ascii(sentence):
					args = ['echo', sentence]
					args2 = ['/infolab/node4/callejas/UMLS_MetaMap/public_mm/bin/metamap11v2','-I']
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
						elif line.startswith("/infolab"):
							candidates = False
							mapping = False
							continue

						# if mapping:
						# 	line = line.strip()
						# 	temp = line.split(":")
						# 	temp = temp[0].split()
						# 	if len(temp) == 2 and pattern.match(temp[1]):
						# 		cuis += temp[1] + " "							

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
						help="Input query file. ")
	parser.add_argument("-o", "--output", nargs='?', 
						 help="Output query file")
	args = parser.parse_args()	

	input_file = args.input
	output_file = args.output

	main(input_file,output_file)