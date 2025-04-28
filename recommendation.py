
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('dataset/anime-dataset-2023.csv')

df['Genres'] = df['Genres'].fillna('')
df['Synopsis'] = df['Synopsis'].fillna('')

df['content'] = df['Genres'] + ' ' + df['Synopsis']

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['content'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df.index, index=df['Name']).drop_duplicates()

def get_recommendations(selected_genre, top_n=10):
    genre_filtered = df[df['Genres'].str.contains(selected_genre, case=False, na=False)]
    if genre_filtered.empty:
        return []
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
