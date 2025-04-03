import streamlit as st
import pickle
import pandas as pd


from movie_utils import fetch_poster


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


if 'id' in movies.columns:
    column_name = 'id'
elif 'movie_id' in movies.columns:
    column_name = 'movie_id'
else:
    st.error("❌ Error: No valid 'id' column found in movies DataFrame!")
    st.stop()


def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:]  # Consider more movies

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]][column_name]
        try:
            poster_url = fetch_poster(movie_id)
            if isinstance(poster_url, str) and poster_url.startswith("http"):
                recommended_movies.append(movies.iloc[i[0]]['title'])
                recommended_posters.append(poster_url)

            if len(recommended_movies) == 5:
                break
        except Exception as e:
            continue

    return recommended_movies, recommended_posters

# Streamlit UI
st.title('🎬 Movie Recommender System')

option = st.selectbox('Enter movie name?', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(option)

    if not names:
        st.error("❌ No recommendations found with available posters. Try another movie!")
    else:
        cols = st.columns(len(names))

        for col, name, poster in zip(cols, names, posters):
            with col:
                st.image(poster, caption=name, use_container_width=True)