import streamlit as st
import requests
import os
import pandas as pd

st.set_page_config(page_title="CodeGuard AI Dashboard", page_icon="🛡️", layout="wide")

if "role" not in st.session_state:
    st.warning("Please log in first.")
    st.switch_page("app.py")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.title("📊 CodeGuard AI Dashboard")
st.markdown(f"**Logged in as:** {st.session_state['role']}")

st.header("Connect GitHub Repository")
with st.form("repo_form"):
    repo_name = st.text_input("Repository Name (e.g., octocat/Hello-World)")
    pr_number = st.number_input("Pull Request Number", min_value=1, step=1)
    submit = st.form_submit_button("Analyze PR")

if submit:
    if st.session_state["role"] not in ["Developer", "QA"]:
        st.error("You do not have permission to trigger an analysis.")
    elif not repo_name:
        st.error("Please enter a repository name.")
    else:
        with st.spinner("Analyzing code with Gemini 2.0 Pro..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    params={"token": st.session_state["token"]},
                    json={"repo_name": repo_name, "pr_number": pr_number}
                )
                if response.status_code == 200:
                    result = response.json()
                    st.session_state["last_analysis"] = result
                    st.session_state["last_repo"] = repo_name
                    st.session_state["last_pr"] = pr_number
                    st.success("Analysis complete!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

if "last_analysis" in st.session_state:
    result = st.session_state["last_analysis"]

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Quality Score", f"{result.get('score', 0)} / 100")

    with col2:
        rec = result.get('recommendation', 'NEEDS FIX')
        color = "normal" if rec == "APPROVED" else "inverse"
        st.metric("Deploy Recommendation", rec, delta_color=color)

    st.subheader("Line-by-Line Comments")
    comments = result.get('comments', [])
    if comments:
        df = pd.DataFrame(comments)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No comments generated.")

    st.divider()
    st.header("Export PDF Report")

    if st.session_state["role"] == "Client":
        # Streamlit pattern: button triggers generation, stores in session state, then download button displays
        if st.button("Generate PDF Data"):
            with st.spinner("Generating PDF..."):
                try:
                    pdf_response = requests.post(
                        f"{BACKEND_URL}/export-pdf",
                        params={"token": st.session_state["token"]},
                        json={
                            "request": {"repo_name": st.session_state["last_repo"], "pr_number": st.session_state["last_pr"]},
                            "analysis": result
                        }
                    )
                    if pdf_response.status_code == 200:
                        st.session_state["pdf_data"] = pdf_response.content
                    else:
                         st.error(f"Error generating PDF: {pdf_response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

        if "pdf_data" in st.session_state:
            st.download_button(
                label="Download PDF Report",
                data=st.session_state["pdf_data"],
                file_name=f"CodeGuard_Report_PR_{st.session_state['last_pr']}.pdf",
                mime="application/pdf"
            )
    else:
        st.info("PDF Export is restricted to Client roles.")
