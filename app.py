import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Global Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: white;
}

[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #333;
    padding: 15px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = px.data.gapminder()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🌍 Dashboard Filters")

continent = st.sidebar.multiselect(
    "Select Continent",
    options=df["continent"].unique(),
    default=df["continent"].unique()
)

filtered_continent = df[df["continent"].isin(continent)]

country = st.sidebar.selectbox(
    "Select Country",
    sorted(filtered_continent["country"].unique())
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (1980, 2007)
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = filtered_continent[
    (filtered_continent["country"] == country) &
    (filtered_continent["year"] >= year_range[0]) &
    (filtered_continent["year"] <= year_range[1])
]

latest_data = filtered_df.iloc[-1]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("📈 Global Analytics Dashboard")

st.markdown(
    "Interactive Streamlit dashboard built using Plotly and Pandas."
)

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌍 Country",
        latest_data["country"]
    )

with col2:
    st.metric(
        "👥 Population",
        f"{latest_data['pop']:,}"
    )

with col3:
    st.metric(
        "💰 GDP Per Capita",
        f"${latest_data['gdpPercap']:,.0f}"
    )

with col4:
    st.metric(
        "❤️ Life Expectancy",
        f"{latest_data['lifeExp']:.1f} yrs"
    )

st.divider()

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "📊 GDP Analysis",
    "🌎 Population Insights",
    "📋 Raw Data"
])

# ---------------------------------------------------
# TAB 1
# ---------------------------------------------------

with tab1:

    col1, col2 = st.columns(2)

    with col1:

        fig_gdp = px.line(
            filtered_df,
            x="year",
            y="gdpPercap",
            markers=True,
            title=f"GDP Per Capita Trend - {country}",
            template="plotly_dark"
        )

        st.plotly_chart(fig_gdp, use_container_width=True)

    with col2:

        fig_life = px.area(
            filtered_df,
            x="year",
            y="lifeExp",
            title=f"Life Expectancy Trend - {country}",
            template="plotly_dark"
        )

        st.plotly_chart(fig_life, use_container_width=True)

# ---------------------------------------------------
# TAB 2
# ---------------------------------------------------

with tab2:

    col1, col2 = st.columns(2)

    with col1:

        fig_pop = px.bar(
            filtered_df,
            x="year",
            y="pop",
            color="year",
            title=f"Population Growth - {country}",
            template="plotly_dark"
        )

        st.plotly_chart(fig_pop, use_container_width=True)

    with col2:

        latest_year = df["year"].max()

        world_df = df[df["year"] == latest_year]

        fig_scatter = px.scatter(
            world_df,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            hover_name="country",
            log_x=True,
            size_max=60,
            title="GDP vs Life Expectancy",
            template="plotly_dark"
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------------------------
# TAB 3
# ---------------------------------------------------

with tab3:

    st.subheader("Filtered Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇ Download Data",
        csv,
        "filtered_data.csv",
        "text/csv"
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()
