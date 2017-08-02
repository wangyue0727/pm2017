import re,os,math,argparse

def main(orig, runid):
	vocab_file = "sa_concept_vocab.txt"
	metamap_log = 'query-metamap-log.txt'

	idf=load_idf(vocab_file)
	# print idf
	synonym=find_synonym(metamap_log)
	replace_mapping={}
	# print synonym
	for name in synonym:
		if len(synonym[name])>1:
			max_idf = -100
			target_cui=""
			# print name
			for cui in synonym[name]:
				# print cui.lower()
				if cui.lower() in idf:
					if idf[cui.lower()] > max_idf:
						max_idf=idf[cui.lower()]
						target_cui = cui
				else:
					print cui, " not found"

			for cui in synonym[name]:
				# print idf[cui.lower()]
				if cui.lower() in idf:
					if max_idf >= idf[cui.lower()]:
						replace_mapping[cui]=target_cui
						# print "replace " +cui+ " with "+ target_cui

	update_query_file(orig, runid,replace_mapping)

def update_query_file(orig_query_file, new_runid, mapping):
	root_dir="../query/offcial"

	outfile = os.path.join(root_dir,new_runid+".txt")
	if os.path.isfile(outfile):
		cont = raw_input(new_runid+" output file exists. Continue?  ")
		if not cont == "y":
			print "Exiting the system..."
			exit()
		else:
			print "Existing file "+new_runid+" will be overwritten!"

	with open(orig_query_file,"r") as infile:
		with open(outfile,"w") as outfile:
			for line in infile:
				line=line.strip()
				if line.startswith("<runID>"):
					outfile.write("<runID>"+new_runid+"</runID>\n")
				elif line.startswith("<text>"):
					items = line.split()
					to_print = []
					printed={}
					for item in items:
						if item.startswith("C"):
							if item in mapping:
								if mapping[item] not in printed:
									outfile.write(mapping[item]+" ")
									printed[mapping[item]]=1
							else:
								# to_print.append(item)
								outfile.write(item+" ")
						else: 
							# to_print.append(item)
							outfile.write(item+" ")
					outfile.write("\n")
				else:
					outfile.write(line+"\n")


def find_synonym(metamap_log):
	synonyms={}
	all_num = re.compile("^\d+$")
	with open(metamap_log,"r") as infile:
		pattern = re.compile("^C\d{7}")
		for line in infile:
			line=line.strip()
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

			if candidates:
				if not line:
					continue
				line = line.strip()
				temp = line.split(":")
				cui=temp[0].split()
				if len(cui) == 2 and pattern.match(cui[1]):
					cui = cui[1]
					name = re.sub(r'\(.*\)', '', temp[1])
					name = re.sub(r'\[.*\]', '', name).lower()
					name = name.strip()
					# print cui, name
					if name not in synonyms:
						synonyms[name]=[]
					if cui not in synonyms[name]:
						synonyms[name].append(cui)
	return synonyms


def load_idf(file):
	idf={}
	with open(file,"r") as infile:
		total=0
		for line in infile:
			line=line.strip()
			item=line.split()
			if item[0]=="TOTAL":
				total = item[2]
			else:
				idf[item[0]]=math.log(1+float(total)/float(item[2]))
	return idf



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("original",nargs="?",help="original query file")
	parser.add_argument("runID",nargs="?",help="run ID for the generated run")
	
	args = parser.parse_args()
	original = args.original
	runid=args.runID

	main(original,runid)