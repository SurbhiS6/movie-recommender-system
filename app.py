import pickle
import streamlit as st
import pandas as pd
import requests



##__creating_title_of_the_app__##

st.title('Movie Recommender System')


##__Reading_movies_pickle_file__##

movies = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies)

##__Reading_similarity_pickle_file__##

similarity = pickle.load(open('similarity.pkl','rb'))


##__creating_a_DropDown_Menu__##

movie_selected = st.selectbox('Pick your choice of movie', movies['title'].values)
print(type(movie_selected))


###__adding_in_movies_posters__###

def get_poster(imdb_id):
    url = f'http://www.omdbapi.com/?i={imdb_id}&apikey=51180bca'
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("Poster")

    
    return None


##__creating_function_to_pass_list_of_recommended_movies__##

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    top_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in top_movies:
        imdb_id = movies.iloc[i[0]]['imdb_id']

        recommended_movies.append(movies.iloc[i[0]]['title'])

        #fetching poster using api 
        recommended_movies_posters.append(get_poster(imdb_id))

    return recommended_movies, recommended_movies_posters




##__adding_button__##

if st.button('Recommend Movies'):
    recommended_movies, recommended_movies_posters = recommend(movie_selected)
    
    ###__Displaying_Movie_Posters__###

    col0, col1, col2, col3, col4 = st.columns(5)

    with col0:
        st.image(recommended_movies_posters[0])
        st.text(recommended_movies[0])

    with col1:
        st.image(recommended_movies_posters[1])
        st.text(recommended_movies[1])
        
    with col2:
        st.image(recommended_movies_posters[2])
        st.text(recommended_movies[2])
        
    with col3:
        st.image(recommended_movies_posters[3])
        st.text(recommended_movies[3])
        
    with col4:
        st.image(recommended_movies_posters[4])
        st.text(recommended_movies[4])
        