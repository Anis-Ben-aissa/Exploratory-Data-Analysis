


# importer les librairies (packages)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# steps:
# 1- importer la database
# 2-  extraire le dossier <archive>
!unzip movies.zip
# 3- livre le fichier csv " tmdb_movies_data.csv:    
df=pd.read_csv('movies_data.csv')

#1/ decouvrir la DB
df.head()

#2/ voir la taille de la data
df.shape

# 3/ verifier les type de chaque variable avant de commencer les calcules
df.info()

# 4) verifier les variable statestiques(numerique)
df.describe()

"""**Data cleaning (nettoyage des donnees)**"""

# verifier sil y a des donnees repeter (dupliquer)
df.duplicated().sum()

#supprimer la ligne qui est dupliquer:
df.drop_duplicates(inplace=True)
# verification:
df.duplicated().sum()

# decouverte des valeur manquante:
df.isnull().sum()

#supprimer les colinnes inutiles
## afficher les colonnes:
df.columns

# cree une liste avec les colunne a supprimer
deleted_columns=['id', 'imdb_id', 'budget', 'revenue',
       'cast', 'homepage', 'director', 'tagline', 'keywords', 'overview',
       'runtime', 'production_companies', 'release_date']
df.drop(deleted_columns,axis=1,inplace=True)
df.head()

# verifier les valeur manquante:
df.isnull().sum()

# on vas suprime les 23 lignes de la colonne "genres" avec valeur manquantes
df.dropna(inplace=True)
df.shape

# recodage de colonne "genre" car il y aplusieur valeurs exemple ( Action|Adventure|Science Fiction|Thriller)
# on vas considerer la 1er valeur
# on vas cree une liste list_genre
list_genre=[]
for i in df['genres']:
  i=i.split('|')
  list_genre.append(i[0])
df['genres_adj']=list_genre
df.head()



""">>> ma methode a corriger!!!

list_genre2=[]
for i in df['genres']:
    index=df['genres'].str.find('|')
    index.astype('int64')
    i=df['genres'].astype(str).str[:index]
    list_genre2.append(i)
list_genre2

**Analyse Exploratoire**
"""

# 1er etape analyse Univariee: etudier variable par variable

df['revenue_adj'].mean()

df['budget_adj'].mean()

df['vote_average'].mean()

df['vote_average'].unique() # pour voir comment evolue le vote
# rq: on ne peut pas la considerer comme une variable qualitative ordinale, on la considaire comme une variable numerique


df['genres_adj'].unique()

df['genres_adj'].value_counts()# pour voir les genre les plus populaire

# on peut aussi utiliser des visuels:
df['vote_average'].plot(kind='hist')
# donc on remarque que les votes sont a l'entour de 6

df['budget_adj'].plot(kind='hist')
# on remarque que il n'est pas equilibre car il y a  un grand ecart entre la valeur max et min

df['revenue_adj'].plot(kind='hist')
# on remarque que ily a une liaison entre le budget et le revenue

# 2eme etape Analyse Bivariee: on utilise la matrice de correlation entre les variable une a une
corr=df.corr()
sns.heatmap(corr,xticklabels=corr.columns,yticklabels=corr.columns,annot=True,cmap=sns.diverging_palette(220,20,as_cmap=True))
# rq plusque la valeur absolue de la corr est proche de 1 la correlations est conciderer forte
# ici le reveune a une correlation forre avec Budget,vote_count,popularity

# on examine la relation correlation entre le revenue et le budget avec un visuel nuage des points
df.plot(kind='scatter',x='budget_adj',y='revenue_adj')
#resultat: il y a une forte correlation entre les deux donc plus qu'on met de budget plus qu'on a de revenue(le nuage tend vers la droite)

# on examine l'impact de vote_averagecount sur le revenue
df.plot(kind='scatter',x='vote_average',y='revenue_adj')
# resultat il y a une correlation selon le nuage des points, lorsque les vote sont a l'entour de 7 courage les gens a voir le films ce qui augmente les revenues

"""Q1: Quel est le genre de film qui a un bon revenue ?"""

df_genre_rev=df.groupby(['genres_adj'])['revenue_adj'].mean().reset_index() # pour retourner en data frame as_index=False ou reset_index

df_genre_rev

df_genre_rev.columns

# pour mieux comprende on fait un visuel
df_genre_rev.plot(x='genres_adj',y='revenue_adj',kind='bar')
# avec le visuel on remarque que les film adventue,sience fiction on un bon budget par contre documentary et TV Movie n'on pas un bon budget

# on examine la correlation entre le genre et le budget
df_genre_budget=df.groupby(['genres_adj'],as_index=False)['budget_adj'].mean()
#df_genre_budget.plot(kind='bar')
df_genre_budget.plot(x='genres_adj',y='budget_adj',kind='bar')
# resultat la correlation est tres semblable avec celle de revenue, c'est la meme repartition.

# afficher tous sur le meme visuel:
plt.figure(figsize=(15,6))


x=df_genre_rev['genres_adj']
y=df_genre_rev['revenue_adj']
y2=df_genre_budget['budget_adj']

n=np.arange(len(x))
width1 = 0.25
plt.bar(n,y,label='revenue_adj', width=width1)
plt.bar(n + width1, y2,label='budget_adj', width=width1)

plt.xticks(rotation = '90')
plt.xticks(n + width1,x)# pour afficher les genres dans l'axe des x
#plt.xlabel(x)
plt.legend()
plt.tight_layout()
plt.show()

"""Q2 : Les caracterestiques des Films avec un bon revenu?"""

df.plot(kind='scatter',x='vote_average',y='revenue_adj')

df.plot(kind='scatter',x='budget_adj',y='revenue_adj')

"""***Conclusion : les films qui ont un tres bon revenue ce sont les films qui sont plus apprecie par les telespectateurs qui ont un vote a l'entour de 7 et un tres bon budget respectable.***"""



