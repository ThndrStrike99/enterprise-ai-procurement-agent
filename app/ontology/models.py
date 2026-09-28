from pydantic import BaseModel
from typing import Optional


class Supplier(BaseModel):
    supplier_id: str
    supplier_name: str
    contracted: bool
    risk_score: float = 0.0


class Product(BaseModel):
    sku: str
    product_name: str
    category: str


class PurchaseOrder(BaseModel):
    po_id: str
    department: str
    buyer: str
    supplier_id: str
    sku: str
    unit_price: float
    quantity: int
    order_date: str


class Contract(BaseModel):
    contract_id: str
    supplier_id: str
    sku: Optional[str] = None
    contracted_price: Optional[float] = None
    terms: str
