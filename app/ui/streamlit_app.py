import streamlit as st

from app.agents.procurement_agent import investigate_purchase


st.set_page_config(
    page_title="Enterprise AI Procurement Agent",
    layout="wide",
)

st.title("Enterprise AI Procurement Agent")
st.caption("AI Engineer / Palantir FDE portfolio demo")

st.markdown(
    """
This demo investigates purchase orders using historical pricing,
contract data, supplier information, and explainable anomaly logic.
"""
)

po_id = st.text_input("Purchase Order ID", value="PO-23451")

if st.button("Investigate Purchase"):
    try:
        result = investigate_purchase(po_id)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Requested Price", f"${result.requested_price:,.2f}")
        col2.metric("Historical Median", f"${result.historical_median:,.2f}")
        col3.metric("Variance", f"{result.variance_pct:,.1f}%")

        if result.contracted_price is not None:
            col4.metric("Contract Price", f"${result.contracted_price:,.2f}")
        else:
            col4.metric("Contract Price", "N/A")

        st.subheader("AI Investigation")
        st.write(f"**Supplier:** {result.supplier}")
        st.write(f"**Product:** {result.product}")
        st.write(f"**Potential savings:** ${result.potential_savings_total:,.2f}")
        st.write(f"**Recommendation:** {result.recommendation}")

        st.info(
            "Human approval required before any operational action is executed."
        )

        st.button("Approve Recommendation", disabled=True)
    except Exception as exc:
        st.error(str(exc))
