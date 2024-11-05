import pandas as pd


file = 'Frequency List.xlsx'
sheetname = 'The List - Frequency List'
df = pd.read_excel(file, sheetname)



print(df.loc[df['POS'] == 'v'])