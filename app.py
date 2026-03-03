import streamlit as st
import pickle
import requests 
from dotenv import load_dotenv
import os
from recommender import recommend

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

# Load saved model files
movies = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Fast lookup for movie_id (O(1) instead of dataframe filtering)
movie_id_map = dict(zip(movies['title'], movies['movie_id']))

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    if not API_KEY:
        return None

    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"api_key": API_KEY},
            timeout=5  # reduced timeout for faster fail
        )

        if response.status_code != 200:
            return None

        data = response.json()
        poster_path = data.get("poster_path")

        if not poster_path:
            return None

        return f"https://image.tmdb.org/t/p/w500/{poster_path}"

    except requests.RequestException:
        return None

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap');

.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #E50914;
    margin-top: 30px;
    margin-bottom: 15px;
}

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

st.markdown('<div class="section-title">🎥 Choose a Movie</div>', unsafe_allow_html=True)

selected_movie = st.selectbox(
    "",
    movies['title'].values
)

if st.button("Recommend"):
    with st.spinner("Finding best matches for you..."):
        results = recommend(selected_movie)

    st.markdown('<div class="section-title">Top Picks For You</div>', unsafe_allow_html=True)
    st.write("")

    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            movie = results[idx]

            poster = fetch_poster(movie_id_map[movie['title']])

            # Poster
            if poster:
                st.markdown(
                    f"""
                    <div class="movie-card">
                        <img src="{poster}" class="movie-poster"/>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.image("assets/placeholder.jpg", use_container_width=True)

            # Title
            st.markdown(
                f"""
                <div class="movie-title">
                    {movie['title']}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Rating + Year
            st.markdown(
                f"""
                <div class="movie-meta">
                    ⭐ {movie['rating']} | {movie['year']}
                </div>
                """,
                unsafe_allow_html=True
            )