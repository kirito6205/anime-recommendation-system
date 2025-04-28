import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(selected_genre, top_n=10):
    df = pd.read_csv('dataset/anime-dataset-2023.csv')

    # Fill missing values
    df['Genres'] = df['Genres'].fillna('')
    df['Synopsis'] = df['Synopsis'].fillna('')

    # Filter only matching genres early (save memory)
    genre_filtered = df[df['Genres'].str.contains(selected_genre, case=False, na=False)]

    if genre_filtered.empty:
        return []

    # Create content column for filtered dataset only
    genre_filtered['content'] = genre_filtered['Genres'] + ' ' + genre_filtered['Synopsis']

    # Apply TF-IDF and Cosine only on small filtered dataset
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(genre_filtered['content'])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Sort by popularity
    sorted_animes = genre_filtered.sort_values(by='Popularity', ascending=True)

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


