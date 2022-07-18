from abc import ABC, abstractmethod
from pandas import DataFrame


class RecommendCoffeeInterface(ABC):

    @abstractmethod
    async def transform_data_to_df(self):
        ...

    @abstractmethod
    def recommend_coffee(self, title: str, count_of_coffee_recommend: int = 10):
        ...

    @abstractmethod
    def prepare_index(self, dataframe: DataFrame):
        ...

    @abstractmethod
    def prepare_tfidf_matrix(self, documents: str, stop_words: str = 'english'):
        ...

    @abstractmethod
    def calculate_cosine_sim(self, tfidf_matrix1, tfidf_matrix_2):
        ...

    @abstractmethod
    def preprocessing_dataframe(self):
        ...
