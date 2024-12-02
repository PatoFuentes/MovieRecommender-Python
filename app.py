import pandas as pd
from flask import Flask, render_template, request
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el dataset
file_path = 'movies.csv'
movies = pd.read_csv(file_path)

# Filtrar las 5 mejores películas por género según el campo 'score'
top_movies_per_genre = movies.sort_values(by='score', ascending=False).groupby('genre').head(5)

app = Flask(__name__)

@app.route('/')
def index():
    # Mostrar las mejores películas por género
    return render_template('index.html', movies=top_movies_per_genre)

@app.route('/filter', methods=['POST'])
def filter():
    # Obtener las películas seleccionadas por el usuario
    selected_movies = request.form.getlist('selected_movies')

    # Filtrar el dataset para obtener las películas seleccionadas
    selected_data = movies[movies['name'].isin(selected_movies)]

    # Buscar similitudes en los campos 'rating', 'genre', 'director', 'writer'
    recommendations = []
    similarity_scores = {}
    for _, movie in movies.iterrows():
        if movie['name'] in selected_movies:
            continue  # No incluir las películas seleccionadas en las recomendaciones

        score = 0
        for _, selected_movie in selected_data.iterrows():
            if movie['genre'] == selected_movie['genre']:
                score += 1
            if movie['rating'] == selected_movie['rating']:
                score += 1
            if movie['director'] == selected_movie['director']:
                score += 1
            if movie['writer'] == selected_movie['writer']:
                score += 1

        similarity_scores[movie['name']] = score

    # Ordenar las películas por la puntuación de similitud y seleccionar las 50 mejores
    sorted_recommendations = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)[:50]
    recommendations = [name for name, score in sorted_recommendations]

    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
