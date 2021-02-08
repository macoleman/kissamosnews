import pandas as pd
df_crete = pd.read_csv("InfectionsCrete.csv", index_col=0)
df_greece = pd.read_csv("InfectionsGreece.csv", index_col=0)
#print(df_jan)

df_crete['Greece'] = df_greece['daily']
df_crete['Greece/100000'] = df_greece['Greece/100000']
print(df_crete)

df_crete.to_csv("InfectionsAll.csv")