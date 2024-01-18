import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests get ("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas. json_normalize(fruityvice_response.json())
    return fruityvice_normalized 
#New Section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = st.text_input( 'What fruit would you like information about?')
    if not fruit_choice:
        st.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        st. dataframe(back_from_function)

# Connecting to Snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()

# Fetching data from the Snowflake table
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()

# Displaying the Snowflake table data
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

# Adding a textbox for the user to input a new fruit to add
new_fruit = st.text_input("What fruit would you like to add:")
fruits_to_add_existing = st.multiselect("Select existing fruits to add to the list:", my_fruit_list['Fruit'].unique())

# If the user presses Enter or clicks the button, add the new fruit to the list
if new_fruit or fruits_to_add_existing:
    fruits_added = [new_fruit] if new_fruit else []
    fruits_added.extend(fruits_to_add_existing)
    # Update your Snowflake table or any other storage mechanism as needed
    st.success(f"Fruits {', '.join(fruits_added)} have been added to the list!")
