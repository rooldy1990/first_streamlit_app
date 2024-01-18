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

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx. cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlit')")
        return "Thanks for adding " + new_fruit
        
add_my_fruit = streamlit.text_input( 'What fruit would you like to add ?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
