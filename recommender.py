import pickle
import pandas as pd

movies = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    # need to sort in reverse order so we can take top 5 movies with highest similarity
    # enumerate(similarity[0]) - creates tuples of similarities with their respective movie-id
    # list(...) - converts the array of tuples into a list of tuples
    # key=lambda x:x[1] - sorting on the basis of the second index - which is similarity - that too in reverse order (descending)
    # [1:6] - taking this so we can take top 5 movies (excluding 0th index- bec it is the same as the movie itself)

    rec_movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in rec_movies_list:
        movie_row = movies.iloc[i[0]]

        # Extract year safely
        if pd.notna(movie_row.release_date):
            year = movie_row.release_date[:4]
        else:
            year = "N/A"

        recommended_movies.append({
            "title": movie_row.title,
            "rating": movie_row.vote_average,
            "year": year
        })

    return recommended_movies