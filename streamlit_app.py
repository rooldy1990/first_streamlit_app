
import streamlit as st
import pandas as pd
import requests

st.title("My Mom's New Healthy Diner")

st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Assuming your DataFrame has columns 'Fruit' and 'Macro'
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = st.multiselect("Pick some fruits:", my_fruit_list['Fruit'].unique(), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list[my_fruit_list['Fruit'].isin(fruits_selected)]

# Display the table on the page.
st.dataframe(fruits_to_show)

# New Section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon" + "kiwi")
#st.text(fruityvice_response.json())

# take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#output it the screen as a table
st. dataframe(fruityvice_normalized)
