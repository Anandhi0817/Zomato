#importing 
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd

# Reading the two datasets for basic information
zomato_data = pd.read_csv(r'C:\Users\SHALINI\Desktop\Zomato\zomato.csv')
zomato_data.info()

zomato_country_data = pd.read_csv(r'C:\Users\SHALINI\Desktop\Zomato\Country-Code.csv')
zomato_country_data.info()

#Merging the two datasets together
zomato_data = pd.read_csv(r'C:\Users\SHALINI\Desktop\Zomato\zomato.csv')
zomato_country_data = pd.read_csv(r'C:\Users\SHALINI\Desktop\Zomato\Country-Code.csv')

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

#Exploratory Data Analysis (EDA) #Numerical EDA
#Displaying basic statistics of the columns
df = pd.read_csv(r'C:\Users\SHALINI\Desktop\Zomato\zomato_data_updated.csv')

# statistics of the numerical columns
print(df.describe())

#information about the dataset
print(df.info())

#Plot comparing Indian currency with other country's currency
# Specify the columns you want to include in correlation analysis
selected_columns = ['Aggregate rating','Price range', 'Converted Cost (INR)', 'Average Cost for two']

# Select only the specified columns
selected_data = df[selected_columns]

# Calculate the correlation matrix
correlation_matrix = selected_data.corr()

# Plot the heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Comparison of Indian Rupees with Other Currencies')
plt.show()

# Filter the DataFrame to include only restaurants in India
df_india = df[df['Country'] == 'India']

# Calculate the average cost for each cuisine in India
avg_cost_per_cuisine = df_india.groupby('Cuisines')['Average Cost for two'].mean().reset_index()

# Sort cuisines by average cost in descending order to find the top costly cuisines
top_costly_cuisines = avg_cost_per_cuisine.sort_values(by='Average Cost for two', ascending=False)

# Select only the top N cuisines (adjust N as needed)
N = 10  # for example, select top 10 costly cuisines
top_N_costly_cuisines = top_costly_cuisines.head(N)

#Find which cuisines are costly in India
df_top_N_costly_cuisines = df_india[df_india['Cuisines'].isin(top_N_costly_cuisines['Cuisines'])]
# Create a Sunburst chart
fig = px.sunburst(df_top_N_costly_cuisines, path=['Country', 'City', 'Cuisines'], 
                  title='Top {} Costly Cuisines in India'.format(N))
fig.update_layout(width=800, height=600)
fig.show()

# Reading the dataframe
df1 = pd.read_csv(r'C:\Users\SHALINI\Desktop\Zomato\zomato_data_updated.csv')
df = df1[df1['Country'] == 'India']
city_df = df[df['City'] == 'selected_city']

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
    st.write("© 2024 Zomato. All rights reserved.")

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
            st.markdown(f'<div style="text-align:center;"><b>The most costly cuisine in {selected_country_1} is "{most_costly_cuisine}"</b></div>', unsafe_allow_html=True)
    with tab2:
        st.markdown("City comparison in India")
        selected_city = st.selectbox("Select City", df['City'].unique())
        city_df = df[df['City'] == selected_city]
        selected = st.selectbox("Selected", ["City comparison", "Online Delivery vs Dine-In", "Living Cost vs Low Living Cost"])

        if selected == "City comparison":
            # Report 1: Comparison Between Cities in India
            st.markdown(f"## City comparison in {selected_city}")
            fig_city = px.scatter(city_df, x='City', y='Average Cost for two', color='Has Online delivery',
                                  title=f'Average Cost for Two in {selected_city} by Delivery Service')
            st.plotly_chart(fig_city)
            st.markdown(f"## City-wise Restaurant Count for {selected_city}")  # City-wise data table
            st.write(city_df.groupby(['City', 'Has Online delivery']).size().reset_index().rename(columns={0: 'Count'}))
        
        # Report 2: Part of India Spends More on Online Delivery vs Dine-In 
        if selected == "Online Delivery vs Dine-In":
            currency = '₹'
            st.markdown(f"## Spending Patterns for {selected_city}")
            fig_spending_patterns = px.pie(city_df, names='Has Online delivery', values='Average Cost for two', 
                                           title=f'Spending Patterns: Online Delivery vs Dine-In in {selected_city}',
                                           labels={'Has Online delivery': 'Service Type', 'Average Cost for two': 'Average Cost'})
            st.plotly_chart(fig_spending_patterns)
            st.markdown(f"## City-wise Data for {selected_city}")
            city_wise_data = city_df.groupby(['Has Online delivery'])['Average Cost for two'].mean().reset_index()
            city_wise_data['Average Cost for two'] = city_wise_data['Average Cost for two'].map(lambda x: f'{currency} {x:.2f}')
            st.write(city_wise_data)
        
        # Report 3: Part of India Has a High Living Cost vs Low Living Cost 
        if selected == "Living Cost vs Low Living Cost":
            currency = '₹'
            st.markdown(f"## Average Living Cost across Cities in India ({currency})")
            fig_living_cost = px.box(city_df, x='City', y='Average Cost for two',
                                     title=f'Average Living Cost across Cities in India ({currency})')
            st.plotly_chart(fig_living_cost)
            st.markdown(f"## City-wise Data for Living Cost in {selected_city}")
            city_wise_data = city_df.groupby(['City'])['Average Cost for two'].mean().reset_index()
            city_wise_data['Average Cost for two'] = city_wise_data['Average Cost for two'].map(lambda x: f'{currency} {x:.2f}')
            st.write(city_wise_data)
