import numpy as np
import pandas as pd
import ast
import pickle

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# selecting all columns that are suitable for a content-based recommender system - genres, id (for movie posters), keywords, title, overview, cast, crew
# not taking numeric values into consideration as it will disturb our current workflow
# not selecting original_language as an important factor - majority is 'english' - so the data is imbalanced (or highly dominated by one category)

movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

movies = movies.merge(credits, on='title')

movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew', 'vote_average', 'release_date']]

# checking missing values
movies.dropna(inplace=True)

# checking for duplicate data
movies.duplicated().sum()


# output is a string of list of dictionaries
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
# ast.literal_eval(obj) converts the string into a list


movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)


def castExtract3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L


movies['cast'] = movies['cast'].apply(castExtract3)


def crewExtractDirector(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L


movies['crew'] = movies['crew'].apply(crewExtractDirector)

# the lambda function splits each row into separate words and stores it in a list
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Applying transformation - removing all the spaces in each element in the list so that they are considered as one single entity (easy for making recommendations)
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# creating a new dataframe with only the required columns
preprocessed_df = movies[['movie_id','title','tags','vote_average','release_date']].copy()

# converting the list into string - tags column
preprocessed_df['tags'] = preprocessed_df['tags'].apply(lambda x: " ".join(x))

# converting all into lowercase
preprocessed_df['tags'] = preprocessed_df['tags'].apply(lambda x: x.lower())


# stemming converts similar words like ['loved' , 'loving', 'love'] to ['love', 'love', 'love']
# using library nltk- a famous library for nlp
ps = PorterStemmer()


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)  # returns a string


# nlp model reads sentences, not python lists
preprocessed_df['tags'] = preprocessed_df['tags'].apply(stem)


# Vectorization - converting tags into vectors (here, we are considering the top 5000 common words and also removing the english stopwords (to, the, of,etc)
# To convert the tags into vectors we use the library
cv = CountVectorizer(max_features=5000, stop_words='english')  # dropping the stopwords

# by default, the countvectorizer returns an object of sparse matrix, which we are then converting to a numpy array
vectors = cv.fit_transform(preprocessed_df['tags']).toarray()

# euclidean distance is not a reliable measure in a higher dimensional space (here, 5000 dimensions) - use cosine distance instead - theta b/w two vectors
# less theta= better
# distance is inversely proportional to similarity

# similarity lies b/w 0 and 1 - 1 implying a higher similarity
similarity = cosine_similarity(vectors)

# diagonal value will always be 1 in this case


# Save model files
pickle.dump(preprocessed_df, open('model/movies.pkl', 'wb'))
pickle.dump(similarity, open('model/similarity.pkl', 'wb'))

print("Model built and saved successfully!")