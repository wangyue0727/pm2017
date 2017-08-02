import os, string
import regex as re
import sys
import traceback
import json
from pprint import pprint
import operator
def main():
	if len(sys.argv) != 3:
		print "Usage: python parse_genecards.py inputfile root_output_dir"
		sys.exit()
	else:
		try:
			with open(sys.argv[1],"r") as infile:
				data = json.load(infile)

			# with open("gene-expansion/ALL.json", "r") as infile:
			# 	data2=json.load(infile)

			# data2["GeneData"]["BRAF"]=data["GeneData"]["BRAF"]

			# with open("ALL.json","w") as outfile:
			# 	json.dump(data2,outfile)
			# exit()

			stopword=reads_stop_word()
			stopword=domain_stop_word(stopword)			

			root_dir = sys.argv[2]
			summary_dir = os.path.join(root_dir,"summary")
			alias_dir = os.path.join(root_dir,"alias")
			top_term_dir = os.path.join(root_dir,"top_10_in_summary")
			if not os.path.isdir(root_dir):
				os.makedirs(root_dir)
			if not os.path.isdir(summary_dir):
				os.makedirs(summary_dir)
			if not os.path.isdir(alias_dir):
				os.makedirs(alias_dir)	
			if not os.path.isdir(top_term_dir):
				os.makedirs(top_term_dir)								
			for gene_name in data["GeneData"]:
				if gene_name == "":
					continue
				print gene_name
				
				# Possibles key for each gene:
				  # Genomics
				  # HumanPhenotypeOntology
				  # Domains
				  # MolecularFunctionDescriptions
				  # UniProtDisorders
				  # UnifiedCompounds
				  # DifferentialExpression
				  # Intolerance
				  # Orthologs
				  # SuperPathway
				  # Interactions
				  # Promoters
				  # Phenotypes
				  # Pathways
				  # Variants
				  # Enhancers
				  # UnifiedDrugs
				  # BiologicalProcesses
				  # Proteins
				  # MalaCardsDisorders
				  # CellularComponents
				  # Transcripts
				  # Gene
				  # TissueExpression
				  # Paralogs
				  # StructureVariant
				  # MolecularFunctions
				  # ExternalIdentifiers
				  # Summaries
				  # Aliases	

				# Find all alias. Count the number of sources each alias contains
				alias_mapping={}
				for alias in data["GeneData"][gene_name]['Aliases']:
					# print alias["Value"]	
					if alias["Value"].lower() in alias_mapping:
						alias_mapping[alias["Value"].lower()]+=len(alias["Sources"])
					else: 
						alias_mapping[alias["Value"].lower()]=len(alias["Sources"])
				filename = os.path.join(alias_dir,gene_name+".json")
				with open(filename,"w") as outfile:
					json.dump(alias_mapping,outfile,indent=4)

				# Find all summaries. 
				summaries_mapping={}
				for summaries in data["GeneData"][gene_name]["Summaries"]:
					# print summaries["Summary"]
					summaries_mapping[summaries["Source"]] = summaries["Summary"]
				filename = os.path.join(summary_dir,gene_name+".json")
				with open(filename,"w") as outfile:
					json.dump(summaries_mapping,outfile,indent=4)

				# Select top 10 terms from all summaries
				all_summary = ""
				for item in summaries_mapping:
					all_summary += summaries_mapping[item]

				filename = os.path.join(top_term_dir,gene_name+".json")
				with open(filename,"w") as outfile:				
					all_summary=re.sub(ur"\p{P}+", " ", all_summary)
					all_summary = all_summary.lower()
					terms = all_summary.split()
					term_count={}
					for term in terms:
						if term in stopword:
							continue
						if term in term_count:
							term_count[term]+=1
						else:
							term_count[term]=1
					sorted_term_count = sorted(term_count.items(), key=operator.itemgetter(1), reverse=True)
					count = 0
					to_print = {}
					for term in sorted_term_count:
						if count < 10: 
							to_print[term[0]]=term[1]
							count+=1
					json.dump(to_print,outfile,indent=4)

		except Exception as inst:
			print "Catch an error: "
			print traceback.print_exc()

def domain_stop_word(stopword):

	domain_stop_word=[
		"pubmed",
		"pubmeds",
		"cell",
		"cells",
		"protein",
		"proteins",
		"gene"
	]
	for word in domain_stop_word:
		stopword.append(word)
	return stopword

def reads_stop_word():
	stopword=[]
	if not os.path.isfile("stopwords"):
		print "[Error] Need the Indri default stopword list in the same directory."
		exit()
	with open("stopwords","r") as infile:
		for line in infile:
			line=line.strip()
			if "<word>" in line:
				line=re.sub("<word>","",line)
				line=re.sub("</word>","",line)
				stopword.append(line)
	return stopword

if __name__ == '__main__':
	main()