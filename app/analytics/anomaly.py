import pandas as pd


def add_price_anomaly_features(df: pd.DataFrame, threshold_pct: float = 25.0) -> pd.DataFrame:
    result = df.copy()

    medians = (
        result.groupby("sku")["unit_price"]
        .median()
        .rename("historical_median_price")
        .reset_index()
    )

    result = result.merge(medians, on="sku", how="left")
    result["price_variance_pct"] = (
        (result["unit_price"] - result["historical_median_price"])
        / result["historical_median_price"]
        * 100
    )

    result["is_price_anomaly"] = result["price_variance_pct"] >= threshold_pct

    result["potential_savings_per_unit"] = (
        result["unit_price"] - result["contracted_price"]
    ).clip(lower=0)

    result["potential_savings_total"] = (
        result["potential_savings_per_unit"] * result["quantity"]
    )

    return result
