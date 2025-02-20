import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    if 'poster_path' in data and data['poster_path']:  # Check if poster exists
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation function
def recommand(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    recomanded_movies = []
    recomanded_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recomanded_movies.append(movies.iloc[i[0]].title)
        recomanded_movies_poster.append(fetch_poster(movie_id))

    return recomanded_movies, recomanded_movies_poster  # Return both names and posters


# Load the pickled data
movie_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Streamlit UI ---
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for better styling
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background: linear-gradient(to right, #141e30, #243b55);
        }
        .stSelectbox label {
            font-size: 20px;
            font-weight: bold;
            color: #FFD700;
        }
        .stButton button {
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            color: white;
            border-radius: 10px;
            font-size: 18px;
            padding: 8px 20px;
            transition: 0.3s ease-in-out;
        }
        .stButton button:hover {
            transform: scale(1.1);
            background: linear-gradient(to right, #ff4b2b, #ff416c);
        }
        .movie-container {
            text-align: center;
        }
        .movie-container img {
            border-radius: 12px;
            box-shadow: 0px 5px 15px rgba(255, 255, 255, 0.3);
            transition: 0.3s ease-in-out;
        }
        .movie-container img:hover {
            transform: scale(1.1);
        }
        .movie-title {
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
            color: #FFD700;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎬 Movie Recommendation System 🎥</h1>", unsafe_allow_html=True)

# Movie selection dropdown
selected_movie_name = st.selectbox(
    '🎞️ Select a movie you like:',
    movies['title'].values
)

st.write("")  # Spacer

# Recommend button
if st.button('🔍 Get Recommendations'):
    names, posters = recommand(selected_movie_name)

    # Create a row layout with movie cards
    cols = st.columns(9)  # 5 columns for 5 recommended movies
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="movie-container">
                    <img src="{posters[idx]}" width="160">
                    <p class="movie-title">{names[idx]}</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><p style='text-align: center; color: lightgray;'>✨ Built with ❤️ by Movie Enthusiasts ✨</p>", unsafe_allow_html=True)
