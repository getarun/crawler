#!/usr/bin/env python
# This is a python script to grab all relevant data from the server and pack them into folders with their names are
# the same as the "desrciptor" in the description file
# Working!!

verbose = True
import os,time
from datetime import datetime
import re	# for checking import dates in file seperated by tab "/t"
import shutil
import glob

patt = re.compile("[^\t]+")

def get_dates_from_written_file(writtenfile):
	if verbose: 
		print("This is a little python crawler which looks up all the files present in the search-folder with os.walk")
		print("Please give it a folder to search (search-folder) and a folder to copy (copy-folder) to.")
		print("Interaction with files in th search-folder will only happen with shutil.copy2(item,destination) - no write-action happens in the search folder.")
	directory = raw_input('search-folder: )'
	destination_input = raw_input('copy-folder: )'
	
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
	#		directory = "/home/ga32xan/Desktop/temp"

#			destination = "/home/ga32xan/Network/private/Promotion/Daten/" + entry[2]
			destination = destination_input + entry[2]
			if not os.path.exists(destination):
			    os.makedirs(destination)

			datfile = []
			vertfile = []
			dat_copied = 0
			vert_copied = 0
			dat_skipped = 0
			vert_skipped = 0
			date1 = datetime.strptime(entry[0],'%Y-%m-%d-%H:%M')	
			date2 = datetime.strptime(entry[1],'%Y-%m-%d-%H:%M')			#datetime.datetime object
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
						if check_file(filepath,date1,date2):
							vertfile.append(filepath)
							if verbose: print("found VERT-file: " + filepath + "    Total:  " + str(len(vertfile)))

			if verbose: 
				print("Found " + str(len(datfile)) + "   .dat     and     " + str(len(vertfile)) + "   .VERT")
			print("Will _copy_ to " + destination + "... proceed?")


########Security issue: Just do if someone wants it to do....
			if not raw_input('Press enter to continue: '):		# Just evaulates if "ENTER" is hit, no other key
				if verbose: print("#########################...Start copiing files...#########################")
				for item in datfile: 
					try:
						if item not in glob.glob(os.path.join(destination,"*.dat")):	#just copy if not already there!
							shutil.copy2(item,destination)		#copy files
							dat_copied+=1
						else: 
							print("Skip" + item +": already present in " + destination)
							dat_skipped+=1
					except IOError as e:
						print("Copy-Error of " + e)
######
				for item in vertfile: 
					try:
						if item not in glob.glob(os.path.join(destination,"*.VERT")):	#just copy if not already there!
							shutil.copy2(item,destination)		#copy files
							vert_copied+=1
						else: 
							print("Skip" + item +": already present in " + destination)
							vert_skipped+=1
					except IOError as e:
						print("Copy-Error of " + e)
######
				descriptionfile = os.path.join(destination, "descriptionfile")
				with open(descriptionfile, "w") as text_file: text_file.write("This is automatically written {0}".format(entry[3])) #write description
			if verbose: 
				print("*.dat : (copied/skipped):   (" + str(dat_copied) + "/"+ str(dat_skipped)+")")
				print("*.VERT: (copied/skipped):   (" + str(vert_copied) + "/"+ str(vert_skipped)+")")	
#counter not working properly
########################################################################################################################################
def check_file(file,date1,date2):
	crea= datetime.fromtimestamp(os.path.getmtime(file))	#datetime.datetime object
	mod = datetime.fromtimestamp(os.path.getctime(file))
#	if verbose:
#		print ("File creation date: " + str(crea))
#		print ("File modification date: " + str(mod))
				#		print ("type of 'os.path.getctime(file)':" + str(type(os.path.getctime(file))))

	if crea > date1:
#		if verbose: print("file date larger than" + str(date1))
		if crea < date2:
#			if verbose: print("file date smaller than" + str(date2))
			print(str(file) + "  MATCHES  " + str(date1) + " and " + str(date2)) 
			return True
#########################
get_dates_from_written_file("/home/ga32xan/git-working-dir/crawler/Messzeiten")
