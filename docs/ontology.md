# Procurement Ontology

## Objects

### Supplier
Represents a vendor that can provide goods or services.

### Product
Represents a purchasable SKU.

### Contract
Represents negotiated commercial terms.

### PurchaseOrder
Represents a procurement transaction.

### Department
Represents the business unit responsible for spend.

### Buyer
Represents the person initiating or managing procurement.

## Relationships

```text
Supplier --sells--> Product
Supplier --governed_by--> Contract
PurchaseOrder --purchased_from--> Supplier
PurchaseOrder --contains--> Product
Department --creates--> PurchaseOrder
Buyer --manages--> PurchaseOrder
```

## Why Ontology Matters

The ontology makes business relationships explicit.

Instead of asking an LLM to infer relationships from raw tables, the system
creates a reusable operational model that agents and applications can query.
