
# EMAIL PARSER

"""

INPUT: A BUNCH OF EMAIL FILES [ .EML - OUTLOOK FILES ]

OUTPUT: THE SUBJECTS AND BODIES OF EACH EMAIL ALONG WITH THE SUBJECTS AND BODIES OF THE ALL THE REPLIES IT HAS REFERENCED.

"""

# START

# IMPORTS
from os import listdir
import os
import email
import base64
import re

# FUNCTION TO LOAD THE DETAILS OF THE VARIOUS .EML FILES
def load(main_path):
	files = []
	for i1 in listdir(main_path):
		for i2 in listdir(main_path + "\\" + i1):
			for i3 in listdir(main_path + "\\" + i1 + "\\" + i2):
				temp_dict = dict()
				temp_dict["file_name"] = i3
				temp_dict["file_path"] = main_path + "\\" + i1 + "\\" + i2 + "\\" + i3
				temp_dict["folder_path"] = main_path + "\\" + i1 + "\\" + i2 
				temp_dict["label"] = i2
				temp_dict["sub_folder_path"] = i1 + "\\" + i2 
				files.append(temp_dict) 
	return files

# FUNCTION TO CREATE THE .JSON FILE
def create_file(temp_dict):
	json_file_path = temp_dict["file_path"][:-3]
	json_file_path += "json"
	with open(json_file_path,"w+") as f:
		f.write(str(temp_dict))
	f.close()
	return 1

# FUNCTION TO GET BODIES OF THE EMAIL
def get_body(eml_str, n):
	body_dict = dict()
	if n == 1:

		body_dict["1"] = eml_str
	else: 
		i = 0
		j = 1
		e = str(eml_str).split("\\r\\n\\r\\n________________________________\\r\\n")
		for x in e:
			i += 1
			if i == len(e): # removing unwanted text from the last string
				x = re.sub(r"\\r\\n\\r\\n\\r\\n.*", r"", x)
			elif i == 1: # removing " b' " from the first string
				x = x[2:]
			x = re.sub(r"(?s)Feedback\\r\\n.*",r'', x)
			x = re.sub(r"From.*Date     :      \d{2}/\d{2}/\d{4} \d{2}:\d{2}\\r\\n\\r\\n",r"",x)
			y = re.split("On.*?wrote:", x)
			for z in y:
				z = z.replace("\\n", "")
				z = z.replace("\\r", "")
				z = z.replace("_____________________________________________________________", "")
				body_dict[j] = z
				j += 1
	return body_dict

# PARSING FUNCTION
def email_parser(temp_dict):
	msg = email.message_from_file(open(temp_dict["file_path"]))
	if msg.is_multipart() == True:
		temp_dict["attachment"] = True
	else: 
		temp_dict["attachment"] = False
	for part in msg.walk():
		if part.get_content_subtype() == "plain":
			eml_str = str(part.get_payload(decode=True))
			break
			"""
			# incorrect padding check
			missing_padding = len(eml_str) % 4
			if missing_padding != 0:
				eml_str += '=' * (4 - missing_padding)
			
			# since we know it's to be decode using base64
			eml_read = str(base64.b64decode(eml_str))
			"""
	temp_dict["subject"] = msg["subject"].replace("Re: ", "")
	if len(eml_str) == 0:
		temp_dict["body"] = "NO BODY"
	else: 
		temp_dict["body"] = get_body(eml_str, len(eml_str.split("\\r\\n\\r\\n________________________________\\r\\n")))
	#temp_dict["body"] = eml_str
	return 1

# MAIN FUNCTION
def main():
	# load all files
	main_path = "C:\\Users\\Rohan Baisantry\\Desktop\\Python, ML, Dl, RL and AI\\pythonfiles\\email_parser\\AIDATA\\INWARD"
	files =[]
	files.extend(load(main_path))
	i = 0
	print("\n LOADING DONE\n PARSING STARTS:\n")
	for temp_dict in files:
		i += 1
		if email_parser(temp_dict) == 1:
			print("email file '" + temp_dict["file_name"] + "' parsed  - #" + str(i))
			#print(temp_dict["subject"])
			if create_file(temp_dict) == 1:
				print("file " + temp_dict["file_name"][:-3] + "json created at AIDATA\\INWARD\\" + temp_dict["sub_folder_path"])

# RUN
main()