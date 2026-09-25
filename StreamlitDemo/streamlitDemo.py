import streamlit as st
import pandas as pd

st.title("My First Streamlit App")

st.write("Hello! Welcome to my Streamlit application.")

name = st.text_input("Enter your  first name")
name1 = st.text_input("id1","Enter your last name")

if name and name1:
    st.success(f"Hello {name} {name1}! Welcome to Streamlit.")
    

df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [10, 20, 30, 40]
})

st.write("Simple Data Frame")
st.dataframe(df)

st.line_chart(df)

# command to run the app: streamlit run streamlitDemo.py