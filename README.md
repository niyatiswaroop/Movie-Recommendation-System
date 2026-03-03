# 🎬 Movie Recommendation System

This project implements a content-based movie recommendation system that suggests movies similar to a given movie using metadata features such as genres, cast, crew, keywords, and overview. The system applies text preprocessing and natural language processing techniques to convert movie information into numerical feature vectors and computes similarity scores to generate recommendations.

---

## 🚀 Features

- Content-based filtering using movie metadata  
- NLP preprocessing (tokenization, stemming, lowercasing)  
- Feature extraction using CountVectorizer  
- Cosine similarity for recommendation generation  
- Top 5 similar movie recommendations  
- Interactive Streamlit frontend  
- TMDB poster integration  
- Optimized model loading using pickle  

---

## 🧠 How It Works

1. Movie and credits datasets are merged.
2. Relevant metadata is combined into a single **tags** feature.
3. Text data is preprocessed and vectorized.
4. Cosine similarity is computed between movie vectors.
5. The system returns the most similar movies for a selected title.

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

## 📂 Dataset

TMDB 5000 Movie Dataset containing metadata such as genres, cast, crew, keywords, and overview.

---

## ⚙️ Installation

Install required dependencies:

```bash
pip install -r requirements.txt
