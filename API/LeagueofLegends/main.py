import api

df= api.getAPI('Ditto Dihoo')
df.to_csv('data.csv',index=False)