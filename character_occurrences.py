import os, io, csv, json, string
import re
import pandas as pd

import nltk
from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")

#variables for this script
my_main_directory = f"{os.getcwd()}/corpus/"
encoding = "utf-8" # text file encoding: utf-8

#char names
sas_chars = [["Elinor", "Miss Dashwood"],
            ["Marianne"],
            ["Brandon"],
            ["Willoughby"],
            ["Edward", "Mr. Ferrars"],
            ["Miss Grey", "Sophia"],
            ["Steele"],
            ["Mrs. Jennings"]]

pap_chars = [["Elizabeth", "Lizzie"],
             ["Jane", "Ms. Bennet"],
             ["Wickham"],
             ["Darcy"],
             ["Bingley", "Charles"],
             ["Charlotte", "Ms. Lucas", "Mrs. Collins"],
             ["Lady Catherine", "De Bourgh"],
             ["Mr. Collins", "WILLIAM COLLINS"]]

na_chars = [["Catherine", "Miss Morland"],
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
            ["Julia", "Miss Bertrams"]] #Only tag Julia when the Miss Bertrams are mentioned together

emma_chars = [["Emma"], 
             ["Knightley"],
             ["Frank", "Mr. Churchill"],
             ["Jane"],
             ["Harriet"], 
             ["Bates"],
             ["Mrs. Weston", "Taylor"],
             ["Elton"]]

p_chars = [["Anne"],
            ["Frederick", "Wentworth"],
            ["Mr Elliot"],
            ["Mary", "Mrs Musgrove"],
            ["Elizabeth", "Miss Elliot"],
            ["Walter"],
            ["Mrs Clay"],
            ["Louisa"],
            ["Henrietta"]]

#pos script inspired and drawn from https://github.com/p-mckenzie/example-projects/blob/master/Jane%20Austen%20Analysis.ipynb

with open(my_main_directory + "Austen_SenseAndSensibility.txt") as file:
    sas_data = file.read()
with open(my_main_directory + "Austen_PrideAndPrejudice.txt") as file:
    pap_data = file.read()
with open(my_main_directory + "Austen_NorthangerAbbey.txt") as file:
    na_data = file.read()
with open(my_main_directory + "Austen_MansfieldPark.txt") as file:
    mp_data = file.read()
with open(my_main_directory + "Austen_Emma.txt") as file:
    emma_data = file.read()
with open(my_main_directory + "Austen_Persuasion.txt") as file:
    p_data = file.read()

#remove character names/titles as well as stopwords
for name in {re.sub(r"\W", '', new_item) for sublist in emma_chars+pap_chars+sas_chars+p_chars+na_chars+mp_chars for item in sublist for new_item in item.split()}:
    cachedStopWords.append(name.lower())
cachedStopWords.append("charles")

def tag_text(message):
    return nltk.pos_tag([word for word in re.findall(r"[a-z']+", message.lower()) 
			 if word not in cachedStopWords])

def condense_pos(df):
    df.loc[df['pos'].isin(['JJS', 'JJR']), 'pos'] = 'JJ'
    df.loc[df['pos'].isin(['NNP', 'NNPS', 'NNS']), 'pos'] = 'NN'
    df.loc[df['pos'].isin(['RBR', 'RBS']), 'pos'] = 'RB'
    df.loc[df['pos'].isin(['VBD' 'VBG', 'VBN', 'VBP', 'VBZ']), 'pos'] = 'VB'
    return df.loc[df['pos'].isin(['JJ', 'NN', 'RB', 'VB'])]

#sas_words = pd.DataFrame(tag_text(sas_data), columns=['word', 'pos'])
#pap_words = pd.DataFrame(tag_text(pap_data), columns=['word', 'pos'])
#na_words = pd.DataFrame(tag_text(na_data), columns=['word', 'pos'])
#mp_words = pd.DataFrame(tag_text(mp_data), columns=['word', 'pos'])
#emma_words = pd.DataFrame(tag_text(emma_data), columns=['word', 'pos'])
#p_words = pd.DataFrame(tag_text(p_data), columns=['word', 'pos'])

#sas_words = condense_pos(sas_words).groupby(['pos', 'word']).size().reset_index().sort_values(0, ascending=False).groupby('pos').head(5).sort_values(['pos', 0], ascending=[True, False])
#pap_words = condense_pos(pap_words).groupby(['pos', 'word']).size().reset_index().sort_values(0, ascending=False).groupby('pos').head(5).sort_values(['pos', 0], ascending=[True, False])
#na_words = condense_pos(na_words).groupby(['pos', 'word']).size().reset_index().sort_values(0, ascending=False).groupby('pos').head(5).sort_values(['pos', 0], ascending=[True, False])
#mp_words = condense_pos(mp_words).groupby(['pos', 'word']).size().reset_index().sort_values(0, ascending=False).groupby('pos').head(5).sort_values(['pos', 0], ascending=[True, False])
#emma_words = condense_pos(emma_words).groupby(['pos', 'word']).size().reset_index().sort_values(0, ascending=False).groupby('pos').head(5).sort_values(['pos', 0], ascending=[True, False])
#p_words = condense_pos(p_words).groupby(['pos', 'word']).size().reset_index().sort_values(0, ascending=False).groupby('pos').head(5).sort_values(['pos', 0], ascending=[True, False])

#print(sas_words)
#print(pap_words)
#print(na_words)
#print(mp_words)
#print(emma_words)
#print(p_words)