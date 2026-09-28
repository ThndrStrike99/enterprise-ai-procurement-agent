from dataclasses import dataclass, asdict
from typing import Optional

from app.etl.pipeline import build_enriched_purchase_orders
from app.analytics.anomaly import add_price_anomaly_features


@dataclass
class InvestigationResult:
    po_id: str
    supplier: str
    product: str
    requested_price: float
    historical_median: float
    variance_pct: float
    contracted_price: Optional[float]
    potential_savings_total: float
    recommendation: str
    requires_human_approval: bool = True

    def to_dict(self):
        return asdict(self)


def investigate_purchase(po_id: str) -> InvestigationResult:
    df = build_enriched_purchase_orders()
    df = add_price_anomaly_features(df)

    row = df[df["po_id"] == po_id]

    if row.empty:
        raise ValueError(f"Purchase order {po_id} not found")

    r = row.iloc[0]

    contracted_price = None if r["contracted_price"] != r["contracted_price"] else float(r["contracted_price"])

    if bool(r["is_price_anomaly"]) and contracted_price and r["unit_price"] > contracted_price:
        recommendation = "Route to contracted supplier for review"
    elif bool(r["is_price_anomaly"]):
        recommendation = "Escalate for procurement review"
    else:
        recommendation = "No material pricing anomaly detected"

    return InvestigationResult(
        po_id=r["po_id"],
        supplier=r["supplier_name"],
        product=r["product_name"],
        requested_price=float(r["unit_price"]),
        historical_median=round(float(r["historical_median_price"]), 2),
        variance_pct=round(float(r["price_variance_pct"]), 1),
        contracted_price=contracted_price,
        potential_savings_total=round(float(r["potential_savings_total"]), 2),
        recommendation=recommendation,
    )
