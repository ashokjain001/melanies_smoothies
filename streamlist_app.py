# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")

Name_on_order = st.text_input("Name on the Smoothie")

st.write("The name on your Smoothie will be", Name_on_order)

st.write("""Choose the fruits you want in your custom Smoothie!""")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width = True)
st.stop()
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect( "Choose up to 5 ingredients:", my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''
    
    for fruits_chosen in ingredients_list:
        ingredients_string+= fruits_chosen+' '
        st.subheader(fruits_chosen +'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruits_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width = True) 


    #st.write("You selected:", ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) 
                        values('"""+ ingredients_string + """','"""+Name_on_order+"""')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('your smoothie is ordered', icon = "✅")

