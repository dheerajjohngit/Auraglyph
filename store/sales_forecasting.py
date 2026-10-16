from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_month_sales(revenue_values):

    if len(revenue_values) < 2:
        return None

    months = np.arange(
        1,
        len(revenue_values) + 1
    ).reshape(-1, 1)

    sales = np.array(revenue_values)

    model = LinearRegression()

    model.fit(months, sales)

    next_month = np.array(
        [[len(revenue_values) + 1]]
    )

    prediction = model.predict(next_month)

    return round(float(prediction[0]), 2)