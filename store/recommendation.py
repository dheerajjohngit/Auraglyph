
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Product


@lru_cache(maxsize=1)
def _get_product_similarity():
    """
    Calculate product similarities once and cache the result.
    Clear the cache when product data changes.
    """
    products = list(Product.objects.all().order_by("id"))

    if len(products) < 2:
        return products, None

    product_data = [
        f"{product.name} {product.category} {product.description or ''}"
        for product in products
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=3000,
    )

    tfidf_matrix = vectorizer.fit_transform(product_data)

    # Keep the similarity matrix sparse to reduce memory usage.
    similarity_matrix = cosine_similarity(
        tfidf_matrix,
        dense_output=False,
    )

    return products, similarity_matrix


def get_recommendations(product_id):
    products, similarity_matrix = _get_product_similarity()

    if similarity_matrix is None:
        return []

    current_index = next(
        (
            index
            for index, product in enumerate(products)
            if product.id == product_id
        ),
        None,
    )

    if current_index is None:
        return []

    row = similarity_matrix.getrow(current_index)

    similarity_scores = sorted(
        zip(row.indices, row.data),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        products[index]
        for index, score in similarity_scores
        if index != current_index
    ][:4]


def clear_recommendation_cache():
    """Call this after adding, editing, or deleting products."""
    _get_product_similarity.cache_clear()
