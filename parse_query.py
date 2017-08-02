from sys import argv
from lxml import etree
import xml.etree.ElementTree as ET
import re
import string
import io
import traceback
import os

queries={}


def main():
	if len(argv) != 3:
		print "python makequery.py xml_query output_query_file"
	else:
		try:
			inputfile = argv[1]
			outputfile = argv[2]
			if os.path.exists(outputfile):
				os.remove(outputfile)
			read_input(inputfile)
			gen_output(outputfile)
		except Exception as inst:
			print "There is an error: "
			print traceback.print_exc()

def gen_output(outputfile):
	global queries

	keylist = queries.keys()
	keylist.sort()
	# for query in keylist:
		# filename=outputfile+queries[query]["qid"]
		# try:
		# 	file = open(filename, "w")
		# 	file.write(queries[query]["description"]+"\n")
		# except Exception as inst:
		# 	print "there is error: "
		# 	print traceback.print_exc()
	try:
		file = open(outputfile, "w")
		# file.write("<parameters>\n")
		# file.write("<index>/local/headnode2/yuewang/MedTrack/2016CDS/index/2016term</index>\n")
		# file.write("<count>1000</count>\n")
		# file.write("<trecFormat>true</trecFormat>\n")
		# file.write("<runID>UDelInfoCDS5</runID>\n")
		keylist = queries.keys()
		keylist.sort()
		for query in keylist:
			file.write(queries[query]["gene"]+"\n")
		# 	file.write("<query>\n")
		# 	file.write("<number>"+queries[query]["qid"]+"</number>\n")
		# 	table = string.maketrans("","")
		# 	summary = queries[query]["summary"]
		# 	summary = summary.translate(table, string.punctuation)
		# 	file.write("<text>#combine("+summary+")</text>\n")
		# 	file.write("</query>\n")
		# file.write("</parameters>\n")	

	except Exception as inst:
		print  "There is an error: "
		print traceback.print_exc()


def read_input(inputfile):
	global queries
	with open(inputfile) as infile:
		for line in infile:
			lines =line + line.strip("\n")
	tree = etree.parse(inputfile)
	root = tree.getroot()
	for topics in root:
		q_id = topics.attrib["number"]
		# q_type = topics.attrib["type"]

		for items in topics:
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

if __name__ == '__main__':
	main()