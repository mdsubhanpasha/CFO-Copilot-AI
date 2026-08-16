import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="FinVeda AI - Credit Card Analyzer", page_icon="🚀", layout="wide")

st.title("🚀 FinVeda AI - Credit Card Analyzer")
st.markdown("Analyze your credit card transactions with the power of Gemini AI.")

# 1. API Key Input
api_key = st.sidebar.text_input("Enter GEMINI_API_KEY", type="password")
if api_key:
    genai.configure(api_key=api_key)
    st.sidebar.success("API Key configured!")
else:
    st.sidebar.warning("Please enter your API Key to enable AI features.")

# 2. Data Loading
os.makedirs('data', exist_ok=True)
csv_path = 'data/credit_card.csv'

@st.cache_data
def load_data():
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        # Create example data if not exists
        data = {
            'Date': [datetime.now() - timedelta(days=x) for x in range(20)],
            'Merchant': ['Amazon', 'Flipkart', 'Swiggy', 'Zomato', 'Amazon', 'BigBasket', 'Uber', 'IRCTC', 'Netflix', 'PhonePe',
                         'Amazon', 'DMart', 'Petrol Pump', 'Hospital', 'College Fees', 'Swiggy', 'Zomato', 'Myntra', 'BookMyShow', 'Amazon'],
            'Amount': [1299, 599, 350, 420, 1299, 850, 180, 1200, 499, 50,
                       25000, 2100, 3000, 15000, 50000, 280, 390, 2200, 600, 899],
            'Category': ['Shopping', 'Shopping', 'Food', 'Food', 'Shopping', 'Grocery', 'Travel', 'Travel', 'Subscription', 'UPI',
                         'Shopping', 'Grocery', 'Fuel', 'Health', 'Education', 'Food', 'Food', 'Shopping', 'Entertainment', 'Shopping']
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)
        return df

df = load_data()

st.subheader("📊 Transaction Data")
st.dataframe(df)

if api_key:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        st.subheader("🤖 AI Analysis")
        if st.button("Analyze Transactions"):
            with st.spinner("Analyzing..."):
                sample_data = df.head(15).to_string()
                prompt = f"""
                You are FinVeda AI, a Banking Assistant.
                Analyze these credit card transactions:
                {sample_data}
                Task in English:
                1. Check for any duplicate or double transaction.
                2. Check for any unusually high amount.
                3. Give 3 safety tips.
                Reply in short, 4 lines only.
                """
                res = model.generate_content(prompt)
                st.write(res.text)

        st.subheader("❓ AI Evaluation Test")
        test_questions = [
            "How can I request a refund?",
            "I have a double debit. What should I do?",
            "What is my home loan eligibility?"
        ]

        selected_question = st.selectbox("Select a question to ask FinVeda AI:", test_questions)
        if st.button("Ask Question"):
            with st.spinner("Thinking..."):
                res = model.generate_content(f"You are FinVeda AI. Answer in English politely and short: {selected_question}")
                st.info(res.text)

    except Exception as e:
        st.error(f"Error communicating with Gemini AI: {e}")
