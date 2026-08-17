import streamlit as st

st.set_page_config(page_title="CodeGuard AI", page_icon="🛡️", layout="wide")

st.title("🛡️ CodeGuard AI Login")

st.markdown("""
Welcome to **CodeGuard AI** - Enterprise Code Review SaaS.
Please log in to continue.
""")

roles = ["Developer", "QA", "Client"]
selected_role = st.selectbox("Select Role", roles)

if st.button("Login"):
    st.session_state["role"] = selected_role
    st.session_state["token"] = f"{selected_role}_token"
    st.success(f"Logged in as {selected_role}")
    st.switch_page("pages/1_dashboard.py")
