import os, argparse, operator

def main(result_1,result_2,runid):	
	result1=load_result(result_1)
	result2=load_result(result_2)

	target=1000

	root_dir="../results"

	outfile = os.path.join(root_dir,runid+".txt")
	if os.path.isfile(outfile):
		cont = raw_input(runid+" output file exists. Continue?  ")
		if not cont == "y":
			print "Exiting the system..."
			exit()
		else:
			print "Existing file "+runid+" will be overwritten!"

	with open(outfile,"w") as outfile:	
		for qid in xrange(1,31):
			qid=str(qid)
			score_range_1 = result1[qid]["max"]-result1[qid]["min"]
			score_range_2 = result2[qid]["max"]-result2[qid]["min"]
			final={}
			for did in result1[qid]:
				if did == "max" or did == "min":
					continue
				else:
					norm_score_1 = float(result1[qid][did]-result1[qid]["min"])/score_range_1
					if did in result2[qid]:
						norm_score_2 = float(result2[qid][did]-result2[qid]["min"])/score_range_2
					else:
						norm_score_2 = 0
				final[did]=norm_score_1+float(norm_score_2)
			for did in result2[qid]:
				if did == "max" or did == "min":
					continue
				if not did in final:
					norm_score_2 = float(result2[qid][did]-result2[qid]["min"])/score_range_2				
					final[did]=norm_score_2
			sort_final = sorted(final.items(), key=lambda x:x[1], reverse=True)
			# print sort_final
			rank=1
			for item in sort_final:
				if rank <= target:
					outfile.write(str(qid)+" Q0 "+str(item[0])+" "+str(rank)+" "+str(item[1])+" "+runid+"\n")
					# print str(qid)+" Q0 "+str(item[0])+" "+str(rank)+" "+str(item[1])+" "+runid
					rank+=1

def load_result(result):
	result_dict={}
	with open(result,"r") as infile:
		for line in infile:
			line=line.strip()
			items = line.split()
			if items[0] not in result_dict:
				result_dict[items[0]]={}
			result_dict[items[0]][items[2]]=float(items[4])
	for qid in result_dict:
		min_score = 1000000000
		max_score = -100000000000
		for did in result_dict[qid]:
			if result_dict[qid][did] > max_score:
				max_score = result_dict[qid][did]
			if result_dict[qid][did] < min_score:
				min_score = result_dict[qid][did]

		result_dict[qid]["min"]=min_score
		result_dict[qid]["max"]=max_score
	return result_dict

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("result_1",nargs="?",help="first result list")
	parser.add_argument("result_2",nargs="?",help="second result list")
	parser.add_argument("runID",nargs="?",help="run ID for the generated run")
	
	args = parser.parse_args()
	result_1 = args.result_1
	result_2 = args.result_2
	runid=args.runID

	main(result_1,result_2,runid)