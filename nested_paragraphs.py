import os, io, csv, json, string

import nltk
from nltk import *

#variables for this usage
my_main_directory = f"{os.getcwd()}/corpus/"
encoding = "utf-8" # text file encoding: utf-8

#text to nested paragraphs
def get_nested_paragraphs(filename):

   nested_paragraphs = []
   with open(my_main_directory + filename) as file:
      text = file.read().split('\n') #split by paragraph

      curr_chapter = None
      curr_chapter_index = 1
      for paragraph in text:
         if paragraph: #check for extra empty space between paragraphs
            if paragraph.lower().startswith("chapter"): #break between chapter
               if curr_chapter_index > 1: #remove 0 chapter
                  nested_paragraphs.append(curr_chapter)
               
               curr_chapter = {"chapter": curr_chapter_index, "paragraphs": []}
               curr_chapter_index += 1
            else:
               curr_chapter["paragraphs"].append(paragraph)
      nested_paragraphs.append(curr_chapter) #off by 1

   with open(filename[:-4] + "_nested_paragraphs.json", "w") as outfile:
      json.dump(nested_paragraphs, fp=outfile, sort_keys=True, indent=4)

# get_nested_paragraphs("Austen_Persuasion.txt")
# get_nested_paragraphs("Austen_PrideAndPrejudice.txt")
# get_nested_paragraphs("Austen_NorthangerAbbey.txt")
# get_nested_paragraphs("Austen_MansfieldPark.txt")
# get_nested_paragraphs("Austen_Emma.txt")
# get_nested_paragraphs("Austen_SenseAndSensibility.txt")
