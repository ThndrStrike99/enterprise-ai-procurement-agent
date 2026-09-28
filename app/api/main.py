from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.etl.pipeline import build_enriched_purchase_orders
from app.analytics.anomaly import add_price_anomaly_features
from app.agents.procurement_agent import investigate_purchase


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Operational AI demo for enterprise procurement intelligence.",
)


class PurchaseAnalysisRequest(BaseModel):
    po_id: str


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}


@app.get("/purchase-orders")
def list_purchase_orders(limit: int = 25):
    try:
        df = build_enriched_purchase_orders().head(limit)
        return df.fillna("").to_dict(orient="records")
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="Synthetic data not found. Run: python -m app.etl.generate_data",
        )


@app.get("/purchase-orders/{po_id}")
def get_purchase_order(po_id: str):
    try:
        df = build_enriched_purchase_orders()
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="Synthetic data not found. Run: python -m app.etl.generate_data",
        )

    row = df[df["po_id"] == po_id]

    if row.empty:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    return row.fillna("").iloc[0].to_dict()


@app.post("/analyze-purchase")
def analyze_purchase(request: PurchaseAnalysisRequest):
    try:
        df = add_price_anomaly_features(build_enriched_purchase_orders())
        row = df[df["po_id"] == request.po_id]
        if row.empty:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return row.fillna("").iloc[0].to_dict()
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="Synthetic data not found. Run: python -m app.etl.generate_data",
        )


@app.post("/agent/investigate")
def agent_investigate(request: PurchaseAnalysisRequest):
    try:
        return investigate_purchase(request.po_id).to_dict()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="Synthetic data not found. Run: python -m app.etl.generate_data",
        )
