
import pandas as pd
from sklearn.cluster import KMeans

from django.contrib.auth.models import User
from django.db.models import Count, Sum

from .models import Order


def get_customer_segments():
    # Fetch each user's order count and total spending in one query.
    users = User.objects.annotate(
        total_orders=Count("order", distinct=True),
        total_spent=Sum("order__total_amount"),
    ).values(
        "username",
        "total_orders",
        "total_spent",
    )

    data = [
        [
            user["username"],
            user["total_orders"] or 0,
            float(user["total_spent"] or 0),
        ]
        for user in users
    ]

    if len(data) < 3:
        return {
            "high_value": 0,
            "regular": 0,
            "new": len(data),
        }

    df = pd.DataFrame(
        data,
        columns=["username", "orders", "spent"],
    )

    # K-Means needs at least three customers for three clusters.
    features = df[["orders", "spent"]]

    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10,
    )

    df["cluster"] = model.fit_predict(features)

    cluster_spending = df.groupby("cluster")["spent"].mean()
    sorted_clusters = cluster_spending.sort_values()

    new_cluster = sorted_clusters.index[0]
    regular_cluster = sorted_clusters.index[1]
    high_cluster = sorted_clusters.index[2]

    return {
        "high_value": int((df["cluster"] == high_cluster).sum()),
        "regular": int((df["cluster"] == regular_cluster).sum()),
        "new": int((df["cluster"] == new_cluster).sum()),
    }
