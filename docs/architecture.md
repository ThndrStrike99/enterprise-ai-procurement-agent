# Architecture

## Goal

Create an operational procurement intelligence platform that combines:

1. enterprise data pipelines
2. business ontology
3. analytics
4. retrieval-augmented generation
5. agent orchestration
6. human approval
7. downstream actions

## Logical Architecture

```mermaid
flowchart TB
    A[ERP / Purchasing] --> E[ETL]
    B[Supplier Catalogs] --> E
    C[Contracts] --> R[RAG Pipeline]
    D[Invoices] --> E

    E --> W[(Operational Data Store)]
    W --> O[Procurement Ontology]

    O --> P[Procurement Agent]
    R --> P
    X[Anomaly Detection] --> P

    P --> API[FastAPI]
    API --> UI[Streamlit / React]
    P --> H[Human Approval]
    H --> ACT[Action Layer]
```

## Design Principle

The LLM should not directly approve spend.

The system separates:

- deterministic calculations
- retrieval and evidence
- AI explanation
- recommendation
- human approval
- governed action
