# import pandas as pd
# from urllib.request import urlopen
# from bs4 import BeautifulSoup

checkWord = ["amalgam"]
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

    # print(word)
    # print(shortDescription)
    # print(longDescription)
    # print(', '.join(FinalDefs))
    # print(', '.join(sum(Synon, [])))
    # print(', '.join(sum(Anton, [])))

    tempDf = pd.DataFrame({
        'Category': ["Common Words"],
        'Word' : [word],
        'ShortDefinition' : [shortDescription],
        'LongDefinition' : [longDescription.encode("utf-8")],
        'Meaning' : [', '.join(FinalDefs)],
        'Synonyms' : [', '.join(sum(Synon, []))],
        'Antonyms' : [', '.join(sum(Anton, []))],
        'Mnemonic' : [" "],
        'Sentence' : [" "]
    })

    tempDf = tempDf[['Category','Word','ShortDefinition','LongDefinition','Meaning','Synonyms','Antonyms','Mnemonic','Sentence']]
    with open('vocab.csv', 'a') as f:
        tempDf.to_csv(f, header=False)
    print("----------------------------- Done -----------------------------")





# Experiemt to append to xlsx


# tempDf = pd.DataFrame({
#         'lol': [""],
#         'Word' : ["word"],
#         'ShortDefinition' : ["shortDescription"],
#         'LongDefinition' : ["longDescription"],
#         'Meaning' : ["[', '.join(FinalDefs)]"],
#         'Synonyms' : ["[', '.join(sum(Synon, []))]"],
#         'Antonyms' : ["[', '.join(sum(Anton, []))]"],
#         'Mnemonic' : ["['; '.join(Sentences)]"],
#         'Sentence' : ["assssssssssssssss"]
#     })

# tempDf = tempDf[['lol','Word','ShortDefinition','LongDefinition','Meaning','Synonyms','Antonyms','Mnemonic','Sentence']]

# append_df_to_excel("vocab.xlsx",tempDf,"List")

# def append_df_to_excel(filename, df, sheet_name='Sheet1', startrow=None,
#                        truncate_sheet=False, 
#                        **to_excel_kwargs):
#     """
#     Append a DataFrame [df] to existing Excel file [filename]
#     into [sheet_name] Sheet.
#     If [filename] doesn't exist, then this function will create it.

#     Parameters:
#       filename : File path or existing ExcelWriter
#                  (Example: '/path/to/file.xlsx')
#       df : dataframe to save to workbook
#       sheet_name : Name of sheet which will contain DataFrame.
#                    (default: 'Sheet1')
#       startrow : upper left cell row to dump data frame.
#                  Per default (startrow=None) calculate the last row
#                  in the existing DF and write to the next row...
#       truncate_sheet : truncate (remove and recreate) [sheet_name]
#                        before writing DataFrame to Excel file
#       to_excel_kwargs : arguments which will be passed to `DataFrame.to_excel()`
#                         [can be dictionary]

#     Returns: None
#     """
#     from openpyxl import load_workbook

#     import pandas as pd

#     # ignore [engine] parameter if it was passed
#     if 'engine' in to_excel_kwargs:
#         to_excel_kwargs.pop('engine')

#     writer = pd.ExcelWriter(filename, engine='openpyxl')

#     # Python 2.x: define [FileNotFoundError] exception if it doesn't exist 
#     try:
#         FileNotFoundError
#     except NameError:
#         FileNotFoundError = IOError


#     try:
#         # try to open an existing workbook
#         writer.book = load_workbook(filename)

#         # get the last row in the existing Excel sheet
#         # if it was not specified explicitly
#         if startrow is None and sheet_name in writer.book.sheetnames:
#             startrow = writer.book[sheet_name].max_row

#         # truncate sheet
#         if truncate_sheet and sheet_name in writer.book.sheetnames:
#             # index of [sheet_name] sheet
#             idx = writer.book.sheetnames.index(sheet_name)
#             # remove [sheet_name]
#             writer.book.remove(writer.book.worksheets[idx])
#             # create an empty sheet [sheet_name] using old index
#             writer.book.create_sheet(sheet_name, idx)

#         # copy existing sheets
#         writer.sheets = {ws.title:ws for ws in writer.book.worksheets}
#     except FileNotFoundError:
#         # file does not exist yet, we will create it
#         pass

#     if startrow is None:
#         startrow = 0

#     # write out the new sheet
#     df.to_excel(writer, sheet_name, startrow=startrow,header=None, **to_excel_kwargs)

#     # save the workbook
#     writer.save()