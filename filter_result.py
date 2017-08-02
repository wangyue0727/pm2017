import re,os,math,argparse
from lxml import etree
import string

def main(orig, result, runid):

	demo=load_demo("/local/data/yuewang/PM/collection/clinicaltrials_clean")
	
	queries = read_input(orig)
	keylist = queries.keys()
	keylist.sort()	

	with open("../results/"+runid+".txt","w") as outfile:
		with open(result,"r") as infile:
			for line in infile:
				line=line.strip()
				items = line.split()
				docid = items[2]
				qid = int(items[0])
				target_age, target_gender = queries[qid]["demographic"].split()
				target_age = int(re.sub(r'yearold','',target_age))
				# print target_age, target_gender
				max_age=200
				if demo[str(items[2])]["max_age"]:
					max_age=float(demo[str(items[2])]["max_age"])
				else:
					max_age=200
				min_age=0
				if demo[str(items[2])]["min_age"]:
					min_age=float(demo[str(items[2])]["min_age"])
				else:
					min_age=0		
				if target_gender in demo[str(items[2])]["gender"].lower():
					if target_age < max_age and target_age > min_age:
					# print "yes"
						print str(qid)+" Q0 "+str(docid)+" "+ items[3]+" "+items[4]+" "+runid
						outfile.write(str(qid)+" Q0 "+str(docid)+" "+ items[3]+" "+items[4]+" "+runid+"\n")
					# else:
					# 	print target_age, max_age, min_age
				else:
					print target_gender, demo[str(items[2])]["gender"].lower()

def load_demo(path):
	demo={}
	for file in os.listdir(path):
		# print file
		with open(os.path.join(path,file),"r") as infile:
			docid=""
			genderstart=False
			min_agestart=False
			max_agestart=False
			gender=""
			for line in infile:
				line = line.strip()
				if "DOCNO" in line:
					docid=re.sub(r'<DOCNO>','',line)
					docid=re.sub(r'</DOCNO>','',docid)
				if "<gender>" in line:
					genderstart=True
					continue
				if "</gender>" in line:
					genderstart=False
					continue	
				if genderstart:
					gender=line

				if "<min_age>" in line:
					min_agestart=True
					continue
				if "</min_age>" in line:
					min_agestart=False
					continue	
				if min_agestart:
					min_age=line	

				if "<max_age>" in line:
					max_agestart=True
					continue
				if "</max_age>" in line:
					max_agestart=False
					continue	
				if max_agestart:
					max_age=line

				if "</DOC>" in line:
					demo[docid]={}
					demo[docid]["min_age"]=min_age
					demo[docid]["max_age"]=max_age
					demo[docid]["gender"]=gender	
	return demo

def load_result(result):
	result_dict={}
	with open(result,"r") as infile:
		for line in infile:
			line=line.strip()
			items = line.split()
			if items[0] not in result_dict:
				result_dict[items[0]]={}
			result_dict[items[0]][items[2]]=items[4]
			# result_dict[items[0]]["score"]=items[4]
	return result_dict

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
	parser = argparse.ArgumentParser()
	parser.add_argument("original",nargs="?",help="original query file")
	parser.add_argument("temp_result",nargs="?",help="temp result file to be filtered")
	parser.add_argument("runID",nargs="?",help="run ID for the generated run")
	
	args = parser.parse_args()
	original = args.original
	result = args.temp_result
	runid=args.runID

	main(original,result,runid)