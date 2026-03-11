from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your TMDb API key
API_KEY = "7f7e6f9e346845408274aa6ec88ecdc6"

# Language options
languages = {
    "English": "en",
    "Hindi": "hi",
    "Malayalam": "ml"
}

# Genre list
genres = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Sci-Fi": 878,
    "TV Movie": 10770,
    "Thriller": 53,
    "War": 10752,
    "Western": 37
}


@app.route("/", methods=["GET", "POST"])
def home():

    movies = []
    selected_language = None
    selected_genres = []

    if request.method == "POST":

        selected_language = request.form.get("language")
        selected_genres = request.form.getlist("genres")

        genre_ids = ",".join([str(genres[g]) for g in selected_genres])

        url = "https://api.themoviedb.org/3/discover/movie"

        params = {
            "api_key": API_KEY,
            "with_original_language": selected_language
        }

        if genre_ids:
            params["with_genres"] = genre_ids

        response = requests.get(url, params=params)
        data = response.json()

        for movie in data.get("results", [])[:10]:
            movies.append({
                "id": movie["id"],
                "title": movie.get("title"),
                "overview": movie.get("overview"),
                "rating": movie.get("vote_average"),
                "release": movie.get("release_date")
            })

    return render_template(
        "index.html",
        movies=movies,
        genres=genres,
        languages=languages,
        selected_language=selected_language,
        selected_genres=selected_genres
    )


@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):

    # Get cast
    cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    cast_data = requests.get(cast_url, params={"api_key": API_KEY}).json()

    cast = [c["name"] for c in cast_data.get("cast", [])[:5]]

    # Get trailer
    video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
    video_data = requests.get(video_url, params={"api_key": API_KEY}).json()

    trailer = None

    for v in video_data.get("results", []):
        if v["site"] == "YouTube" and v["type"] in ["Trailer", "Teaser"]:
            trailer = "https://www.youtube.com/watch?v=" + v["key"]
            break

    return jsonify({
        "cast": cast,
        "trailer": trailer
    })


if __name__ == "__main__":
    app.run(debug=True)