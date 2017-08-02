import json
import os
import argparse
import regex as re
from lxml import etree
import string

def main():
	orig_query = "../query/topics2017.xml"
	concept = "../query/topics2017-concept.xml"
	
	# index = "/local/data/yuewang/PM/index/ct_term/"
	# index = "/local/data/yuewang/PM/index/sa_term/"
	# queries=read_input(orig_query)
	# keylist = queries.keys()
	# keylist.sort()	
	# index = "/local/data/yuewang/PM/index/ct_concept/"
	index = "/local/data/yuewang/PM/index/sa_concept/"
	queries = read_input(concept)
	keylist = queries.keys()
	keylist.sort()		

	runid = "UDelInfoPMSA6"

	query_dir = "../query/official/"
	if not os.path.isdir(query_dir):
		os.makedirs(query_dir)
	outfile = os.path.join(query_dir,runid+".txt")

	if os.path.isfile(outfile):
		cont = raw_input(runid+" output file exists. Continue?  ")
		if not cont == "y":
			print "Exiting the system..."
			exit()
		else:
			print "Existing file "+runid+" will be overwritten!"
	alias, summary = load_alias_summary()
	
	with open(outfile,"w") as out:
		out.write("<parameters>\n")
		out.write("<index>"+index+"</index>\n")
		out.write("<count>1000</count>\n")
		out.write("<trecFormat>true</trecFormat>\n")
		out.write("<runID>"+runid+"</runID>\n")		

		for query in keylist:

			# demo = queries[query]["demographic"]
			# age, gender = demo.split()
			# age=re.sub(r'yearold','',age)
			# print age, gender
			out.write("<query>\n")
			out.write("<number>"+queries[query]["qid"]+"</number>\n")
			out.write("<text>")
			

			# out.write("#filreq(")

			# out.write(" #band(#greater(max_age "+age+") #less(min_age "+age+"))")

			# out.write(" #weight(")
			out.write(" #combine(")
			# out.write("0.8 #combine(")
			# for term in queries[query]["disease"].split():
			# 	out.write(term+".exclusion ")
			# for term in queries[query]["gene"].split():
			# 	out.write(term+".exclusion ")
			# interested_fields=["detailed_description", "inclusion", "keyword", "condition_browse", "intervention_browse"]
			# for term in queries[query]["disease"].split():
			# 	for field in interested_fields:
			# 		out.write(term+"."+field+" ")
			# for term in queries[query]["gene"].split():
			# 	for field in interested_fields:
			# 		out.write(term+"."+field+" ")
			# for term in queries[query]["other"].split():
			# 	for field in interested_fields:
			# 		out.write(term+"."+field+" ")	
			# out.write(" 0.5 #combine(")
			out.write(queries[query]["disease"]+" ")
			# out.write(")")
			# if not queries[query]["gene"]  == "":
			# 	out.write(" 0.3 #combine(")
			out.write(queries[query]["gene"]+" ")
			# 	out.write(")")
			# if not queries[query]["other"]  == "":
			# 	out.write(" 0.2 #combine(")
			# 	out.write(queries[query]["other"])
			# 	out.write(")")
			# out.write(" "+gender+".gender")
			
			# out.write(")") #right parathesis for 0.8 combine
			
			# out.write(" 0.2 #combine(")
			# for gene in queries[query]["gene"].split():
			# 	if gene == "EML4ALK":
			# 		gene = "EML4"
			# 	if gene in alias:
			# 		for key in alias[gene]:
			# 			# print key
			# 			key=re.sub(ur"\p{P}+", " ", key)
			# 			key = re.sub(ur"\+", " ",key)
			# 			# print key
			# 			out.write(" #1("+key+")")
			# out.write(")")
			
			# out.write(")") #right parathesis for combine
			out.write(")") #right parathesis for weight

			# out.write(")") #right parathesis for filreq
			
			out.write("</text>\n")
			out.write("</query>\n")
		out.write("</parameters>\n")

def load_alias_summary():
	alias_dir = "gene-expansion/alias/"
	alias={}
	for file in os.listdir(alias_dir):
		with open(os.path.join(alias_dir,file)) as infile:
			gene=re.sub(r'-alias.json','',file)
			alias[gene]=json.load(infile)
			total=0
			for item in alias[gene]:
				total+=alias[gene][item]
			for item in alias[gene]:
				alias[gene][item]/=float(total)

	summary_term_dir = "gene-expansion/top_10_in_summary"
	summary={}
	for file in os.listdir(summary_term_dir):
		with open(os.path.join(summary_term_dir,file)) as infile:
			gene=re.sub(r'.json','',file)
			summary[gene]=json.load(infile)
			total=0
			for item in summary[gene]:
				total+=summary[gene][item]
			for item in summary[gene]:
				summary[gene][item]/=float(total)	
	return alias, summary

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
		# print q_id
		for items in topics:
			# print items.text
			if items.text is None:
				items.text=""
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

if __name__ == '__main__':

	main()