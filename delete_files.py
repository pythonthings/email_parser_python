import os
from os import listdir
main_path = "C:\\Users\\Rohan Baisantry\\Desktop\\Python, ML, Dl, RL and AI\\pythonfiles\\email_parser\\AIDATA\\INWARD"
files = []
for i1 in listdir(main_path):
	for i2 in listdir(main_path + "\\" + i1):
		for i3 in listdir(main_path + "\\" + i1 + "\\" + i2):
			if i3[-3:] != "eml":
				os.remove(main_path + "\\" + i1 + "\\" + i2 + "\\" + i3)

print("\n\t deleted all files that are not .eml files \n")