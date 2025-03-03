from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

df = pickle.load(open('/home/meanzaza/mysite/df.pkl', 'rb'))

vector = TfidfVectorizer()
vector.fit(df['Content'])
tf = vector.transform(df['Content'])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', book_name = list(df['Title'].values), 
                           author = list(df['Authors'].values),
                           content = list(df['Content'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_book', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    n = 5 
    query_vec = vector.transform([user_input])

    scores = cosine_similarity(query_vec, tf).flatten()
    indices = scores.argsort()[-n:][::-1]
    recommended_books = df.iloc[indices][['Title','Authors','Content']]

    book_names = recommended_books['Title'].tolist()
    authors = recommended_books['Authors'].tolist()
    contents = recommended_books['Content'].tolist()


    return render_template('submitted.html',  book_names=book_names, authors=authors,
                           contents=contents)

if __name__ == '__main__':
    app.run(debug=True)