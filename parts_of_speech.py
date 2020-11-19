import os, io, pd, csv, json, string

import nltk
from nltk import stopwords
cachedStopWords = stopwords.words("english")

#variables for this script
my_main_directory = f"{os.getcwd()}/corpus/"
encoding = "utf-8" # text file encoding: utf-8

#char names
emma_chars = [["Emma"], 
             ["Knightley"],
             ["Frank", "Mr. Churchill"],
             ["Jane"],
             ["Harriet"], 
             ["Bates"],
             ["Mrs. Weston", "Taylor"],
             ["Elton"]]

pap_chars = [["Elizabeth", "Lizzie"],
             ["Jane", "Ms. Bennet"],
             ["Wickham"],
             ["Darcy"],
             ["Bingley"],
             ["Charlotte", "Ms. Lucas", "Mrs. Collins"],
             ["Lady Catherine", "De Bourgh"],
             ["Mr. Collins", "WILLIAM COLLINS"]]

sas_chars = [["Elinor", "Miss Dashwood"],
            ["Marianne"],
            ["Brandon"],
            ["Willoughby"],
            ["Edward", "Mr. Ferrars"],
            ["Miss Grey", "Sophia"],
            ["Steele"],
            ["Mrs. Jennings"]]

p_chars = [["Anne"],
            ["Frederick", "Wentworth"],
            ["Mr Elliot"],
            ["Mary", "Mrs Musgrove"],
            ["Elizabeth", "Miss Elliot"],
            ["Walter"],
            ["Mrs Clay"],
            ["Louisa"],
            ["Henrietta"]]

nh_chars = [["Catherine", "Miss Morland"],
            ["Henry", "Mr. Tilney"],
            ["Eleanor", "Miss Tilney"],
            ["Isabella", "Miss Thorpe"],
            ["James", "Mr. Morland"],
            ["General Tilney", "the general"], #<5 uses of "the general" for non-character uses
            ["Captain Tilney", "Frederick"],
            ["Mrs. Allen", "Mr. Allen"]]

mp_chars = [["Fanny", "Miss Price"],
            ["Edmund"],
            ["Henry", "Mr. Crawford"],
            ["Mary", "Miss Crawford"],
            ["Mrs. Norris"],
            ["Sir Thomas"],
            ["Maria", "Mrs. Rushworth", "Miss Bertram"], #eldest daughter is Miss until married
            ["Julia", "Miss Bertrams"] #Only tag Julia when the Miss Bertrams are mentioned together

#pos script inspired from https://github.com/p-mckenzie/example-projects/blob/master/Jane%20Austen%20Analysis.ipynb
#remove character names/titles as well as stopwords
for name in {re.sub(r"\W", '', new_item) for sublist in emma_chars+pap_chars+sas_chars for item in sublist for new_item in item.split()}:
    cachedStopWords.append(name.lower())

def tag_text(message):
    return nltk.pos_tag([word for word in re.findall(r"[a-z']+", message.lower()) 
			 if word not in cachedStopWords])

sas_words = pd.DataFrame(tag_text(sas_data), columns=['word', 'pos'])
emma_words = pd.DataFrame(tag_text(emma_data), columns=['word', 'pos'])
pap_words = pd.DataFrame(tag_text(pap_data), columns=['word', 'pos'])


# get_formatted_bigrams("Austen_NorthangerAbbey.txt")
# get_formatted_bigrams("Austen_MansfieldPark.txt")
# get_formatted_bigrams("Austen_Emma.txt")
# get_formatted_bigrams("Austen_Persuasion.txt")
# get_formatted_bigrams("Austen_SenseAndSensibility.txt")
# get_formatted_bigrams("Austen_Combined.txt")

