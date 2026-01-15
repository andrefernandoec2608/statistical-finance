import pandas as pd
from typing import List, Dict, Any
from model.transaction import Transaction
from sklearn.linear_model import LinearRegression
from utils.enums import TransactionType

def transaction_amount_statistics(transactions: List[Transaction]) -> Dict[str, Any]:

    data = [
        {
            "date": t.date,
            "amount": t.amount,
            "category": t.category.name,
            "transaction_type": t.transaction_type.name,
        }
        for t in transactions
    ]

    df = pd.DataFrame(data)

    stats = df["amount"].describe()

    return {
        "count": int(stats["count"]),
        "mean": float(stats["mean"]),
        "median": float(stats["50%"]),
        "std": float(stats["std"]),
        "min": float(stats["min"]),
        "max": float(stats["max"]),
    }

def transaction_category_summary(
    transactions: List[Transaction],
) -> Dict[str, Dict[str, float]]:

    data = [
        {
            "category": t.category.name,
            "transaction_type": t.transaction_type.name,
            "amount": t.amount,
        }
        for t in transactions
    ]

    df = pd.DataFrame(data)

    grouped = (
        df
        .groupby(["category", "transaction_type"])["amount"]
        .sum()
        .unstack(fill_value=0)
    )

    result: Dict[str, Dict[str, float]] = {}

    for category, row in grouped.iterrows():
        result[category] = {
            "Income": float(row.get("INCOME", 0)),
            "Expense": float(row.get("EXPENSE", 0)),
        }

    return result

def monthly_amount_forecast_linear(
    transactions: List[Transaction],
    transaction_type: TransactionType,
    months_to_predict: int,
) -> Dict[str, Any]:

    if months_to_predict <= 0:
        raise ValueError("months_to_predict must be > 0")

    if not transactions:
        return {"history": [], "forecast": []}

    df = pd.DataFrame(
        [{"date": t.date, "amount": float(t.amount)} for t in transactions]
    )
    df["date"] = pd.to_datetime(df["date"])

    # Aggregate monthly totals
    monthly = (
        df.assign(month=df["date"].dt.to_period("M"))
          .groupby("month", as_index=False)["amount"]
          .sum()
          .sort_values("month")
          .reset_index(drop=True)
    )

    # Dynamic labels
    base_label = transaction_type.value.lower()
    predicted_label = f"predicted_{base_label}"

    history = [
        {"month": str(row["month"]), base_label: float(row["amount"])}
        for _, row in monthly.iterrows()
    ]

    # Regression
    X = pd.Series(range(len(monthly))).to_numpy().reshape(-1, 1)
    y = monthly["amount"].to_numpy()

    model = LinearRegression()
    model.fit(X, y)

    X_future = pd.Series(
        range(len(monthly), len(monthly) + months_to_predict)
    ).to_numpy().reshape(-1, 1)

    y_pred = model.predict(X_future)

    last_month = monthly.loc[len(monthly) - 1, "month"]
    future_months = [str(last_month + i) for i in range(1, months_to_predict + 1)]

    forecast = [
        {"month": future_months[i], predicted_label: float(y_pred[i])}
        for i in range(months_to_predict)
    ]

    return {
        "history": history,
        "forecast": forecast
    }