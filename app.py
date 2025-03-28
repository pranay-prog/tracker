import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Initialize the app
st.title("SmartSpend: Personal Finance Manager")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Add Expense", "Set Goals", "Reminders", "Investments"])

# Initialize data storage
if "expenses" not in st.session_state:
    st.session_state["expenses"] = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

if "savings" not in st.session_state:
    st.session_state["savings"] = 0

if "goals" not in st.session_state:
    st.session_state["goals"] = {"Monthly Limit": 0, "Savings Goal": 0}

if "reminders" not in st.session_state:
    st.session_state["reminders"] = []

# Dashboard Page
if page == "Dashboard":
    st.header("Dashboard")
    
    # Display expenses summary
    if not st.session_state["expenses"].empty:
        total_spent = st.session_state["expenses"]["Amount"].sum()
        st.write(f"Total Spent: ₹{total_spent}")
        st.write(f"Total Savings: ₹{st.session_state['savings']}")
        
        # Display spending breakdown by category
        category_breakdown = st.session_state["expenses"].groupby("Category")["Amount"].sum()
        fig, ax = plt.subplots()
        category_breakdown.plot(kind="bar", ax=ax)
        ax.set_title("Spending by Category")
        ax.set_ylabel("Amount (₹)")
        st.pyplot(fig)
    else:
        st.write("No expenses recorded yet.")
    
    # Display goals
    if st.session_state["goals"]["Monthly Limit"]:
        st.write(f"Monthly Spending Limit: ₹{st.session_state['goals']['Monthly Limit']}")
    if st.session_state["goals"]["Savings Goal"]:
        st.write(f"Savings Goal: ₹{st.session_state['goals']['Savings Goal']}")

# Add Expense Page
elif page == "Add Expense":
    st.header("Add Expense")
    
    with st.form("expense_form"):
        date = st.date_input("Date", value=datetime.date.today())
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Others"])
        amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
        description = st.text_input("Description")
        submit = st.form_submit_button("Add Expense")
        
        if submit:
            new_expense = {"Date": date, "Category": category, "Amount": amount, "Description": description}
            st.session_state["expenses"] = pd.concat([st.session_state["expenses"], pd.DataFrame([new_expense])], ignore_index=True)
            st.success("Expense added successfully!")

# Set Goals Page
elif page == "Set Goals":
    st.header("Set Financial Goals")
    
    with st.form("goal_form"):
        monthly_limit = st.number_input("Set Monthly Spending Limit (₹)", min_value=0.0, step=0.01)
        savings_goal = st.number_input("Set Savings Goal (₹)", min_value=0.0, step=0.01)
        submit = st.form_submit_button("Save Goals")
        
        if submit:
            st.session_state["goals"]["Monthly Limit"] = monthly_limit
            st.session_state["goals"]["Savings Goal"] = savings_goal
            st.success("Goals updated successfully!")

# Reminders Page
elif page == "Reminders":
    st.header("Reminders")
    
    with st.form("reminder_form"):
        reminder_date = st.date_input("Reminder Date", value=datetime.date.today())
        reminder_text = st.text_area("Reminder Text")
        submit = st.form_submit_button("Add Reminder")
        
        if submit:
            new_reminder = {"Date": reminder_date, "Text": reminder_text}
            st.session_state["reminders"].append(new_reminder)
            st.success("Reminder added successfully!")
    
    # Display reminders
    if len(st.session_state["reminders"]) > 0:
        for reminder in sorted(st.session_state["reminders"], key=lambda x: x["Date"]):
            with st.expander(f"{reminder['Date']}: {reminder['Text']}"):
                pass

# Investments Page
elif page == "Investments":
    st.header("Explore Investment Options")
    
    # Dummy investment options (replace with API integration for real data)
    investments_data = [
        {"Name": "Mutual Fund A", "Expected Return (%)": 12},
        {"Name": "Stock B", "Expected Return (%)": 15},
        {"Name": "Fixed Deposit C", "Expected Return (%)": 7},
    ]
    
    investments_df = pd.DataFrame(investments_data)
    selected_investment = st.selectbox(
        "Choose an investment option",
        investments_df["Name"]
    )
    
    selected_details = investments_df[investments_df["Name"] == selected_investment]
    for index, row in selected_details.iterrows():
        st.write(f"Name: {row['Name']}")
        st.write(f"Expected Return: {row['Expected Return (%)']}%")

st.sidebar.markdown("---")
st.sidebar.write(f"Total Expenses Recorded: {len(st.session_state['expenses'])}")