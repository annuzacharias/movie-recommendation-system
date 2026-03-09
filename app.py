from flask import Flask, render_template, request
from recommendation import recommend_by_genre

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    recs = []

    if request.method == "POST":
        genre = request.form["genre"]
        recs = recommend_by_genre(genre)

    return render_template("index.html", recommendations=recs)

if __name__ == "__main__":
    app.run(debug=True)