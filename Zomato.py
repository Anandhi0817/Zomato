# Importing libraries
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd

# Data loading
zomato_data = pd.read_csv('zomato.csv')
zomato_country_data = pd.read_csv('Country-Code.csv')

# Merging the datasets
merged_df = pd.merge(zomato_data, zomato_country_data, how='left', on='Country Code')

# Adding a new column for converted cost to INR
merged_df['Converted Cost (INR)'] = merged_df['Average Cost for two'] * merged_df['Aggregate rating']

# Splitting the cuisines column into individual cuisines
merged_df['Cuisines'] = merged_df['Cuisines'].str.split(', ')

# Explode the lists to create a new row for each cuisine
exploded_df = merged_df.explode('Cuisines')

# Exploratory Data Analysis (EDA)
# Filter the DataFrame to include only restaurants in India
df_india = merged_df[merged_df['Country'] == 'India']

# Streamlit app
st.title('Zomato Data Analysis and Visualization')

# Sidebar navigation
selected = st.sidebar.selectbox("Navigation", ["Home", "Data Analysis and Visualization"])

if selected == "Home":
    st.markdown("Welcome to Zomato Data Analysis!")
    st.write("With our platform, you can gain valuable insights and make informed decisions about restaurants and food trends. Whether you're a food enthusiast, a restaurant owner, or a data analyst, our comprehensive data analysis tools provide you with the information you need. Explore restaurant ratings, cuisines, popular dishes, and more with ease. Let Zomato Data Analysis empower you in the world of food!")

    st.markdown("---")
    st.write("© 2024 Zomato. All rights reserved.")

if selected == "Data Analysis and Visualization":
    tab1, tab2 = st.columns(2)
    
    with tab1:
        st.subheader("Country based data analysis")
        selected_country = st.selectbox("Select Country", merged_df['Country'].unique())
        filtered_df = merged_df[merged_df['Country'] == selected_country]

        selected_analysis = st.selectbox("Select Analysis", ["Cuisine Analysis", "Delivery Services", "Cost Analysis", "Ratings Analysis"])
        
        if selected_analysis == "Cuisine Analysis":
            st.plotly_chart(px.sunburst(filtered_df, path=['Country', 'City', 'Cuisines'], title='Cuisine Analysis'))

        if selected_analysis == "Delivery Services":
            st.plotly_chart(px.pie(filtered_df.drop_duplicates(subset=['Restaurant Name']), names='Has Online delivery', title='Delivery Services'))

        if selected_analysis == "Cost Analysis":
            st.plotly_chart(px.scatter(filtered_df.groupby('Cuisines').agg({'Converted Cost (INR)': 'mean'}).reset_index(),
                                        x='Cuisines', y='Converted Cost (INR)', title='Cost Analysis'))

        if selected_analysis == "Ratings Analysis":
            st.plotly_chart(px.box(filtered_df, x='Restaurant Name', y='Aggregate rating', title='Ratings Analysis'))
    
    with tab2:
        st.subheader("City comparison in India")
        selected_city = st.selectbox("Select City", df_india['City'].unique())
        city_df = df_india[df_india['City'] == selected_city]

        selected_comparison = st.selectbox("Select Comparison", ["Restaurant Count", "Spending Patterns", "Living Cost"])

        if selected_comparison == "Restaurant Count":
            st.write(city_df.groupby(['City', 'Has Online delivery']).size().reset_index().rename(columns={0: 'Count'}))

        if selected_comparison == "Spending Patterns":
            st.plotly_chart(px.pie(city_df, names='Has Online delivery', values='Average Cost for two', 
                                   title=f'Spending Patterns: Online Delivery vs Dine-In in {selected_city}'))

        if selected_comparison == "Living Cost":
            st.plotly_chart(px.box(city_df, x='City', y='Average Cost for two', title=f'Average Living Cost in {selected_city}'))
