from typing import List
import pandas as pd
import pickle
from scipy import spatial
import numpy as np


# establish a cache of embeddings to avoid recomputing
# cache is a dict of tuples (bookId, model) -> embedding, saved as a pickle file

# set path to embedding cache
embedding_cache_path = "data/description_embeddings_cache.pkl"

# load the cache if it exists, and save a copy to disk
try:
    embedding_cache = pd.read_pickle(embedding_cache_path)
except FileNotFoundError:
    embedding_cache = {}
with open(embedding_cache_path, "wb") as embedding_cache_file:
    pickle.dump(embedding_cache, embedding_cache_file)



def get_embedding_local(client, text: str, engine="text-embedding-ada-002") -> List[float]:

    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    res = client.embeddings.create(
        model=engine,
        input=[text],
        encoding_format="float"
    )
    return res.data[0].embedding


# define a function to retrieve embeddings from the cache if present, and otherwise request via the API
def embedding_from_string(
    client,
    book_ids_descriptions,
    model: str = "text-embedding-ada-002",
    embedding_cache=embedding_cache
) -> list:
    
    for id, string in book_ids_descriptions:
        """Return embedding of given string, using a cache to avoid recomputing."""
        if string and (id, model) not in embedding_cache.keys():
            embedding_cache[(id, model)] = get_embedding_local(client, string, model)
            with open(embedding_cache_path, "wb") as embedding_cache_file:
                pickle.dump(embedding_cache, embedding_cache_file)
    return (embedding_cache)



def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances

def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
    """Return a list of indices of nearest neighbors from a list of distances."""
    return np.argsort(distances)

def recommendations_from_descriptions(
    client, 
    book_dictionary,
    book_ids_descriptions,
    model="text-embedding-ada-002",
    k_nearest_neighbors: int = 6,
    ) -> List[int]:
        
        # get embeddings for all strings
    embeddings = embedding_from_string(client, book_ids_descriptions, model=model)

    # get the embedding of the source string
    query_id = book_dictionary['bookId']
    query_model = model
    query_embedding = embeddings[(query_id, query_model)]

    # get distances between the source embedding and other embeddings (function from embeddings_utils.py)
    distances = distances_from_embeddings(query_embedding, embeddings.values(), distance_metric="cosine")

    # get indices of nearest neighbors (function from embeddings_utils.py)
    indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)

    suggested_books = []
    embeddings_keys = list(embeddings.keys())
    # Looping the knn indicies, ordered
    for index in indices_of_nearest_neighbors:
        # check the number of suggested books returned
        if len(suggested_books) < k_nearest_neighbors:
            # bookId extraction for all the 6 suggested books
            book_id = embeddings_keys[index][0]
            if book_id != query_id:
                suggested_books.append(book_id)
        else:
            break

    return suggested_books




