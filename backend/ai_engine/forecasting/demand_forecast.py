# Demand forecasting using past sales data.
import numpy as np
from sklearn.linear_model import LinearRegression

class DemandForecaster:
    """Forecast future product demand based on past sales."""

    @staticmethod
    def forecast_next_days(sales_history, n_days=30):
        """
        sales_history: list of integers, ordered by date ascending
        n_days: number of future days to predict
        """
        if not sales_history or len(sales_history) < 3:
            return {"error": "Not enough sales data (>=3 points required)"}

        X = np.arange(len(sales_history)).reshape(-1, 1)
        y = np.array(sales_history)

        model = LinearRegression()
        model.fit(X, y)

        future_X = np.arange(len(sales_history), len(sales_history) + n_days).reshape(-1, 1)
        preds = model.predict(future_X)

        # No negative predictions
        preds = [float(max(0.0, p)) for p in preds]
        return preds
