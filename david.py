import pandas as pd
artwork = pd.read_excel("ArtGalleryDataBase.xlsx", sheet_name="Artwork",skiprows=1)
transactions = pd.read_excel("ArtGalleryDataBase.xlsx", sheet_name="Transactions",skiprows=1) # read in data

# selects only the columns we need from the artwork dataframe and renames them, then merges with the transactions dataframe on the exhibitID and transactionPrice columns
final = artwork[['artID', 'price', 'exhibitID']].rename(columns={'price': 'transactionPrice'}).merge(transactions, on=['exhibitID', 'transactionPrice'], how='inner')
# marks the rows that are duplicates based on the exhibitID, artID, and transactionPrice columns. we keep the first instance of the duplicate and mark the rest as True
final['duplicate'] = final.duplicated(subset=['exhibitID', 'artID', 'transactionPrice'], keep='first')

# writes the dataframe to an excel file
final.to_excel("output.xlsx", index=False)