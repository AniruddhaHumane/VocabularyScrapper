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

WordList = open("WordList.txt").read().split(", ")
url = "https://www.vocabulary.com/dictionary/"
print(len(WordList))

FinalDataFrame = pd.DataFrame(columns=['Word','ShortDefinition','LongDefinition','Meaning','Synonyms','Antonyms'])
checkWord = ["chastise"]
for word in checkWord:
    page = urlopen(url+word)
    print("URL Opened")

    formattedPage = BeautifulSoup(page, "lxml")
    print("Page Formatted")

    word = formattedPage.find("h1", attrs={'class':'dynamictext'}).text

    shortDescription = formattedPage.find("p", attrs={'class':'short'}).text

    longDescription = formattedPage.find("p", attrs={'class':'long'}).text

    FinalDefs = []
    Synon = []
    Anton = []

    definitionGroups = formattedPage.find_all("div", attrs={'class':'group'})

    # Sentences = formattedPage.find_all("div", attrs={'class':'sentence'})
    # print(Sentences)

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
            for dl in dls:
                synAnt = dl.find("dt")
                if synAnt.text == "Synonyms:":
                    Synon.append([ i.text for i in dl.find_all("a", attrs={'class':'word'})])
                elif synAnt.text == "Antonyms:":
                    Anton.append([ i.text for i in dl.find_all("a", attrs={'class':'word'})])

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
        # 'Sentence' : ['; '.join(Sentences)]
    })

    FinalDataFrame = pd.concat([FinalDataFrame,tempDf])

FinalDataFrame = FinalDataFrame[['Word','Meaning','ShortDefinition','LongDefinition','Synonyms','Antonyms']]
FinalDataFrame.head()
FinalDataFrame.to_csv("Vocabulary.csv")
print("------------------- DONE ------------------")