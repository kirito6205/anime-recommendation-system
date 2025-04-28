# recommendation.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define the recommendation function
def get_recommendations(selected_genre, top_n=10):
    # Load the anime dataset
    df = pd.read_csv('dataset/anime-dataset-2023.csv')

    # Fill missing values
    df['Genres'] = df['Genres'].fillna('')
    df['Synopsis'] = df['Synopsis'].fillna('')

    # Filter only those anime that match the selected genre
    genre_filtered = df[df['Genres'].str.contains(selected_genre, case=False, na=False)]

    # If no anime matches the genre, return empty list
    if genre_filtered.empty:
        return []

    # Combine 'Genres' and 'Synopsis' into a single feature for content-based filtering
    genre_filtered['content'] = genre_filtered['Genres'] + ' ' + genre_filtered['Synopsis']

    # Apply TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(genre_filtered['content'])

    # Calculate cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Sort by Popularity (ascending means more popular)
    sorted_animes = genre_filtered.sort_values(by='Popularity', ascending=True)

    # Build the final recommendations list
    recommendations = []
    for _, row in sorted_animes.head(top_n).iterrows():
        recommendations.append({
            'name': row['Name'],
            'genre': row['Genres'],
            'score': row['Score'],
            'synopsis': row['Synopsis'],
            'image_url': row['Image URL']
        })

    return recommendations
    
