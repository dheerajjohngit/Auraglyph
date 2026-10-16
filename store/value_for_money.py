def calculate_vfm(product):

    price = float(product.price)

    price_score = max(
        0,
        100 - (price / 500)
    )

    score = (

        product.processor_score * 0.50 +

        product.camera_score * 0.45 +

        product.battery_score * 0.20 +

        product.display_score * 0.10 +

        price_score * 0.30

    )

    return round(score, 2)

def predict_vfm(score):

    if score >= 85:
        return "🔥 Best Value"

    elif score >= 75:
        return "✅ Great Value"

    elif score >= 65:
        return "👍 Good Value"

    elif score >= 50:
        return "⚖️ Average Value"

    return "❌ Poor Value"