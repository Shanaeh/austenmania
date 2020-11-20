import os, io, csv, json, string
import re
import pandas as pd

import nltk

#variables for this script
my_main_directory = f"{os.getcwd()}/nested_paragraphs/"
encoding = "utf-8" # text file encoding: utf-8

#char names
sas_chars = [["Elinor", "Miss Dashwood"],
            ["Marianne", "Miss Dashwoods"], #tag Marianne, the younger, when paired
            ["Brandon", "the Colonel"],
            ["Willoughby"],
            ["Edward", "Mr. Ferrars"],
            ["Miss Grey", "Sophia"],
            ["Lucy", "Miss Steeles"], #tag Lucy, the younger, when paired
            ["Mrs. Jennings"]
            ]
sas_names = ["Elinor Dashwood", "Marianne Dashwood", "Colonel Brandon", "John Willoughby", "Edward Ferrars", "Sophia Grey", "Lucy Steele", "Mrs. Jennings"]

pap_chars = [["Elizabeth", "Lizzy"],
            ["Darcy"],
            ["Jane", "Miss Bennet"],
            ["Bingley", "Charles"], #Unfortunately this will also include 87 references to Miss Bingley
            ["Wickham"],
            ["Charlotte", "Miss Lucas", "Mrs. Collins"],
            ["Lady Catherine", "De Bourgh"],
            ["Mr. Collins", "WILLIAM COLLINS"],
            ["Lydia", "Mrs. Wickham"],
            ["Miss Bingley", "Caroline"]
            ]
pap_names = ["Elizabeth Bennet", "Fitzwilliam Darcy", "Jane Bennet", "Charles Bingley", "George Wickham", "Charlotte Lucas", "Lady Catherine", "Mr. Collins", "Lydia Bennet", "Caroline Bingley"]

na_chars = [["Catherine", "Miss Morland"],
            ["Henry", "Mr. Tilney"],
            ["Eleanor", "Miss Tilney"],
            ["Isabella", "Miss Thorpe"],
            ["James", "Mr. Morland"],
            ["General Tilney", "the general"], #<5 uses of "the general" for non-character uses
            ["Captain Tilney", "Frederick"],
            ["Mrs. Allen"], 
            ["Mr. Allen"]
            ]
na_names = ["Catherine Morland", "Henry Tilney", "Eleanor Tilney", "Isabella Thorpe", "James Morland", "General Tilney", "Captain Tilney", "Mrs. Allen", "Mr. Allen"]

mp_chars = [["Fanny", "Miss Price"],
            ["Edmund"],
            ["Henry", "Mr. Crawford"],
            ["Mary", "Miss Crawford"],
            ["Mrs. Norris"],
            ["Sir Thomas"],
            ["Lady Bertram"],
            ["Maria", "Mrs. Rushworth", "Miss Bertram"], #eldest daughter is Miss until married
            ["Julia", "Miss Bertrams"] #Tag Julia, the younger, when the Miss Bertrams are mentioned together
            ] 
mp_names = ["Fanny Price", "Edmund Bertram", "Henry Crawford", "Mary Crawford", "Mrs. Norris", "Sir Thomas", "Lady Bertram", "Maria Bertram", "Julia Bertram"]

emma_chars = [["Emma", "Miss Woodhouse"], 
            ["Knightley"],
            ["Frank", "Mr. Churchill"],
            ["Jane", "Miss Fairfax"],
            ["Harriet", "Miss Smith"], 
            ["Robert", "Mr. Martin"],
            ["Miss Bates"],
            ["Mrs. Weston", "Miss Taylor"],
            ["Mr. Elton"],
            ["Mrs. Elton"]
            ]
emma_names = ["Emma Woodhouse", "George Knightley", "Frank Churchill", "Jane Fairfax", "Harriet Smith", "Robert Martin", "Miss Bates", "Mrs. Weston", "Mr. Elton", "Mrs. Elton"]

p_chars = [["Anne"],
            ["Frederick", "Wentworth"],
            ["Mr Elliot"],
            ["Mary", "Mrs Musgrove"],
            ["Elizabeth", "Miss Elliot"],
            ["Lady Russell"],
            ["Walter"],
            ["Mrs Clay"],
            ["Louisa", "Miss Musgrove"],
            ["Henrietta", "Miss Musgroves"], #Louisa and Henrietta referred to as a pair
            ["Mrs Smith"]
            ]
p_names = ["Anne Elliot", "Frederick Wentworth", "William Elliot", "Mrs. Musgrove", "Elizabeth Elliot", "Lady Russell", "Sir Walter", "Mrs. Clay", "Louisa Musgrove", "Henrietta Musgrove", "Mrs. Smith"]

#character occurrence script inspired from https://github.com/p-mckenzie/example-projects/blob/master/Jane%20Austen%20Analysis.ipynb
def count_char_occurrences(filename, char_list, char_standardized_names):
    with open(my_main_directory + filename) as file:
        novel_nested_paragraphs = json.load(file)
    char_occurrences = []
    for name in char_standardized_names:
        char_occurrences.append({"name": name, "values": []})

    current_char_index = 0
    for char_nicknames in char_list:
        for chapter in novel_nested_paragraphs:
            chapter_count = 0
            chapter_values = {"chapter": chapter["chapter"], "count": 0, "paragraph_counts": []}

            for paragraph in chapter["paragraphs"]:
                paragraph_count = 0
                sentence_list =  nltk.sent_tokenize(paragraph)
                #Count max 1 mention per sentence to reduce exaggeration / overlap (e.g. Mrs. Bennet muttering Lydia several times in one sentence)
                for sentence in sentence_list:
                    for name in char_nicknames:
                        if name in sentence:
                            paragraph_count += 1
                            break
                
                chapter_count += paragraph_count
                chapter_values["paragraph_counts"].append(paragraph_count)

            chapter_values["count"] = chapter_count
            char_occurrences[current_char_index]["values"].append(chapter_values)
        
        current_char_index += 1
    filename_ending_len = len("nested_paragraphs.json") + 1
    with open(filename[:-filename_ending_len] + "_character_occurrences.json", "w") as outfile:
      json.dump(char_occurrences, fp=outfile, sort_keys=True, indent=4)


#since this script will look for substrings, which can be error-prone with last name references 
#as male characters are often referred to by their last name, even if they have female relations with Miss, Mr, Mrs
#there will be a few overlaps; normalization + smoothing with d3 will hopefuly reduce reader confusion

# count_char_occurrences("Austen_SenseAndSensibility_nested_paragraphs.json", sas_chars, sas_names)
# count_char_occurrences("Austen_PrideAndPrejudice_nested_paragraphs.json", pap_chars, pap_names)
# count_char_occurrences("Austen_NorthangerAbbey_nested_paragraphs.json", na_chars, na_names)
# count_char_occurrences("Austen_MansfieldPark_nested_paragraphs.json", mp_chars, mp_names)
# count_char_occurrences("Austen_Emma_nested_paragraphs.json", emma_chars, emma_names)
# count_char_occurrences("Austen_Persuasion_nested_paragraphs.json", p_chars, p_names)


########################
#fix the Charles Bingley and Miss Bingley name overlap; even in text-mining Miss Bingley seeks to sabotage :)
def clean_pap(): #get temp file from removing "Caroline" (17 occurrences) and only using "Miss Bingley" in the char mappings
    with open(os.getcwd() + "/" + "Austen_PrideAndPrejudice_character_occurrences_TEMP.json") as file:
        char_groupings = json.load(file)
    
    bingley_grouping = char_groupings[3]
    caroline_grouping = char_groupings[9]

    current_chapter_index = 0
    for chapter_value in bingley_grouping["values"]:
        if caroline_grouping["values"][current_chapter_index]["count"]:
            chapter_value["count"] -= caroline_grouping["values"][current_chapter_index]["count"]
            curr_paragraph_index = 0
            for paragraph in chapter_value["paragraph_counts"]:
                chapter_value["paragraph_counts"][curr_paragraph_index] -= caroline_grouping["values"][current_chapter_index]["paragraph_counts"][curr_paragraph_index]
                curr_paragraph_index += 1
        current_chapter_index += 1
    
    char_groupings[3] = bingley_grouping

    with open("pap_cleaned_to_copy_over.json", "w") as outfile:
      json.dump(char_groupings, fp=outfile, sort_keys=True, indent=4)

# clean_pap()