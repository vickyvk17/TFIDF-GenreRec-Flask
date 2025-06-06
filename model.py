import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from difflib import get_close_matches

class MovieRecommender:
    def __init__(self, data_path="Scrapped_imdb_data.csv"):
        self.data = self._load_and_preprocess(data_path)
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self._build_tfidf_model()
        self.indices = pd.Series(self.data.index, index=self.data['Title']).drop_duplicates()
    
    def _load_and_preprocess(self, data_path):
        data = pd.read_csv(data_path)
        data.dropna(inplace=True)
        data['Year'] = data['Year'].astype(int)
        return data
    
    def _build_tfidf_model(self):
        return self.tfidf.fit_transform(self.data['Genre'])
    
    def get_recommendations(self, title, num_recommendations=5):
        matches = get_close_matches(title, self.indices.index, n=1, cutoff=0.3)
        if not matches:
            return None, f"Movie '{title}' not found. Did you mean: {self.indices.sample(3).index.tolist()}"
        
        corrected_title = matches[0]
        idx = self.indices[corrected_title]
        
        cosine_sim = linear_kernel(self.tfidf_matrix[idx:idx+1], self.tfidf_matrix).flatten()
        sim_scores = list(enumerate(cosine_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        top_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]
        
        recommendations = []
        for i in top_indices:
            movie = self.data.iloc[i]
            recommendations.append({
                'Title': movie['Title'],
                'Year': movie['Year'],
                'Rating': movie['Rating'],
                'Genre': movie['Genre'],
                'Top_cast': eval(movie['Top_cast'])[:5]  # Get first 5 cast members
            })
        
        return recommendations, corrected_title