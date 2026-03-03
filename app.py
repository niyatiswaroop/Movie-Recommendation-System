import streamlit as st
import pickle
import requests 
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

# Load saved model files
movies = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": API_KEY,
            "language": "en-US"
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            poster_path = data.get("poster_path")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"

        return None

    except:
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0E1117;
}

/* Title colors */
h1 {
    color: white !important;
}

h2, h3 {
    color: #E50914 !important;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Normal text */
p, label {
    color: white !important;
}
            
.movie-title {
    text-align: center;
    font-weight: 600;
    font-size: 16px;
    margin-top: 10px;
    color: #ffffff;
    opacity: 0.95;
}            

/* Selectbox main field */
div[data-baseweb="select"] > div {
    background-color: #1c1f26 !important;
    color: white !important;
    border-radius: 8px;
}

/* Dropdown menu options */
ul {
    background-color: #1c1f26 !important;
}

li {
    color: white !important;
}

/* Button styling */
.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 8px 20px;
}

.stButton>button:hover {
    background-color: #b20710;
    color: white;
}

.block-container {
    padding-top: 2rem;
}
            
/* Movie card hover effect */
.movie-card {
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.3s ease;
}

.movie-card:hover {
    transform: scale(1.08);
}

.movie-poster {
    width: 100%;
    border-radius: 12px;
}
            
.movie-meta {
    text-align: center;
    font-size: 14px;
    color: #bbbbbb;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;'>🎬 Movie Recommendation System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:gray;'>Discover movies similar to your favorites</p>",
    unsafe_allow_html=True
)

st.write("")

st.markdown("### 🎥 Choose a Movie")

selected_movie = st.selectbox(
    "",
    movies['title'].values
)

if st.button("Recommend"):
    with st.spinner("Finding best matches for you..."):
        recommendations, posters = recommend(selected_movie)

    st.markdown("## Top Picks For You")
    st.write("")

    cols = st.columns(5)
    placeholder_path = "assets/placeholder.jpg"

    for idx, col in enumerate(cols):
        with col:
            image_url = posters[idx] if posters[idx] else None

            if image_url:
                st.markdown(
                    f"""
                    <div class="movie-card">
                        <img src="{image_url}" class="movie-poster"/>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # For local placeholder image
                st.image("assets/placeholder.jpg", use_container_width=True)

            st.markdown(
                f"""
                <div class="movie-title">
                    {recommendations[idx]}
                </div>
                """,
                unsafe_allow_html=True
            )