from .models import Product

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


def get_recommendations(product_id):

    products = Product.objects.all()

    if products.count() < 2:
        return []

    product_data = []

    for product in products:

        text = f"""
        {product.name}
        {product.category}
        {product.description}
        """

        product_data.append(text)

    vectorizer = TfidfVectorizer(
        stop_words='english'
    )

    tfidf_matrix = vectorizer.fit_transform(
        product_data
    )

    similarity_matrix = cosine_similarity(
        tfidf_matrix
    )

    product_list = list(products)

    current_index = None

    for i, product in enumerate(product_list):

        if product.id == product_id:

            current_index = i

            break

    if current_index is None:

        return []

    similarity_scores = list(
        enumerate(
            similarity_matrix[current_index]
        )
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommended_products = []

    for index, score in similarity_scores[1:5]:

        recommended_products.append(
            product_list[index]
        )

    return recommended_products