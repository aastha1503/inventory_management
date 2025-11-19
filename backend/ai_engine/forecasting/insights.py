# ai_engine/insights.py

class InventoryInsights:
    """Analyze product sales trends and anomalies."""
    '''
    Detect if sales suddenly dropped
    Classify whether a product is fast-moving, medium-moving, or slow-moving

    '''

    @staticmethod
    def detect_sudden_drop(sales_history):
        """Detect sudden drops in sales (>30% drop from previous day)."""
        if len(sales_history) < 3:
            return {"anomaly": False, "reason": "Not enough data"}

        prev = sales_history[-2]
        last = sales_history[-1]

        if prev == 0:
            return {"anomaly": False}

        drop_pct = (prev - last) / prev
        return {"anomaly": drop_pct > 0.30, "drop_pct": round(drop_pct, 3)}

    @staticmethod
    def classify_velocity(sales_history):
        """Classify product as Fast, Medium, or Slow moving based on avg sales."""
        if not sales_history:
            return "No Data"

        avg_sales = sum(sales_history) / len(sales_history)
        if avg_sales >= 20:    #The owner decides what counts as Fast, Medium, or Slow moving. It's a threshold value decided by owner.
            return "Fast selling item"
        elif avg_sales >= 5:
            return "Medium selling item"
        else:
            return "Slow sellin item"
