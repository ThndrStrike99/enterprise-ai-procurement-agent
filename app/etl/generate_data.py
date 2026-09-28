from pathlib import Path
import random
import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "generated"
OUT.mkdir(parents=True, exist_ok=True)


def build_suppliers() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"supplier_id": "SUP-001", "supplier_name": "VWR Scientific", "contracted": True, "risk_score": 0.08},
            {"supplier_id": "SUP-002", "supplier_name": "Fisher Scientific", "contracted": True, "risk_score": 0.10},
            {"supplier_id": "SUP-003", "supplier_name": "Alkali Scientific", "contracted": False, "risk_score": 0.22},
            {"supplier_id": "SUP-004", "supplier_name": "LabSource Direct", "contracted": False, "risk_score": 0.31},
        ]
    )


def build_products() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"sku": "LAB-1001", "product_name": "Nitrile Gloves", "category": "Lab Supplies"},
            {"sku": "LAB-1002", "product_name": "Pipette Tips", "category": "Lab Supplies"},
            {"sku": "LAB-1003", "product_name": "Centrifuge Tubes", "category": "Lab Supplies"},
            {"sku": "LAB-1004", "product_name": "Reagent Kit", "category": "Reagents"},
            {"sku": "LAB-1005", "product_name": "Safety Goggles", "category": "Safety"},
        ]
    )


def build_contracts() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"contract_id": "CON-001", "supplier_id": "SUP-001", "sku": "LAB-1001", "contracted_price": 26.17,
             "terms": "Contract price valid through fiscal year. Preferred supplier for lab consumables."},
            {"contract_id": "CON-002", "supplier_id": "SUP-002", "sku": "LAB-1002", "contracted_price": 18.40,
             "terms": "Pricing locked for twelve months. Freight included above minimum order threshold."},
            {"contract_id": "CON-003", "supplier_id": "SUP-001", "sku": "LAB-1003", "contracted_price": 14.10,
             "terms": "Preferred pricing applies to all university departments."},
        ]
    )


def build_purchase_orders(n: int = 250) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    random.seed(42)

    skus = ["LAB-1001", "LAB-1002", "LAB-1003", "LAB-1004", "LAB-1005"]
    supplier_ids = ["SUP-001", "SUP-002", "SUP-003", "SUP-004"]
    departments = ["Biology", "Chemistry", "Medical Research", "Engineering"]
    buyers = ["A. Patel", "J. Smith", "M. Chen", "R. Johnson"]

    base_prices = {
        "LAB-1001": 24.50,
        "LAB-1002": 18.25,
        "LAB-1003": 13.90,
        "LAB-1004": 72.00,
        "LAB-1005": 11.50,
    }

    rows = []
    for i in range(1, n + 1):
        sku = random.choice(skus)
        price = round(base_prices[sku] * rng.normal(1.0, 0.08), 2)
        rows.append(
            {
                "po_id": f"PO-{23000+i}",
                "department": random.choice(departments),
                "buyer": random.choice(buyers),
                "supplier_id": random.choice(supplier_ids),
                "sku": sku,
                "unit_price": max(price, 1),
                "quantity": random.randint(5, 250),
                "order_date": pd.Timestamp("2026-01-01") + pd.Timedelta(days=random.randint(0, 250)),
            }
        )

    # Inject interview-friendly anomaly
    rows.append(
        {
            "po_id": "PO-23451",
            "department": "Medical Research",
            "buyer": "A. Patel",
            "supplier_id": "SUP-004",
            "sku": "LAB-1001",
            "unit_price": 45.21,
            "quantity": 300,
            "order_date": pd.Timestamp("2026-09-01"),
        }
    )

    return pd.DataFrame(rows)


def main():
    suppliers = build_suppliers()
    products = build_products()
    contracts = build_contracts()
    purchase_orders = build_purchase_orders()

    suppliers.to_csv(OUT / "suppliers.csv", index=False)
    products.to_csv(OUT / "products.csv", index=False)
    contracts.to_csv(OUT / "contracts.csv", index=False)
    purchase_orders.to_csv(OUT / "purchase_orders.csv", index=False)

    print(f"Generated data in {OUT}")


if __name__ == "__main__":
    main()
