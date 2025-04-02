from datetime import timedelta

import numpy as np
from sklearn.linear_model import LinearRegression


def build_prediction(data):
    """
    data: список кортежей (дата, курс)
    возвращает: список словарей {'date': дата, 'rate': курс}
    """
    data = sorted(data)
    days = np.array([(d[0] - data[0][0]).days for d in data]).reshape(-1, 1)
    rates = np.array([d[1] for d in data])

    model = LinearRegression()
    model.fit(days, rates)

    predictions = []
    last_day = data[-1][0]

    for i in range(1, 8):  # 7 дней
        future_day = last_day + timedelta(days=i)
        x = np.array([(future_day - data[0][0]).days]).reshape(1, -1)
        predicted_rate = model.predict(x)[0]
        predictions.append({"date": future_day, "rate": round(predicted_rate, 4)})

    return predictions
