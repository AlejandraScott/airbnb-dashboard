import streamlit as st
import pandas as pd

# Set up the page layout
st.set_page_config(layout="wide")

# Add a title and description
st.title("Alejandra Scott")
st.markdown("This dashboard analyzes a dataset of *Airbnb* listings in Madrid.")

# Load the dataset
df = pd.read_csv("airbnb.csv")

# Display basic information about the dataset
st.subheader("Dataset Overview")
st.dataframe(df.head())

# Sidebar for filtering data by Neighbourhood Group and price range
st.sidebar.header("Filters")

# Select Neighborhood Group
neighbourhood_group = st.sidebar.selectbox("Select Neighbourhood Group", df["neighbourhood_group"].unique())

# Filter the data based on the selected neighbourhood group
df_filtered = df[df["neighbourhood_group"] == neighbourhood_group]

# Add a slider to filter by price range
price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=int(df["price"].min()),
    max_value=int(df["price"].max()),
    value=(0, 100)
)

# Filter the dataframe based on the selected price range
df_filtered = df_filtered[(df_filtered["price"] >= price_range[0]) & (df_filtered["price"] <= price_range[1])]

# Add a column layout for better organization
col1, col2 = st.columns(2)

# Tabbed layout for multiple views
tab1, tab2 = st.tabs(["Tab 1: Price Distribution", "Tab 2: Reviews per Month"])

with tab1:
    st.subheader(f"Price Distribution by Neighbourhood for {neighbourhood_group}")
    price_distribution = df_filtered.groupby("neighbourhood")["price"].mean()
    st.bar_chart(price_distribution)

with tab2:
    st.subheader(f"Reviews per Month in {neighbourhood_group}")
    reviews_per_month = df_filtered.groupby("neighbourhood")["reviews_per_month"].mean()
    st.bar_chart(reviews_per_month)

# Create additional graphs below tabs

# 1. Graph to study the relationship between listing type and number of people (using calculated_host_listings_count)
st.subheader("Graph: Listing Type vs Number of People")
listing_type_vs_people = df.groupby("room_type")["calculated_host_listings_count"].mean()  # Use this column as a proxy for number of people
st.bar_chart(listing_type_vs_people)

# 2. Graph to explore the price by listing type
st.subheader("Graph: Price by Listing Type")
price_by_listing_type = df.groupby("room_type")["price"].mean()
st.bar_chart(price_by_listing_type)

# 3. Graph to display the apartments with the highest number of reviews per month, broken down by neighborhood
st.subheader("Graph: Top Apartments by Reviews Per Month")
df_reviews_per_month = df.groupby(["neighbourhood", "name"])["reviews_per_month"].mean().reset_index()
df_reviews_per_month = df_reviews_per_month.sort_values(by="reviews_per_month", ascending=False)

# Display the top 10 apartments with the highest reviews per month in a table
st.dataframe(df_reviews_per_month.head(10))

# 4. Graph showing the relationship between the number of reviews and the price
st.subheader("Graph: Relationship Between Reviews and Price")
# Using a scatter plot to show the relationship between reviews and price
st.scatter_chart(df[["reviews_per_month", "price"]])

# Simulator: User inputs apartment details to get a recommended price range
st.sidebar.header("Price Range Simulator")

# Get user inputs
neighborhood_input = st.sidebar.selectbox("Select Neighborhood", df["neighbourhood_group"].unique())
listing_type_input = st.sidebar.selectbox("Select Listing Type", df["room_type"].unique())
accommodates_input = st.sidebar.slider("Select Number of People (Accommodates)", 1, 16, 1)

# Filter data based on user inputs
df_simulator = df[(df["neighbourhood_group"] == neighborhood_input) & 
                  (df["room_type"] == listing_type_input) & 
                  (df["calculated_host_listings_count"] == accommodates_input)]  # Adjusted the column here

# Calculate the recommended price range
if len(df_simulator) > 0:
    min_price_simulator = df_simulator["price"].min()
    max_price_simulator = df_simulator["price"].max()
    st.sidebar.write(f"The recommended price range for your apartment is between €{min_price_simulator} and €{max_price_simulator}.")
else:
    st.sidebar.write("No data available for the selected criteria. Please try different options.")
