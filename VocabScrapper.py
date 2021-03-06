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
import time
import json

WordList = open("WordList.txt").read().split(",")
url = "https://www.vocabulary.com/dictionary/"
print(len(WordList))

FinalDataFrame = pd.DataFrame(columns=['Word','ShortDefinition','LongDefinition','Meaning','Synonyms','Antonyms'])


doneIndex = ""
with open('doneList.txt', 'r') as f:
    doneIndex = f.read()
flag = False


#checkWord = [#"bona fide"]

for i,word in enumerate(WordList):
    if(i != (0 if doneIndex == '' else int(doneIndex)+1) and flag is False):
        continue
    flag = True
    page = urlopen(url+word.lower())
    #print("URL Opened")

    formattedPage = BeautifulSoup(page, "lxml")
    #print("Page Formatted")

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

    
    # Vocabulary.com corpus api
    sentences = urlopen('https://corpus.vocabulary.com/api/1.0/examples.json?query='+word)
    sentences = json.load(sentences)
    sents = []
    sents.append(sentences["result"]["sentences"][0]["sentence"])
    sents.append(sentences["result"]["sentences"][1]["sentence"])
    
    
    # mnemonics dictionary
    mnPage = urlopen('https://mnemonicdictionary.com/?word='+word)
    mnFormatted = BeautifulSoup(mnPage, "lxml")
    mns = mnFormatted.find_all("div", attrs={'class':'card-text'})
    
    mnemonics = []
    if len(mns) is not 0:
        mnemonics.append(' '.join(mns[0].find("p").text.strip().split()))
        
    print("---------------------------------------------------------------------------------------------------------------------------------")   
    print(word)
    print()
    print(shortDescription)
    print()
    print(longDescription)
    print()
    print(', '.join(FinalDefs))
    print()
    print(', '.join(sum(Synon, [])))
    print()
    print(', '.join(sum(Anton, [])))
    print()
    print(', '.join(sents))
    print()
    print(', '.join(mnemonics))
    print()
    print("---------------------------------------------------------------------------------------------------------------------------------")   

    tempDf = pd.DataFrame({
    'Category': ["Barrons"],
    'Word' : [word],
    'ShortDefinition' : [shortDescription],
    #'LongDefinition' : [longDescription.encode("utf-8")],
    'LongDefinition' : [longDescription],
    'Meaning' : [', '.join(FinalDefs)],
    'Synonyms' : [', '.join(sum(Synon, []))],
    'Antonyms' : [', '.join(sum(Anton, []))],
    'Mnemonic' : [', '.join(mnemonics)],
    'Sentence' : [', '.join(sents)]
    })

    tempDf = tempDf[['Category','Word','ShortDefinition','LongDefinition','Meaning','Synonyms','Antonyms','Mnemonic','Sentence']]
    # tempDf.to_csv("Vocabulary.csv")
    with open('vocab.csv', 'a') as f:
        tempDf.to_csv(f, header=False)
    # FinalDataFrame = pd.concat([FinalDataFrame,tempDf])

    with open('doneList.txt', 'w') as f:
        f.write(str(i))

FinalDataFrame = FinalDataFrame[['Word','Meaning','ShortDefinition','LongDefinition','Synonyms','Antonyms']]
FinalDataFrame.head()
FinalDataFrame.to_csv("Vocabulary.csv")
print("------------------- DONE ------------------")

# Next Steps to clean the CSV
#
# import ast
# import pandas as pd
# df = pd.read_csv('vocab.csv',header=None)
# df[3] = df[3].apply( x : ast.literal_eval(x).decode('utf-8'))

# Excel formula to concatenate
# =CONCATENATE(A:A,"||","Small Def : ",B:B&CHAR(10)&CHAR(10),"Long Def : ",C:C&CHAR(10)&CHAR(10),"Definitions : ",D:D&CHAR(10)&CHAR(10),"Synonyms : ",E:E&CHAR(10)&CHAR(10),"Antonyms : ",F:F&CHAR(10)&CHAR(10),"Mnemonic : ",G:G&CHAR(10)&CHAR(10),"Sentence : ",H:H,"||||")

'''
##### QUIZLET LEARN SCREEN EXPANDING SCRIPT
 document.getElementsByClassName("SiteHeaderWrapper")[0].remove();
 document.getElementsByClassName("UIContainer")[0].style.maxWidth = "100%";
 document.getElementsByClassName("ModeLayout-ad")[0].remove();
 document.getElementsByClassName("ModeLayout")[0].style.cssText = 'top: 0 !important';
 document.getElementsByClassName("ModeLayout-controls")[0].style.top = "0";
 document.getElementsByClassName("AssistantViewController")[0].style.cssText = "font-size: 1.5rem; max-height: 100%;";
 document.getElementsByClassName("FormattedText")[0].style.marginTop = 0;
 document.getElementsByClassName("FormattedText")[0].style.height = "100%";
 document.getElementsByClassName("FormattedText")[1].style.marginTop = 0;
 document.getElementsByClassName("FormattedText")[1].style.height = "100%";

#### This much is fine... I just find scrollbars irritating in flashcards so I remove them...

 var styles = `
  html {
      overflow: scroll;
      overflow-x: hidden;
  }
  ::-webkit-scrollbar {
      width: 0px;  /* Remove scrollbar space */
      background: transparent;  /* Optional: just make scrollbar invisible */
  }
 /* Optional: show position indicator on hover */
  ::-webkit-scrollbar-thumb {
      background: rgba(0,0,0,0);
  }
  `
  var styleSheet = document.createElement("style")
  styleSheet.style = "text/css"
  styleSheet.innerText = styles
  document.head.appendChild(styleSheet)
'''
