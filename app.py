import streamlit as st
from graph import graph

st.set_page_config(
    page_title="Sentinels of Truth",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Sentinels of Truth")
st.subheader("Multi-Agent Fact Checking System")

claim = st.text_area(
    "Enter a claim to verify:",
    placeholder="Example: India won ICC Champions Trophy 2025"
)
if st.button("Verify Claim"):
    if not claim.strip():
        st.warning("Please enter a claim.")
    else:
        with st.spinner("Agents are investigating..."):
            result = graph.invoke({
                "claim": claim
            })
        st.success("Verification Complete!")

        st.markdown("## Final Decision")
        st.write(result["decision"])

        st.markdown("## Verification Status")
        st.write(result["verification_status"])

        st.markdown("##  Evidence")
        st.text_area(
            "Evidence",
            value=result["evidence"],
            height=300
        )