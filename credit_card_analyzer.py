# ================================================
# 🚀 FinVeda AI - Credit Card Analyzer
# Works on: Kaggle + Google Jules + Colab
# ================================================

import pandas as pd
import google.generativeai as genai
import os
import numpy as np
from datetime import datetime, timedelta

print("="*60)
print("🚀 FinVeda AI - Credit Card Analyzer")
print("="*60)

# CHECK CURRENT FOLDER
print("📂 Current Working Directory:", os.getcwd())

# 1. LOAD API KEY - Kaggle Secret / Jules Env Variable
try:
    from kaggle_secrets import UserSecretsClient
    user_secrets = UserSecretsClient()
    API_KEY = user_secrets.get_secret('GEMINI_API_KEY')
    print("✅ API Key loaded from Kaggle Secrets")
except:
    API_KEY = os.environ.get('GEMINI_API_KEY') # For Google Jules
    print("✅ API Key loaded from Environment Variable")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
print("✅ Gemini 1.5 Flash Connected\n")

# 2. AUTO FIND OR CREATE CSV
os.makedirs('data', exist_ok=True)
csv_path = 'data/credit_card.csv'

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print(f"✅ Data Loaded from: {csv_path}")
else:
    print("⚠️ File not found. Creating example credit_card.csv for demo")
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
    print(f"✅ Example file created at: {csv_path}")

print(f"✅ Data Shape: {df.shape}")
print(df.head(3))

print("\n" + "="*60)
print("--- AI ANALYSIS ---")

sample_data = df.head(15).to_string()
prompt = """
You are FinVeda AI, a Telugu banking assistant.
Analyze these credit card transactions:
""" + sample_data + """
Task in Telugu:
1. Check for any duplicate or double transaction.
2. Check for any unusually high amount.
3. Give 3 safety tips with emojis.
Reply in short, 4 lines only.
"""
res = model.generate_content(prompt)
print(res.text)

print("\n" + "="*60)
print("--- AI EVALUATION TEST ---")

test_questions = [
    "nenu refund ela adagali",
    "naku double debit undi em cheyali",
    "nenu home loan eligibility entha"
]

for i, q in enumerate(test_questions, 1):
    res = model.generate_content(f"You are FinVeda AI. Answer in Telugu politely and short: {q}")
    print(f"\nQ{i}: {q}")
    print(f"A{i}: {res.text}")
    print("-"*40)

print("\n✅ Evaluation Complete. FinVeda AI is LIVE")
