from pandas import DataFrame
import pandas as pd

from recommender_system.interfaces.recommend_logic import \
    RecommendCoffeeInterface

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class RecommendCoffee(RecommendCoffeeInterface):
    """
        https://medium.com/geekculture/
            data-science-movie-recommendation-system-theory-and-simple-python-
                implementation-90e591106427
    """

    def __init__(self, coffee_collection):
        self.__coffee_collection = coffee_collection
        self.df = pd.DataFrame()

    async def transform_data_to_df(self):
        cursor = await self.__coffee_collection.find()
        coffees = [coffee async for coffee in cursor]
        self.df = pd.DataFrame(list(coffees))

    def prepare_index(self, dataframe: DataFrame):
        return pd.Series(dataframe.index, index=dataframe['title'])

    def prepare_tfidf_matrix(self, documents: str, stop_words: str = 'english'):
        tfidf = TfidfVectorizer(stop_words=stop_words)
        return tfidf.fit_transform(raw_documents=documents)

    def calculate_cosine_sim(self, tfidf_matrix1, tfidf_matrix_2):
        return cosine_similarity(tfidf_matrix1, tfidf_matrix_2)

    def preprocessing_dataframe(self):
        self.df['title'] = self.df['title'].fillna('')
        self.df['description'] = self.df['description'].fillna('')
        self.df['text'] = self.df['title'] + ' ' + self.df['description']

    def recommend_coffee(
            self, title: str, count_of_coffee_recommend: int = 10
    ):
        idx = self.prepare_index(dataframe=self.df)
        self.preprocessing_dataframe()
        tfidf_matrix = self.prepare_tfidf_matrix(documents=self.df['text'])
        cosine_sim = self.calculate_cosine_sim(tfidf_matrix, tfidf_matrix)
        sim_scores = list(enumerate(cosine_sim[idx[title]]))

        movie_indices = [
            x[0] for x in
            sorted(
                sim_scores, key=lambda x: x[1], reverse=True
            )[1:count_of_coffee_recommend + 1]
        ]
        return self.df['title'].iloc[movie_indices]
