# 5-Minute Interview Demo

## 1. Business Problem — 45 seconds

"Procurement teams often have purchase history, contracts, supplier catalogs,
and approval rules spread across different systems. I built an operational AI
layer that brings those sources together and helps buyers investigate risky
purchases before approval."

## 2. Architecture — 60 seconds

Explain:

source systems -> ETL -> ontology -> analytics/RAG -> agent -> human approval -> action

## 3. Live Scenario — 90 seconds

Enter:

```text
PO-23451
```

Explain:

- requested price
- historical median
- contract price
- variance
- potential savings
- recommendation

## 4. AI Engineering — 60 seconds

Explain:

- deterministic calculations stay outside the LLM
- RAG is used for contract evidence
- the agent orchestrates tools
- human approval prevents unsafe autonomous spending actions

## 5. FDE Mapping — 45 seconds

Explain:

- messy operational data
- enterprise object model
- decision logic
- AI
- user workflow
- action back into the business
