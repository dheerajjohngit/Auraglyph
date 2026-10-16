import pandas as pd

from sklearn.cluster import KMeans

from .models import Order

from django.contrib.auth.models import User


def get_customer_segments():

    users = User.objects.all()

    data = []

    for user in users:

        orders = Order.objects.filter(
            user=user
        )

        total_orders = orders.count()

        total_spent = sum(
            order.total_amount
            for order in orders
        )

        data.append([
            user.username,
            total_orders,
            float(total_spent)
        ])

    if len(data) < 3:

        return {

            'high_value': 0,

            'regular': 0,

            'new': len(data)
        }

    df = pd.DataFrame(
        data,
        columns=[
            'username',
            'orders',
            'spent'
        ]
    )

    kmeans = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    df['cluster'] = kmeans.fit_predict(
        df[['orders', 'spent']]
    )

    cluster_spending = df.groupby(
        'cluster'
    )['spent'].mean()

    sorted_clusters = cluster_spending.sort_values()

    new_cluster = sorted_clusters.index[0]

    regular_cluster = sorted_clusters.index[1]

    high_cluster = sorted_clusters.index[2]

    return {

        'high_value': (
            df['cluster'] == high_cluster
        ).sum(),

        'regular': (
            df['cluster'] == regular_cluster
        ).sum(),

        'new': (
            df['cluster'] == new_cluster
        ).sum()
    }