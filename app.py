import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Golf Major Tracker", page_icon="⛳", layout="wide")

st.title("⛳ Golf Major Tracker")
st.subheader("Set up your tournament")

# Tournament name
tournament_name = st.text_input("Tournament name", placeholder="e.g. The Open 2026")

# Friends
st.subheader("Add your friends")
friends_input = st.text_area("Enter each friend's name on a new line", placeholder="John\nSarah\nMike")

if st.button("Save tournament"):
    if not tournament_name:
        st.error("Please enter a tournament name")
    elif not friends_input.strip():
        st.error("Please enter at least one friend's name")
    else:
        friends = [f.strip() for f in friends_input.strip().split("\n") if f.strip()]
        data = {
            "tournament": tournament_name,
            "friends": friends
        }
        with open("tournament.json", "w") as f:
            json.dump(data, f)
        st.success(f"Saved! Tournament: {tournament_name} with {len(friends)} players: {', '.join(friends)}")