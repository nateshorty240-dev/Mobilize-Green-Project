import streamlit as st
import pandas as pd
import numpy as np

# --- Mock data (cached so it doesn't regenerate every rerun) ---
@st.cache_data
def generate_mock_data():
    # Region-level cohort data (no individual patients, ever)
    regions = pd.DataFrame({
        "region": ["US-East", "US-West", "US-Central", "EU-West", "EU-North", "APAC", "LATAM"],
        "lat": [39.0, 37.0, 41.5, 48.8, 59.3, 1.35, -23.5],
        "lon": [-77.0, -122.0, -93.0, 2.3, 18.0, 103.8, -46.6],
        "patient_count": [1800, 1500, 1200, 1600, 900, 1700, 1300]
    })

    # Model metadata over federated learning rounds
    rounds = pd.DataFrame({
        "round": list(range(1, 21)),
        "verification_loss": np.round(np.linspace(0.09, 0.042, 20) + np.random.normal(0, 0.003, 20), 4),
        "demographic_weight": np.round(np.linspace(0.75, 0.87, 20) + np.random.normal(0, 0.01, 20), 3)
    })

    return regions, rounds

regions_df, rounds_df = generate_mock_data()

 #page set up

st.set_page_config(
    page_title="Live PCCP AUDIT",
    page_icon="CD",
    layout="wide"
)

with st.sidebar:
    st.header("Project Team")
    st.write("Latiful —  context")
    st.write("Nathan — dashboard build")
    st.write("Gigi — Business Pitch")
    st.divider()
    st.caption("This dashboard never transmits raw patient data. Only encrypted, anonymized model updates leave patient devices.")

st.title("Live PCCP Audit Framework")
st.caption("Privacy-Preserving Federated Learning Compliance Dashboard")


tab1, tab2, tab3 =st.tabs(["Privacy Proof", "Live Audit", "Deploy & Log"])

#Tab 1:Privacy and Proof
with tab1:
    selected = st.multiselect("Filter by region", regions_df["region"].tolist(), default=regions_df["region"].tolist())
    st.map(regions_df[regions_df["region"].isin(selected)], latitude="lat", longitude="lon", size="patient_count")
    st.success("This dashboard displays zero patient names, medical, medical histories, or raw vitals as all Data below is aggregated model metadata only.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cohort Size", "10,000")
    col2.metric("Number of Regions", "7")
    col3.metric("Raw Records storied centrally", "0") 
 
    st.subheader("Cohort Regions (aggregated only)")
    st.map(regions_df, latitude="lat", longitude="lon", size="patient_count")

# Tab 2: Live Audit 


with tab2:
    status = "🟢 Compliant" if rounds_df["verification_loss"].iloc[-1] < 0.05 else "🟡 Under Review"
    st.markdown(f"**Compliance Status:** {status}")
    st.subheader("Model Metadata")

    col1, col2, col3 = st.columns(3)
    col1.metric("Demographic Weight", "0.87", "0.02")
    col2.metric("Verification Loss", "0.042", "-0.01")
    col3.metric("Model Version", "v2.0")

    st.write("Verification Loss over Federated Learning Rounds")
    st.line_chart(rounds_df, x="round", y="verification_loss")

# --- Tab 3: Deploy & Log ---
with tab3:
    st.subheader("Deploy Update")

    if "log" not in st.session_state:
        st.session_state.log = []
    if "deployed" not in st.session_state:
        st.session_state.deployed = False

    if st.button("Deploy Patch v2.1"):
        st.session_state.deployed = True
        with st.spinner("Distributing encrypted patch to 10,000 devices..."):
            import time
            for region in regions_df["region"]:
                st.session_state.log.append(f"Region: {region} — encrypted update received — status: verified")
                time.sleep(0.3)
        st.success("Patch v2.1 deployed to all regions.")
        st.toast("Deployment complete — 10,000 devices updated")

    st.subheader("Regulatory Activity Log")
    log_box = st.empty()
    if st.session_state.log:
        log_box.code("\n".join(st.session_state.log))
    else:
        log_box.write("No deployments yet. Click the button above to simulate one.")

    if st.session_state.log:
        st.download_button(
            "Download Audit Log (CSV)",
            data="\n".join(st.session_state.log),
            file_name="audit_log.csv"
        )
