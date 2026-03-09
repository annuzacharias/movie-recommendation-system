import pandas as pd

# Load dataset
data = pd.read_csv("movies.csv")

def recommend_by_genre(genre):

    genre = genre.lower()

    # Find movies with matching genre
    filtered = data[data["genre"].str.lower().str.contains(genre)]

    if filtered.empty:
        return ["No movies found for this genre"]

    # Return movie titles
    return filtered["title"].head(5).tolist()