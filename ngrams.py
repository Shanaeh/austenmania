import os, io, csv, json, string

import nltk
from nltk import *
from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")

#variables for this usage
my_main_directory = f"{os.getcwd()}/corpus/"
encoding = "utf-8" # text file encoding: utf-8

#bigram generator
#separate into list of bigrams, then group by first word, next word + count of similar pairs

#text to bigram
def get_formatted_bigrams(filename):
   tokens = None
   bigrams = None
   with open(my_main_directory + filename) as file:
      text = file.read().replace('\n', '')
      tokens = word_tokenize(text)
      bigrams = list(nltk.bigrams(tokens))
   
   #format bigrams for easier viz-processing
   formatted_bigrams = {}
   for bigram in bigrams:
      key = bigram[0]
      if key not in formatted_bigrams:
         formatted_bigrams[key] = {bigram[1]: 1} # a dict with 1 val
      else:
         outer_val = bigram[1]
         nested_dict = formatted_bigrams[key]
         not_in_nest = True
         for nested_bigram_key in nested_dict: #{"meow": 4, "roar": 7}
            if outer_val == nested_bigram_key: #checks against the key
               nested_dict[outer_val] += 1
               not_in_nest = False
         if not_in_nest: #else, add another value pair to the nested dict
            nested_dict[outer_val] = 1

   with open(filename[:-4] + "_bigrams.json", "w") as outfile:
      json.dump(formatted_bigrams, fp=outfile, sort_keys=True, indent=4)

# get_formatted_bigrams("Austen_PrideAndPrejudice.txt")
# get_formatted_bigrams("Austen_NorthangerAbbey.txt")
# get_formatted_bigrams("Austen_MansfieldPark.txt")
# get_formatted_bigrams("Austen_Emma.txt")
# get_formatted_bigrams("Austen_Persuasion.txt")
# get_formatted_bigrams("Austen_SenseAndSensibility.txt")
# get_formatted_bigrams("Austen_Combined.txt")

