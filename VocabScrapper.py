################################################################################################################################
#
# Author: Aniruddha Humane
# Date: 02-02-2019
# Git Repository: git@github.com:AniruddhaHumane/VocabularyScrapper.git
# Please Star the repository on github if this was helpful
#
################################################################################################################################

import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

WordList = pd.read_csv("WordList.txt", sep=", ")
url = "https://www.vocabulary.com/dictionary/"
print(len(WordList))

FinalDataFrame = pd.DataFrame(columns=['Word','ShortDefinition','LongDefinition','Meaning','Synonyms','Antonyms'])
checkWord = ["abstemious"]
for word in WordList:
    page = urlopen(url+word)
    print("URL Opened")

    formattedPage = BeautifulSoup(page, "lxml")
    print("Page Formatted")

    #print parsed_html.body.find_all('div', attrs={'class':'container'}).text
    word = formattedPage.find("h1", attrs={'class':'dynamictext'}).text


    shortDescription = formattedPage.find("p", attrs={'class':'short'}).text

    longDescription = formattedPage.find("p", attrs={'class':'long'}).text

    #Definitions

    FinalDefs = []
    Synon = []
    Anton = []

    definitionGroups = formattedPage.find_all("div", attrs={'class':'group'})

    for defGrp in definitionGroups:
        ordinals = defGrp.find_all("div", attrs={'class':'ordinal'})

        for ordinal in ordinals:
            definitions = ordinal.find_all("h3", attrs={'class':'definition'})

            for definition in definitions:
                d = definition.text.split()
                d[0] = '('+d[0]+')'
                d = ' '.join(d)
                FinalDefs.append(d)
            
            dls = ordinal.find_all("dl", attrs={'class':'instances'})
            # print(dls)
            # Syn = []
            # synFlag = False
            # Ant = [] 
            # antFlag = False
            for dl in dls:
                synAnt = dl.find("dt")
                if synAnt.text == "Synonyms:":
                    Synon.append([ i.text for i in dl.find_all("a", attrs={'class':'word'})])
                elif synAnt.text == "Antonyms:":
                    Anton.append([ i.text for i in dl.find_all("a", attrs={'class':'word'})])


            # for i,row in enumerate(synAnt):
            #     if row.text == "Synonyms:" or (row.text == "" and synFlag == True):
            #         Syn.append(i)
            #         synFlag = True
            #     elif row.text == "Antonyms:" or (row.text == "" and antFlag == True):
            #         synFlag = False
            #         antFlag = True
            #         Ant.append(i)
            #     else:
            #         synFlag = False
            #         antFlag = False
            # dds = ordinal.find_all("dd")
            # for i,dd in enumerate(dds):
            #     r1 = dd.find_all("a", attrs={'class':'word'})
            #     for r in r1:
            #         if i in Syn:
            #             Synon.append(r.text)
            #         if i in Ant:
            #             Anton.append(r.text)

    # if len(Synon) == 0:
    #     Synon = ["Can't","find","any"]
    # if len(Anton) == 0:
    #     Anton = ["Can't","find","any"]

    print(word)
    print(shortDescription)
    print(longDescription)
    print(', '.join(FinalDefs))
    print(', '.join(sum(Synon, [])))
    print(', '.join(sum(Anton, [])))

    tempDf = pd.DataFrame({
        'Word' : [word],
        'ShortDefinition' : [shortDescription],
        'LongDefinition' : [longDescription],
        'Meaning' : [', '.join(FinalDefs)],
        'Synonyms' : [', '.join(sum(Synon, []))],
        'Antonyms' : [', '.join(sum(Anton, []))]
    })

    FinalDataFrame = pd.concat([FinalDataFrame,tempDf])

FinalDataFrame = FinalDataFrame[['Word','Meaning','ShortDefinition','LongDefinition','Synonyms','Antonyms']]
FinalDataFrame.head()
FinalDataFrame.to_csv("Vocabulary.csv")
print("------------------- DONE ------------------")