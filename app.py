import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# Load Data
df = pd.read_csv("datasets/indian_food_cleaned.csv")

# Page Config
st.set_page_config(page_title="Indian Food Dashboard", layout="wide")

# Set background image and theme
dark_bg = """
<style>
.stApp {
    background-image: url("https://i0.wp.com/www.tusktravel.com/blog/wp-content/uploads/2020/10/North-Indian-Food-Top-10-Must-Eat-Local-Dishes.jpg?w=1024&ssl=1");
    background-size: cover;
    background-attachment: fixed;
    background-repeat: no-repeat;
    background-position: center;
}
.block-container {
    background-color: rgba(255, 255, 255, 0.65);
    padding: 2rem;
    border-radius: 10px;
}
</style>
"""
st.markdown(dark_bg, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h1 style='color:#B22222;'>🍛 Filters</h2>", unsafe_allow_html=True)
    selected_state = st.selectbox("Select a State", ["All"] + sorted(df["state"].dropna().unique().tolist()))
    selected_flavor = st.selectbox("Select a Flavor", ["All"] + sorted(df["flavor_profile"].dropna().unique().tolist()))

    # Apply Filters
    filtered_df = df.copy()
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df["state"] == selected_state]
    if selected_flavor != "All":
        filtered_df = filtered_df[filtered_df["flavor_profile"] == selected_flavor]

    filtered_df["total_time"] = filtered_df["prep_time"] + filtered_df["cook_time"]

    # Sidebar Pie Chart
    # Sidebar Pie Chart
# Sidebar Pie Chart
# Sidebar Pie Chart
with st.sidebar:
    st.markdown("## 🥗 Diet Distribution")
    diet_counts = filtered_df["diet"].value_counts().reset_index()
    diet_counts.columns = ['Diet Type', 'Count']
    fig_sidebar = px.pie(
        diet_counts, names='Diet Type', values='Count', 
        color_discrete_sequence=['#F4A261', '#E76F51']
    )

    # Custom size and removing unnecessary margins
    fig_sidebar.update_layout(
        width=350,  # Adjust to your desired width for better fit in sidebar
        height=350,  # Adjust to your desired height
        margin=dict(t=10, b=10, l=10, r=10)  # Set small margins to reduce space
    )

    # Plot the chart in the sidebar with the exact size
    st.plotly_chart(fig_sidebar, use_container_width=False)

# --- Title ---
st.markdown("<h1 style='color:#b44e39;'>Indian Cuisine Analysis Dashboard</h1>", unsafe_allow_html=True)

# --- KPIs ---
most_common_flavor = filtered_df["flavor_profile"].mode()[0] if not filtered_df["flavor_profile"].mode().empty else "N/A"
most_common_course = filtered_df["course"].mode()[0] if not filtered_df["course"].mode().empty else "N/A"
ingredient_list = filtered_df["ingredients"].dropna().str.split(", ")
flattened = [ingredient.strip().lower() for sublist in ingredient_list for ingredient in sublist]
ingredient_counts = Counter(flattened)
most_common_ingredient = ingredient_counts.most_common(1)[0][0] if ingredient_counts else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("🍛 Most Common Flavor", most_common_flavor.title())
col2.metric("🍽️ Most Common Course", most_common_course.title())
col3.metric("🧂 Most Used Ingredient", most_common_ingredient.title())

# --- Charts ---
st.markdown("### 🍲 Visual Insights")

# Row 1
row1_col1, row1_col2 = st.columns(2)
region_counts = filtered_df["region"].value_counts().reset_index()
region_counts.columns = ["Region", "Dish Count"]
fig_region = px.bar(
    region_counts, x="Region", y="Dish Count", color="Dish Count",
    color_continuous_scale=px.colors.sequential.Oranges, title="Dish Count by Region"
)
row1_col1.plotly_chart(fig_region, use_container_width=True)

flavor_counts = filtered_df["flavor_profile"].value_counts().reset_index()
flavor_counts.columns = ["Flavor", "Count"]
fig_flavor = px.pie(
    flavor_counts, names="Flavor", values="Count", title="Flavor Profiles",
    color_discrete_sequence=['#E07A5F', '#F2CC8F', '#81B29A', '#3D405B', '#F4F1DE']
)
row1_col2.plotly_chart(fig_flavor, use_container_width=True)

# Row 2 (Full Width)
diet_state = filtered_df.groupby(["state", "diet"]).size().reset_index(name="count")
fig_diet = px.bar(
    diet_state, x="state", y="count", color="diet", barmode="stack",
    color_discrete_sequence=['#F4A261', '#2A9D8F'], title="State-wise Diet Split"
)
fig_diet.update_layout(xaxis_tickangle=45, height=400)
st.plotly_chart(fig_diet, use_container_width=True)

# Row 3
row3_col1, row3_col2 = st.columns(2)
color_sequence = ['#E76F51', '#F4A261', '#2A9D8F', '#264653', '#E9C46A']

fig_total_box = px.box(
    filtered_df, x="course", y="total_time", color="course",
    title="Total Time Distribution by Course",
    color_discrete_sequence=color_sequence
)
row3_col1.plotly_chart(fig_total_box, use_container_width=True)

ingredient_series = filtered_df["ingredients"].dropna().apply(lambda x: [i.strip().lower() for i in x.split(",")])
all_ingredients = [ingredient for sublist in ingredient_series for ingredient in sublist]
top_ingredients = Counter(all_ingredients).most_common(5)
ingredient_df = pd.DataFrame(top_ingredients, columns=["Ingredient", "Count"])
fig_ing = px.bar(
    ingredient_df, x="Count", y="Ingredient", orientation="h",
    title="Top 5 Ingredients Used", color="Count",
    color_continuous_scale=px.colors.sequential.Oranges
)
row3_col2.plotly_chart(fig_ing, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>📊 Created by an Aspiring Data Analyst | Project: Indian Cuisine Analytics</p>", unsafe_allow_html=True)
