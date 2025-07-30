import streamlit as st
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "complaints.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Timestamp","Name","Department","Issue","Photo","Status"])

st.title("FoodStories Maintenance Complaint Form")

name = st.text_input("Your Name")
dept = st.selectbox("Select Department", [
    "Kitchen","Café","Ground Floor","First Floor","Meat Section","Kitchen Studio","Others"
])
issue = st.text_area("Describe the Issue")
photo = st.file_uploader("Upload Photo (Optional)")

if st.button("Submit"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    photo_name = ""
    if photo:
        folder = "uploads"
        os.makedirs(folder, exist_ok=True)
        photo_name = f"{folder}/{photo.name}"
        with open(photo_name, "wb") as f:
            f.write(photo.read())
    new_row = pd.DataFrame([{
        "Timestamp": timestamp,
        "Name": name,
        "Department": dept,
        "Issue": issue,
        "Photo": photo_name,
        "Status": "Open"
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Complaint submitted!")

st.subheader("Dashboard: Open vs Closed")
status_counts = df["Status"].value_counts()
st.bar_chart(status_counts)
