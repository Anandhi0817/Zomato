import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Reading the two datasets for basic information
zomato_data = pd.read_csv('Desktop/Zomato/zomato.csv')
zomato_data.info()

zomato_country_data = pd.read_csv('Desktop/Zomato/Country-Code.csv')
zomato_country_data.info()

#Merging the two datasets together
zomato_data = pd.read_csv('Desktop/Zomato/zomato.csv')
zomato_country_data = pd.read_csv('Desktop/Zomato/Country-Code.csv')

# Merge DataFrames
merged_df = pd.merge(zomato_data, zomato_country_data, how='left', on='Country Code')

# Display a few rows to verify the merge
print(merged_df.head())
print(merged_df.info())

#Adding a new column 'Converted Cost (INR)' for the Average cost of two in Indian currency
# Multiplying 'Exchange Rate' with average column for two for the converted cost
merged_df['Converted Cost (INR)'] = merged_df['Average Cost for two'] * merged_df['Aggregate rating']

# Displaying the final DataFrame with new columns
print(merged_df[['Country', 'Average Cost for two', 'Converted Cost (INR)']])

# Splitting the cuisines column into individual cuisines
merged_df['Cuisines'] = merged_df['Cuisines'].str.split(', ')

# Explode the lists to create a new row for each cuisine
exploded_df = merged_df.explode('Cuisines')

# Now you can use groupby to get counts for each cuisine
cuisine_counts = exploded_df['Cuisines'].value_counts()

# Print the counts
print(cuisine_counts)
print(exploded_df.head())
print(exploded_df.info())

#Saving the new dataframe in an updated file
exploded_df.info()
exploded_df.to_csv('Desktop/Zomato/zomato_data_updated.csv')

#Exploratory Data Analysis (EDA) #Numerical EDA
#Displaying basic statistics of the columns
df = pd.read_csv('Desktop/Zomato/zomato_data_updated.csv')

# Display basic statistics of the numerical columns
print(df.describe())

# Display information about the dataset
print(df.info())


# Reading the dataframe
df1 = pd.read_csv('Desktop/Zomato/zomato_data_updated.csv')
df = df1[df1['Country'] == 'India']

# Streamlit part
st.markdown("<h1 style='text-align: center; color: Brown; font-size: 25px; font-family: Arial, sans-serif;'>Zomato Data Analysis and Visualization</h1>", unsafe_allow_html=True)

with st.sidebar:
    selected = st.sidebar.selectbox("Navigation", ["Home", "Data Analysis and Visualization"])

if selected == "Home":
    st.markdown("Welcome to Zomato Data Analysis !")
    st.write("With our platform, you can gain valuable insights and make informed decisions about restaurants and food trends. Whether you're a food enthusiast, a restaurant owner, or a data analyst, our comprehensive data analysis tools provide you with the information you need. Explore restaurant ratings, cuisines, popular dishes, and more with ease. Let Zomato Data Analysis empower you in the world of food !")
    
    # Footer with image
    st.markdown('<div class="icon-container"><img src="/content/5.png" width="60"></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.write("© 2024 BizCardX. All rights reserved.")

if selected == "Data Analysis and Visualization":
    tab1, tab2 = st.tabs(["Country based data analysis","City comparison in India"])
    with tab1:
        st.markdown("Country based data analysis")
        selected_country_1 = st.selectbox("Select Country_1", df1['Country'].unique(), index=0)
        filtered_df_1 = df1[df1['Country'] == selected_country_1]
        selected = st.selectbox("Selected", ["Cuisine Analysis", "Delivery Services", "Cost Analysis using Converted Cost (INR)", 
                                             "Ratings Analysis - Restaurant-wise", "The most costly cuisine"])
        if selected == "Cuisine Analysis":
            st.plotly_chart(px.sunburst(filtered_df_1, path=['Country', 'City', 'Cuisines'], title='Cuisine Analysis'))
        if selected == "Delivery Services":
            st.plotly_chart(px.pie(filtered_df_1.drop_duplicates(subset=['Restaurant Name']), names='Has Online delivery', title='Delivery Services'))
        if selected == "Cost Analysis using Converted Cost (INR)":
             st.plotly_chart(px.scatter(filtered_df_1.groupby('Cuisines').agg({'Converted Cost (INR)': 'mean'}).reset_index(),
                           x='Cuisines', y='Converted Cost (INR)', title='Cost Analysis'))
        if selected == "Ratings Analysis - Restaurant-wise":
            st.plotly_chart(px.box(filtered_df_1, x='Restaurant Name', y='Aggregate rating', title='Ratings Analysis'))
        if selected == "The most costly cuisine":
            most_costly_cuisine = filtered_df_1.groupby('Cuisines')['Converted Cost (INR)'].mean().idxmax()
            st.markdown(f'<div style="text-align:center;"><b>The most costly cuisine in {selected_country} is "{most_costly_cuisine}"</b></div>', unsafe_allow_html=True)
    with tab2:
        st.markdown("City comparison in India")
        # Report 1: Comparison Between Cities in India
        fig_cities = px.sunburst(df.groupby(['City', 'Has Online delivery']).size().reset_index(),
                                 path=['City', 'Has Online delivery'], values=0,
                                 title='Number of Restaurants per City')
        fig_cities.update_layout(width=800, height=600)
        st.plotly_chart(fig_cities)
    
        # Report 2: Part of India Spends More on Online Delivery vs Dine-In 
        spending_data = df.groupby(['City', 'Has Online delivery'])['Average Cost for two'].mean().reset_index()
        
        fig_spending_patterns = px.bar(spending_data, x='City', y='Average Cost for two', color='Has Online delivery',
                                       title='Spending Patterns: Online Delivery vs Dine-In across Cities in India')
        st.plotly_chart(fig_spending_patterns)
    
        # Report 3: Part of India Has a High Living Cost vs Low Living Cost 
        living_cost_data = df.groupby('City')['Average Cost for two'].mean().reset_index()
        
        fig_living_cost = px.box(living_cost_data, x='City', y='Average Cost for two',
                                 title='Average Living Cost across Cities in India')
        st.plotly_chart(fig_living_cost)
