import pandas as pd
from app.analytics.anomaly import add_price_anomaly_features


def test_detects_price_anomaly():
    df = pd.DataFrame(
        [
            {"sku": "A", "unit_price": 10.0, "quantity": 10, "contracted_price": 9.0},
            {"sku": "A", "unit_price": 10.0, "quantity": 10, "contracted_price": 9.0},
            {"sku": "A", "unit_price": 20.0, "quantity": 10, "contracted_price": 9.0},
        ]
    )

    result = add_price_anomaly_features(df, threshold_pct=25)

    assert result.iloc[-1]["is_price_anomaly"]
    assert result.iloc[-1]["price_variance_pct"] > 25
