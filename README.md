# 🎬 Movie Recommendation System

This project implements a content-based movie recommendation system that suggests movies similar to a given movie using metadata features such as genres, cast, crew, keywords, and overview. The system applies text preprocessing and natural language processing techniques to convert movie information into numerical feature vectors and computes similarity scores to generate recommendations.

## 🚀 Features

- Content-based filtering using movie metadata
- Data preprocessing and feature engineering
- NLP preprocessing including tokenization and stemming
- Feature extraction using CountVectorizer
- Similarity computation using cosine similarity
- Top-5 movie recommendations based on similarity scores
- Model optimization using pickle for faster loading

## 🧠 How It Works

1. Movie and credits datasets are merged and cleaned.
2. Relevant metadata is extracted and combined into a single text feature (**tags**).
3. Text data is preprocessed using lowercasing and stemming.
4. CountVectorizer converts text into numerical vectors.
5. Cosine similarity is computed between movie vectors.
6. The system returns the most similar movies for a given input title.

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- NLTK
- Pickle

## 📂 Dataset

TMDB 5000 Movie Dataset containing movie metadata such as genres, cast, crew, keywords, and overview.

## ⚙️ Installation

Install the required libraries using pip:

pip install pandas numpy scikit-learn nltk

## ▶️ How to run the Project

First, run python build_model.py 

Then run pyhton main.py
