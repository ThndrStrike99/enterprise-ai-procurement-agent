from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "generated"


def load_procurement_data():
    return {
        "purchase_orders": pd.read_csv(DATA_DIR / "purchase_orders.csv"),
        "suppliers": pd.read_csv(DATA_DIR / "suppliers.csv"),
        "products": pd.read_csv(DATA_DIR / "products.csv"),
        "contracts": pd.read_csv(DATA_DIR / "contracts.csv"),
    }


def build_enriched_purchase_orders() -> pd.DataFrame:
    data = load_procurement_data()
    po = data["purchase_orders"]
    suppliers = data["suppliers"]
    products = data["products"]
    contracts = data["contracts"]

    enriched = po.merge(suppliers, on="supplier_id", how="left")
    enriched = enriched.merge(products, on="sku", how="left")

    contracted = contracts[["sku", "contracted_price"]].dropna()
    contracted = contracted.groupby("sku", as_index=False)["contracted_price"].min()

    enriched = enriched.merge(contracted, on="sku", how="left")
    enriched["extended_cost"] = enriched["unit_price"] * enriched["quantity"]

    return enriched
