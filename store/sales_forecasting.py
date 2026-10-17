
def predict_next_month_sales(revenue_values):
    """
    Predict next month's revenue using a simple linear trend.
    Returns None if fewer than two revenue values are available.
    """

    values = [float(value) for value in revenue_values]

    n = len(values)

    if n < 2:
        return None

    # Months are represented as 1, 2, 3, ..., n.
    x_mean = (n + 1) / 2
    y_mean = sum(values) / n

    numerator = sum(
        (month - x_mean) * (revenue - y_mean)
        for month, revenue in enumerate(values, start=1)
    )

    denominator = sum(
        (month - x_mean) ** 2
        for month in range(1, n + 1)
    )

    if denominator == 0:
        return round(y_mean, 2)

    slope = numerator / denominator
    prediction = y_mean + slope * ((n + 1) - x_mean)

    return round(float(prediction), 2)
