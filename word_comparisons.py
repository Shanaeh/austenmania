#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Thanks to JD Porter / Literary Lab in 2019 for help with writing this script!
import os, io, csv, string, scipy.stats

#variables for this usage
my_main_directory = f"{os.getcwd()}/corpus/"
my_metadata_table = f"{os.getcwd()}/Austen_Metadata.csv"
ofn = my_main_directory + "_mdw.tsv"
encoding = "utf-8" # text file encoding: utf-8

#building a body of functions

# Turn a spreadsheet into a list of lists (aka a matrix table)
#Use this for the metadata table that organizes your corpus
#Currently, w/ the separator, only accepts .csv files
def sheet2lol(fn,separator=","):
	file = io.open(fn,encoding=encoding)
	text = file.read()
	file.close()
	lines = text.splitlines()
	lol = [] #list of lists
	for line in lines:
		line = line.split(separator)
		lol.append(line)
	return lol

# Turns a directory into a list of its text files
# The directory contains your corpus, and these files must all end with .txt
#Use this for your corpus, which will exclude the metadata table
def dir2files(somedirectory,path=False): #the path = is the default option
	if path == False:
		files = os.listdir(somedirectory)
	else:
		files = os.listdir(somedirectory)
		files = [os.path.join(somedirectory,file) for file in files]
	for i in files[:]:
			if not i.endswith(".txt"):
				files.remove(i)
	return files

# Clean words; need to adjust the parameters here
# Usually want to make lowercase, but might not with names
def cleanword(word,lower=True):
    if lower: 
    	word = word.lower()
    # If you want to keep numbers, change to "isalnum"
    while word and not word[0].isalnum(): #if starts with a number, will remove char
        word = word[1:]
    while word and not word[-1].isalnum(): #if ends with a number, will remove char
        word = word[:-1]
    
    #remove apostrophes contained in string
    word = string.replace(word, "'", "")

    # all of this is if you want to get rid of apostrophe s's
    if word.endswith("'s"):
        word = word[:-2]
        #w=w+"s"

    return word

# Turn a filename into a cleaned up list of its words
def file2cleanwords(filename):
    file = io.open(filename,encoding=encoding)
    text = file.read()
    file.close()
    text = text.encode(encoding)
    
    # Get rid of curly quotes, apostrophes, and em dashes
    text = text.replace("\xe2\x80\x93"," ").replace("\xe2\x80\x94"," ").replace('\u2019',"'").replace("\u2018","'").replace("\u201c",'"').replace("\u201d",'"').replace("‘","'").replace("’","'").replace('“','"').replace("”",'"').replace('\xa0', ' ')
    words = text.split() #splits at any empty space
    words = [cleanword(word) for word in words]
    #savecleanedfile(filename, words) #save cleaned file for mallet
    return words

def savecleanedfile(filename, words):
	newname = filename[:-4] #removes the .txt portion
	with open(newname + "_Cleaned.txt",'w') as output_file:
		output_file.write(" ".join(words))
	print("Wrote the file " + filename)

# Get the unique values in a spreadsheet column
# (Actually a list of lists now, but same idea)
def unique_col_values(somedf,col_num,header=True):
	values = []
	if header == True:
		somedf = somedf[1:]
	for row in somedf:
		v = row[col_num]
		if v not in values:
			values.append(v)
	return values


# Turn your corpora into wordcount dictionaries
# This will be a dictionary of dictionaries
# For this to work as is, your metadata table must have filenames but not path names
def makecorpusdicts(somedir,metatable,meta_col_num,fn_col_num):
	corp_dict = {}
	files = dir2files(somedir)
	corpora = unique_col_values(metatable,meta_col_num)
	for c in corpora:
		corp_dict[c] = {}
	for row in metatable[1:]:
		fn = os.path.join(somedir,row[fn_col_num])
		words = file2cleanwords(fn)
		cd = str(row[meta_col_num])
		for w in words:
			if w in corp_dict[cd]:
				corp_dict[cd][w] += 1
			else:
				corp_dict[cd][w] = 1
	return corp_dict


# Get word counts for your corpora from the "makecorpusdicts" output
# This would work for any such dictionary of dictionaries
# Useful for subcorpora within your corpora
def get_wcd(corp_dict):
	wcd = {}
	for cd in corp_dict:
		tempdict = dict(corp_dict[cd])
		wcd[cd] = sum(tempdict.values())
	return wcd

# Turn a directory of text files into an overall dictionary of word counts
# Will count the entire corpora, use get_wcd for a subcorpora
def dir2counts(somedirectory):
	counts = {}
	files = dir2files(somedirectory,path=True)
	wordoccurences = 0
	
	for file in files:
		words = file2cleanwords(file)
		for word in words:
			if word in counts:
				counts[word] += 1
			else:
				counts[word] = 1
	return counts

# For MDW, we want word rates
# I.e. how often a word appears given the word count
# This converts a counts dictionary to a rates dictionary
def counts2rates(somecountdict):
	rates = dict(somecountdict)
	total = sum(somecountdict.values())
	for key in rates:
		rates[key] = float(rates[key])/total
	return rates

# Make your dictionaries a term document matrix
# This gives you a good way to A) produce writable output
# And B), go through and get MDW later on
# min_obs refers to total observations across all corpora
def dicts2tdm(dictofcountdicts,min_obs=0,no_numbers=False):
	# I'm removing any corpus that had no actual values found; might not want to do this
	for d in dictofcountdicts:
		if sum(dictofcountdicts[d].values()) == 0:
			del dictofcountdicts[d]
	tdm = [['token_']+list(dictofcountdicts.keys())]
	all_words = []
	for d in dictofcountdicts:
		for w in list(dictofcountdicts[d].keys()):
			if w not in all_words:
				all_words.append(w)
	for w in all_words:
		row=[w]
		for col in tdm[0][1:]:
			if w in dictofcountdicts[col]:
				row.append(dictofcountdicts[col][w])
			else:
				row.append(0)
		tdm.append(row)
	if no_numbers == True:
		for row in tdm[1:]:
			if is_number(row[0]):
				tdm.remove(row)
	for row in tdm[1:]:
		if sum(row[1:]) < min_obs:
			tdm.remove(row)
	return tdm

# 'Melts' the tdm
# Which means columns are types of data instead of particular instances of that type
# E.g. instead of columns for "Western" and "Sci-Fi" you'd have "Genre" and list the two types under it for each word
def tdm_melter(sometdm):
	old_headers = sometdm[0]
	melt = [['token_','corpus','observations']]
	for row in sometdm[1:]:
		for n,col in enumerate(row[1:],1):
			ol = [row[0],old_headers[n],row[n]]
			melt.append(ol)
	return melt

# Do a Fishers exact test, mdw style
def get_fishers(melted_tdm_row,wcd,word_rates,obs_exp=False,alternative="greater"):
	corpus = melted_tdm_row[1]
	wc = wcd[corpus]
	word = melted_tdm_row[0]
	rate = word_rates[word]
	a = melted_tdm_row[2]
	b = wc-a
	c = round(rate*wc)
	d = wc-c
	p = scipy.stats.fisher_exact([[a,b],[c,d]],alternative=alternative)[1]
	if obs_exp == True:
		if c != 0:
			oe = a/c
		else:
			oe = "Inf"
		p = (p,oe)
	return p

# Get the actual mdw data and append to the tdm
def add_mdw(melted_tdm,wcd,word_rates,obs_exp=True,alpha=0.05,alternative="greater"):
	melted_tdm[0].extend(['p_value','Obs/Exp'])
	for row in melted_tdm[1:]:
		duple = get_fishers(row,wcd,word_rates,obs_exp=obs_exp,alternative=alternative)
		p = duple[0]
		if p >= alpha:
			melted_tdm.remove(row)
		else:
			row.extend([p,duple[1]])
	return melted_tdm

# Turns our list of lists into a spreadsheet, located wherever you put it
# I recommend using tab separation, but commas are sometimes preferable
def lol_to_file(lol,output_filename,separator="\t"):
	with open(output_filename,'w') as output_file:
		for row in lol:
			row = [str(i) for i in row]
			ostr = "\t".join(row) + "\n"
			output_file.write(ostr)
	print("Wrote the file " + output_filename)

# Combine all the functions above to get MDW from a metadata table and a corpus
# If there's an equals sign in any of the inputs, you don't have to write anything unless you want to change the default
# Otherwise, you have to write something
def get_mdw(metadata_table_fn,metadata_column_num,filename_col_num,source_directory,output_filename,metadata_table_separator=",",keep_uppercase=False,minimum_observations=0,fishers_alternative="greater",alpha=.05,output_filename_separator="\t"):
	print("Reading metadata table...")
	metatable = sheet2lol(metadata_table_fn,separator=metadata_table_separator)
	print("Making a wordcount dictionary for each subcorpus...")
	corp_dict = makecorpusdicts(source_directory,metatable,meta_col_num=metadata_column_num,fn_col_num=filename_col_num)

	with open(output_filename,'w') as output_file:
		row = [str(i) for i in corp_dict]
		ostr = "\t".join(row) + "\n"
		output_file.write(ostr)
	print("Wrote the file " + output_filename)

	print("Getting total word counts for your subcorpora...")
	wcd = get_wcd(corp_dict)
	print("Getting word counts for the full corpus...")
	counts = dir2counts(source_directory)
	print(counts)
	print("Coverting those counts to rates...")
	rates = counts2rates(counts)
	print("Making a tdm out of the individual corpus counts...")
	tdm = dicts2tdm(corp_dict,min_obs=minimum_observations)
	print("Melting the tdm...")
	melted_tdm = tdm_melter(tdm)
	print("Getting mdw data...")
	mdw = add_mdw(melted_tdm,wcd,rates,alpha=alpha,alternative=fishers_alternative)
	print("Writing data to file...")
	lol_to_file(mdw,output_filename)

	print("Hello, world! Welcome back!") #my happy little starter message
#get_mdw(my_metadata_table,metadata_column_num=5,filename_col_num=0,source_directory=my_main_directory,output_filename=ofn,minimum_observations=10)

def clean_one_file(filename):
    file = io.open(filename, encoding=encoding)
    text = file.read()
    file.close()
    text = text.encode(encoding)
    
    # Get rid of curly quotes, apostrophes, and em dashes
    text = text.replace("\xe2\x80\x93"," ").replace("\xe2\x80\x94"," ").replace('\u2019',"'").replace("\u2018","'").replace("\u201c",'"').replace("\u201d",'"').replace("‘","'").replace("’","'").replace('“','"').replace("”",'"').replace('\xa0', ' ')
    words = text.split() #splits at any empty space
    words = [cleanword(word) for word in words]
    save_cleaned_file(filename, words) #save cleaned file for mallet
    return words

def save_cleaned_file(filename, words):
	# newname = filename
	# with open(newname,'w') as output_file:
	newname = filename[:-4]
	with open(newname + "_Cleaned.txt",'w') as output_file:
		output_file.write(" ".join(words))
	print("Cleaned the file " + filename)

#clean_one_file(my_main_directory + "Austen_SenseAndSensibility.txt")

#text to word count
def get_word_frequencies(filename):
	wordcount = {}
	with open(my_main_directory + filename) as file:
		for word in file.read().split():
			if word not in wordcount:
				wordcount[word] = 1
			else:
				wordcount[word] += 1
	wordcount = sorted(wordcount.items(), key=lambda item: item[1], reverse=True) #orders based on most used

	csv_wri = csv.writer(open(filename[:-4] + "_count.csv", "w"))
	for key, val in wordcount:
		csv_wri.writerow([key, val])

# get_word_frequencies("Austen_SenseAndSensibility.txt")