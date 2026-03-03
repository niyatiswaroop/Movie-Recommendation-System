# 🎬 Movie Recommendation System

A content-based movie recommendation system that suggests similar movies using metadata such as genres, cast, crew, keywords, and overview.

The project includes a Streamlit-based web interface and integrates the TMDB API to display movie posters.

---

## 🚀 Features

- Content-based filtering using movie metadata  
- NLP preprocessing (tokenization, stemming, lowercasing)  
- Feature extraction using CountVectorizer  
- Cosine similarity for recommendation generation  
- Top 5 similar movie recommendations  
- TMDB poster integration  
- Optimized poster fetching using caching  
- Clean modular architecture (model + UI separation)

---

## 🧠 How It Works

1. Movie and credits datasets are merged.
2. Important metadata is combined into a single **tags** feature.
3. Text is preprocessed and vectorized.
4. Cosine similarity is computed between movie vectors.
5. The system recommends the most similar movies.
6. Posters are fetched dynamically from TMDB.

---

## 📁 Project Structure

```
├── app.py              # Streamlit frontend
├── build_model.py      # Builds similarity model & saves pickle files
├── recommender.py      # Core recommendation logic
├── main.py             # CLI version (terminal-based runner)
├── model/
│   ├── movies.pkl      # Preprocessed movie data
│   └── similarity.pkl  # Cosine similarity matrix
├── data/               # TMDB dataset files
├── assets/             # Placeholder images
├── requirements.txt    # Project dependencies
└── .env                # API key (not pushed to GitHub)
```

---

## 🛠️ Tech Stack

- Python  
- Pandas  
- NumPy  
- Scikit-learn  
- NLTK  
- Streamlit  
- Requests  
- Pickle  

---

## ⚙️ Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the root directory and add:

```
TMDB_API_KEY=your_api_key_here
```

---

## ▶️ How to Run

### 1️⃣ Build the Model (Required First Step)

```bash
python build_model.py
```

This generates:
- `model/movies.pkl`
- `model/similarity.pkl`

---

### 2️⃣ Launch the Streamlit App

```bash
streamlit run app.py
```

---

### 3️⃣ (Optional) Run CLI Version

```bash
python main.py
```

---

## 📌 Notes

- The API key is stored securely using environment variables.
- The system uses content-based filtering (no collaborative filtering).
- Poster API calls are optimized using caching and constant-time lookups.