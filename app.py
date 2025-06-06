from flask import Flask, render_template, request
from model import MovieRecommender
import os

app = Flask(__name__)

# Initialize the recommender system
recommender = MovieRecommender()

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    original_title = ""
    if request.method == 'POST':
        title = request.form['movie_name'].strip()
        try:
            num_rec = int(request.form['num_recommendations'])
        except ValueError:
            return render_template('index.html', 
                                error="Please enter a valid number",
                                recommendations=recommendations,
                                original_title=original_title)
        
        recommendations, original_title = recommender.get_recommendations(title, num_rec)
        if not recommendations:
            return render_template('index.html', 
                                error=original_title,  # In this case, original_title contains the error message
                                recommendations=[],
                                original_title="")
    
    return render_template('index.html', 
                         recommendations=recommendations,
                         error=None,
                         original_title=original_title)

if __name__ == '__main__':
    app.run(debug=True)