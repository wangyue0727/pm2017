import os
import subprocess
import re
import nltk
import argparse
from lxml import etree
import codecs

def main(inputdir,outputdir):
	inputdir = inputdir.rstrip("/")
	outputfile = os.path.join(outputdir,os.path.split(inputdir)[1])
	if os.path.exists(outputfile):
		# print "[ERROR] Duplicate outputfile: "+outputfile	
		return
	else:
		print "+++"+inputdir+"---"
		return
	with codecs.open(outputfile + ".txt","w", encoding="utf-8") as outfile:	
		for filename in os.listdir(inputdir):
			inputfile = os.path.join(inputdir, filename)
			docid = os.path.splitext(filename)[0]
			outfile.write("<DOC>\n<DOCNO>"+docid+"</DOCNO>\n<TEXT>\n")
			try:
				tree = etree.parse(inputfile)
			except:
				print inputfile
			root = tree.getroot()

			if root.find("brief_title") is not None:
				outfile.write("<brief_title>\n"+root.find("brief_title").text+"\n</brief_title>\n")
			else:
				outfile.write("<brief_title>\n \n</brief_title>\n")

			if root.find("acronym") is not None:
				outfile.write("<acronym>\n"+root.find("acronym").text+"\n</acronym>\n")
			else:
				outfile.write("<acronym>\n \n</acronym>\n")

			if root.find("official_title") is not None:
				outfile.write("<official_title>\n"+root.find("official_title").text+"\n</official_title>\n")
			else:
				outfile.write("<official_title>\n \n</official_title>\n")
			
			if root.find("brief_summary") is not None:
				if root.find("brief_summary").find("textblock") is not None:
					content = root.find("brief_summary").find("textblock").text
					content = re.sub(r'\n',' ',content)
					outfile.write("<brief_summary>\n"+ content +"\n</brief_summary>\n")
				else:
					outfile.write("<brief_summary>\n \n</brief_summary>\n")
			else:
				outfile.write("<brief_summary>\n \n</brief_summary>\n")


			if root.find("detailed_description") is not None:
				if root.find("detailed_description").find("textblock") is not None:
					content = root.find("detailed_description").find("textblock").text
					content = re.sub(r'\n',' ',content)					
					outfile.write("<detailed_description>\n"+ content +"\n</detailed_description>\n")
				else:
					outfile.write("<detailed_description>\n \n</detailed_description>\n")
			else:
				outfile.write("<detailed_description>\n \n</detailed_description>\n")

			
			if root.findall("keyword") is not None:
				outfile.write("<keyword>\n")
				for keyword in root.findall("keyword"):
					outfile.write(keyword.text+"\n")
				outfile.write("\n</keyword>\n")
			else:
				outfile.write("<keyword>\n \n</keyword>\n")

			if root.findall("condition") is not None:
				outfile.write("<condition>\n")
				for condition in root.findall("condition"):
					outfile.write(condition.text+"\n")
				outfile.write("\n</condition>\n")
			else:
				outfile.write("<condition>\n \n</condition>\n")

			if root.findall("intervention") is not None:
				outfile.write("<intervention>\n")
				for intervention in root.findall("intervention"):
					outfile.write(intervention.find("intervention_name").text+"\n")
				outfile.write("\n</intervention>\n")
			else:
				outfile.write("<intervention>\n \n</intervention>\n")

			if root.find("condition_browse") is not None:
				if root.find("condition_browse").findall("mesh_term") is not None:
					outfile.write("<condition_browse>\n")
					for term in root.find("condition_browse").findall("mesh_term"):
						outfile.write(term.text+"\n")
					outfile.write("\n</condition_browse>\n")
				else:
					outfile.write("<condition_browse>\n \n</condition_browse>\n")
			else:
				outfile.write("<condition_browse>\n \n</condition_browse>\n")

			if root.find("intervention_browse") is not None:
				if root.find("intervention_browse").findall("mesh_term") is not None:
					outfile.write("<intervention_browse>\n")
					for term in root.find("intervention_browse").findall("mesh_term"):
						outfile.write(term.text+"\n")
					outfile.write("\n</intervention_browse>\n")
				else:
					outfile.write("<intervention_browse>\n \n</intervention_browse>\n")
			else:
				outfile.write("<intervention_browse>\n \n</intervention_browse>\n")


			if root.find("eligibility") is not None:
				if root.find("eligibility").find("gender") is not None:
					if root.find("eligibility").find("gender").text == "All":
						outfile.write("<gender>\nFemale Male\n</gender>\n")
					else:
						outfile.write("<gender>\n"+root.find("eligibility").find("gender").text+"\n</gender>\n")
				else:
					outfile.write("<gender>\n \n</gender>\n")

				if root.find("eligibility").find("minimum_age") is not None:
					if root.find("eligibility").find("minimum_age").text == "N/A":
						outfile.write("<min_age>\n \n</min_age>\n")
					else:
						(number, unit) = root.find("eligibility").find("minimum_age").text.split(" ")
						if unit == "Year" or unit == "Years":
							outfile.write("<min_age>\n"+number+"\n</min_age>\n")
						elif unit == "Month" or unit == "Months":
							outfile.write("<min_age>\n"+str(float(number)/12)+"\n</min_age>\n")
				else:
					outfile.write("<min_age>\n \n</min_age>\n")



				if root.find("eligibility").find("maximum_age") is not None:
					if root.find("eligibility").find("maximum_age").text == "N/A":
						outfile.write("<max_age>\n \n</max_age>\n")
					else:
						(number, unit) = root.find("eligibility").find("maximum_age").text.split(" ")
						if unit == "Year" or unit == "Years":
							outfile.write("<max_age>\n"+number+"\n</max_age>\n")
						elif unit == "Month" or unit == "Months":
							outfile.write("<max_age>\n"+str(float(number)/12)+"\n</max_age>\n")
				else:
					outfile.write("<max_age>\n \n</max_age>\n")

				if root.find("eligibility").find("criteria") is not None:
					if root.find("eligibility").find("criteria").find("textblock") is not None:
						all_criteria = root.find("eligibility").find("criteria").find("textblock").text
						inclusion = True
						exclusion = False
						inclusion_content = ""
						exclusion_content = ""
						for line in all_criteria.split("\n"):
							if line.strip():
								# print line
								if "inclusion" in line.lower():
									inclusion = True
									exclusion = False
								elif "exclusion" in line.lower():
									exclusion = True
									inclusion = False

								if inclusion:
									inclusion_content += line
								if exclusion:
									exclusion_content += line
						outfile.write("<inclusion>\n"+inclusion_content+"\n</inclusion>\n")
						outfile.write("<exclusion>\n"+exclusion_content+"\n</exclusion>\n")
					else:
						outfile.write("<inclusion>\n \n</inclusion>\n")
						outfile.write("<exclusion>\n \n</exclusion>\n")
				else:
					outfile.write("<inclusion>\n \n</inclusion>\n")
					outfile.write("<exclusion>\n \n</exclusion>\n")
			outfile.write("</TEXT>\n</DOC>\n")

def get_leafdir(dirname):
	leaves=[]
	filenames = os.listdir(dirname)
	all_files = True
	for filename in filenames:
		if os.path.isdir(os.path.join(dirname,filename)):
			all_files=False
			leaves.extend(get_leafdir(os.path.join(dirname,filename)))
	if all_files:
		leaves.extend([dirname])		
	
	return leaves

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", nargs='?', 
						help="Input dir that contains xml files. ")
	parser.add_argument("-o", "--output", nargs='?', 
						 help="Output dir for text rep")
	args = parser.parse_args()	

	inputdir = args.input
	outputdir = args.output

	# pool = multiprocessing.Pool(processes=8)

	# # main(inputdir,outputdir)

	# pool.apply_async(runquery,(cmd, ))
 #    pool.close()
 #    pool.join()

	leaves = get_leafdir(inputdir)
	total = len(leaves)
	print total
	count = 0
	for leaf in leaves:
		# print leaf
		main(leaf,outputdir)							
		count += 1

		print str(count)+"/"+str(total)+" has been done"