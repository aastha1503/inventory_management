# Suggest reorder quantities based on predicted demand.

class ReorderEngine:
    """Calculate suggested reorder quantities for products."""

    @staticmethod
    def suggest_reorder(predicted_sales, current_stock, safety_days=7):
        """
        predicted_sales: list of predicted daily sales, This is the forecast of how many items you expect to sell in upcoming days.
        current_stock: int, how many items you currently have in your warehouse.
        safety_days: These are extra number of days you want to keep stock for safety.

        """
        if not predicted_sales:    #If the prediction list is empty, the function returns an error bcz you cannot calculate reorder quantity without future demand.
            return {"error": "No prediction data"}

        predicted_total = sum(predicted_sales)
        """
        If predictions = [10, 12, 11, 14]
        Total predicted = 47
        This means you expect to sell 47 units over the forecast period
        """
        avg_daily = predicted_total / len(predicted_sales)
        """
        If predicted_total = 47
        and number of days = 4
        then:
        avg_daily = 47 / 4 = 11.75 units/day

        """
        safety_stock = avg_daily * safety_days
        """
        If avg_daily = 11.75
        and safety_days = 7
        Safety stock = 11.75 * 7 = 82.25
        Means:
        You keep 82 units extra as a buffer to avoid stockout.
        """
        suggested_qty = max(0, int(round(predicted_total + safety_stock - current_stock)))
        """
        Example:
       Predicted = 47
       Safety = 82
       Total needed = 129 units

       If current_stock = 40
       Needed = 129
       Stock = 40
       Reorder quantity = 129 - 40 = 89

       If result is negative (meaning stock is enough), reorder becomes 0.
        """

        return {
            "predicted_total": int(round(predicted_total)),
            "avg_daily": float(round(avg_daily, 2)),
            "safety_stock": int(round(safety_stock)),
            "current_stock": current_stock,
            "suggested_reorder_qty": suggested_qty
        }
