#!/usr/bin/env python
# This is a python script to grab all relevant data from the server and pack them into folders with their names are
# the same as the "desrciptor" in the description file
# Working!!

verbose = False
import os,time
from datetime import datetime
import re	# for checking import dates in file seperated by tab "/t"
import shutil

patt = re.compile("[^\t]+")

def get_dates_from_written_file(writtenfile):
	if verbose: print("Getting dates from " + writtenfile)
	with open(writtenfile) as in_file:
		lines = in_file.readlines()[1:]		#skip first row as it contains just some labeling #testing
#		lines = [lines.rstrip('\n') for line in open("/home/ga32xan/Desktop/Messzeiten")]

		if verbose:
			print ("lines:")
			print (lines)

		for item in lines:
			entry = patt.findall(item)
			if verbose:
				print ("entries:"+ entry[0]+" "+entry[1]+" "+entry[2])

#			directory = "/home/ga32xan/Network/LT_Testdata/"
			directory = "/home/ga32xan/Desktop/temp"

#			destination = "/home/ga32xan/Network/private/Promotion/Daten/" + entry[2]
			destination = "/home/ga32xan/Desktop/temp/" + entry[2]
			if not os.path.exists(destination):
			    os.makedirs(destination)

			datfile = []
			vertfile = []
			date1 = datetime.strptime(entry[0],'%Y-%m-%d')	
			date2 = datetime.strptime(entry[1],'%Y-%m-%d')			#datetime.datetime object
#			if verbose: print("type of date1/2 is:" + str(type(date1)))
			print("")
			print("Beginning file crawling in :" + directory)
			print("for " + str(date1) + " < date < " + str(date2))
			for root, dirs, files in os.walk(directory):
				for file in files:
					if file.endswith(".dat"):			#Crawling for .dat-files
						filepath = os.path.join(root, file)
						#print("type filepath: " + str(type(filepath)))
						if check_file(filepath,date1,date2):
							datfile.append(filepath)						
							if verbose: print("found dat-file: " + filepath + "    Total:  " + str(len(datfile)))
					if file.endswith(".VERT"):			#Crawling for .VERT-files
						if check_file(file,date1,date2):
							vertfile.append(os.path.join(root, file))
						if verbose: 
							if verbose: print("found VERT-file: " + filepath + "    Total:  " + str(len(vertfile)))

			if verbose: 
				print("Found " + str(len(datfile)) + "   .dat     and     " + str(len(vertfile)) + "   .VERT")
			print("Will copy to " + destination + "... proceed?")


	
			if not raw_input('Press enter to continue: '):		# Just evaulates if "ENTER" is hit, no other key
				for item in datfile: shutil.copy2(item,destination)

def check_file(file,date1,date2):
	crea= datetime.fromtimestamp(os.path.getmtime(file))	#datetime.datetime object
	mod = datetime.fromtimestamp(os.path.getctime(file))
	if verbose:
		print ("File creation date: " + str(crea))
		print ("File modification date: " + str(mod))
				#		print ("type of 'os.path.getctime(file)':" + str(type(os.path.getctime(file))))

	if crea > date1:
		if verbose: print("file date larger than" + str(date1))
		if crea < date2:
			if verbose: print("file date smaller than" + str(date2))
			print(str(file) + "  MATCHES  " + str(date1) + " and " + str(date2)) 
			return True
#########################
get_dates_from_written_file("/home/ga32xan/Desktop/Messzeiten")