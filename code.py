import pandas as pd 
import matplotlib.pyplot as plt #type: ignore
import seaborn as sns #type: ignore
import ast

# Load the data

movies = pd.read_csv('X:\Data Analyst\Machine Learning\ProjectSpaces\Movie_RecommenderSystem\MovieRecomendationSystemDataset\movies.csv')
credits = pd.read_csv('X:\Data Analyst\Machine Learning\ProjectSpaces\Movie_RecommenderSystem\MovieRecomendationSystemDataset\credits.csv')


# merging the two dataframes

movies = movies.merge(credits, on='title')


# columns in the dataset

# 'budget', 'genres', 'homepage', 'id', 'keywords', 'original_language','original_title', 'overview', 'popularity', 'production_companies',
# 'production_countries', 'release_date', 'revenue', 'runtime',
# 'spoken_languages', 'status', 'tagline', 'title', 'vote_average',
# 'vote_count', 'movie_id', 'cast', 'crew'


# coloumns to be used for the recommendation system

# 'id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew'


movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# print(movies.info())

  # checking for missing values
# print(movies.isnull().sum())

  # filling the missing values
movies.dropna(inplace=True)

  # checking duplicates
# print(movies.duplicated().sum())
  # no duplicates
  
  
#  preprocessing the data

# print(movies['genres'][0]) # [{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]

# converting it into a list of genres  # ['Action', 'Adventure', 'Fantasy', 'Science Fiction']

def convert(text):
    List = []
    for i in ast.literal_eval(text):
            List.append(i['name'])
    return List

movies['genres'] = movies['genres'].apply(convert)

    
def convert_cast(text):
            List = []
            counter = 0
            for i in ast.literal_eval(text):
                        if counter < 3:
                         List.append(i['name'])
                         counter+=1
                        else:
                         break
            return List

movies['cast'] = movies['cast'].apply(convert_cast)

def convert_crew(text):
            List = []
            for i in ast.literal_eval(text):
                        if i['job'] == 'Director':
                            List.append(i['name'])
                            break
            return List

movies['crew'] = movies['crew'].apply(convert_crew)
movies['keywords'] = movies['keywords'].apply(convert)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# removing spaces between the names ex : 'Tom Hanks' -> 'TomHanks'
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])


#  making tags 

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# lowercasing the tags

new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())


# now vectorizing the tags

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=5000, stop_words='english')

vector = cv.fit_transform(new_df['tags']).toarray()

# now ['love','loving','loved'] will be considered as one word 'love'

from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def stem(text):
            y = []
            for i in text.split():
             y.append(ps.stem(i))
            return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

# now finding the cosine similarity between the tags of the movies for the recommendation system

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vector)


def recommand(movie):
            movie_index = new_df[new_df['title'] ==movie].index[0]
            distances = similarity[movie_index]
            movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
            for i in movies_list:
             print(new_df.iloc[i[0]].title)
             
# recommand()

import pickle 
pickle.dump(new_df.to_dict(), open('movie_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))