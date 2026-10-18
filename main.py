import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ==============================================================================
# 1. STREAMLIT CONFIGURATION & WORKFLOW BASICS
# ==============================================================================
# Streamlit scripts execute from TOP to BOTTOM whenever:
# 1. The user first loads or refreshes the page.
# 2. Any widget (slider, selectbox, button, etc.) is interacted with.
#
# st.set_page_config MUST be the first Streamlit command in your script.
st.set_page_config(
    page_title="Streamlit Workflow & Visualizations Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Header
st.title("📊 Understanding Streamlit Workflow & Data Visualization")
st.markdown("""
Welcome to the Streamlit interactive walkthrough! This app illustrates:
- **Reactive Execution:** Every time you touch a widget, Streamlit reruns the script top-to-bottom with updated values.
- **Native Charts:** Quick built-in visualizations (`st.line_chart`, `st.bar_chart`, `st.area_chart`).
- **External Chart Libraries:** Integrating **Plotly** and **Matplotlib/Seaborn**.
- **Layouts & Containers:** Using columns, tabs, sidebars, and expanders.
""")

st.divider()

# ==============================================================================
# 2. SIDEBAR CONTROLS (WIDGETS & USER INPUT)
# ==============================================================================
# Widgets in st.sidebar automatically update variables when adjusted.
st.sidebar.header("⚙️ Controls & Parameters")
st.sidebar.caption("Interact with these inputs to see Streamlit's reactive rerun in action.")

# Number of sample data points
num_points = st.sidebar.slider("Number of Data Points:", min_value=50, max_value=500, value=150, step=25)

# Category selection
selected_categories = st.sidebar.multiselect(
    "Filter Categories:",
    options=["Category A", "Category B", "Category C"],
    default=["Category A", "Category B", "Category C"]
)

# Color theme for charts
chart_theme = st.sidebar.selectbox("Color Palette:", ["Viridis", "Plasma", "Cividis", "Spectral", "Coolwarm"])

# Random seed option to stabilize or randomize data
randomize = st.sidebar.checkbox("Randomize Data on Each Run", value=False)
seed = None if randomize else 42

# ==============================================================================
# 3. DATA GENERATION & CACHING
# ==============================================================================
# @st.cache_data prevents re-calculating expensive operations when inputs haven't changed.
@st.cache_data
def generate_sample_data(points: int, seed_value: int | None):
    if seed_value is not None:
        np.random.seed(seed_value)

    dates = pd.date_range(end=pd.Timestamp.today(), periods=points)
    
    # Generate random trends
    trend_a = np.cumsum(np.random.randn(points)) + 50
    trend_b = np.cumsum(np.random.randn(points)) + 30
    trend_c = np.cumsum(np.random.randn(points)) + 10

    df = pd.DataFrame({
        "Date": dates,
        "Category A": trend_a,
        "Category B": trend_b,
        "Category C": trend_c,
        "Volume": np.random.randint(100, 1000, size=points),
        "Score": np.random.normal(70, 15, size=points).clip(0, 100),
        "Group": np.random.choice(["Category A", "Category B", "Category C"], size=points)
    })
    return df

df = generate_sample_data(num_points, seed)

# Filter dataset based on sidebar selection
filtered_df = df[df["Group"].isin(selected_categories)]

# ==============================================================================
# 4. KEY METRICS ROW (st.columns & st.metric)
# ==============================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Records", value=len(filtered_df), delta=f"{len(filtered_df) - num_points} from full set")

with col2:
    avg_score = filtered_df["Score"].mean() if not filtered_df.empty else 0
    st.metric(label="Average Score", value=f"{avg_score:.2f}", delta="+2.4% vs last period")

with col3:
    total_volume = filtered_df["Volume"].sum() if not filtered_df.empty else 0
    st.metric(label="Total Volume", value=f"{total_volume:,}")

with col4:
    active_groups = len(filtered_df["Group"].unique())
    st.metric(label="Active Categories", value=active_groups)

st.divider()

# ==============================================================================
# 5. TABBED VISUALIZATION SECTION (st.tabs)
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Native Streamlit Charts", 
    "📊 Interactive Plotly", 
    "🎨 Matplotlib & Seaborn", 
    "🧠 Streamlit Workflow Guide"
])

# ------------------------------------------------------------------------------
# TAB 1: Streamlit Built-in Charts
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Streamlit Native Charts")
    st.write("Streamlit has built-in, lightweight chart elements based on Altair.")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**1. Time Series Line Chart (`st.line_chart`)**")
        available_cols = [c for c in ["Category A", "Category B", "Category C"] if c in selected_categories]
        if available_cols:
            st.line_chart(filtered_df.set_index("Date")[available_cols])
        else:
            st.info("Please select at least one category from the sidebar.")

    with col_chart2:
        st.markdown("**2. Cumulative Area Chart (`st.area_chart`)**")
        if available_cols:
            st.area_chart(filtered_df.set_index("Date")[available_cols])
        else:
            st.info("Please select at least one category from the sidebar.")

    st.markdown("**3. Categorical Bar Chart (`st.bar_chart`)**")
    if not filtered_df.empty:
        category_summary = filtered_df.groupby("Group")["Volume"].sum()
        st.bar_chart(category_summary)

# ------------------------------------------------------------------------------
# TAB 2: Plotly Interactive Visualizations
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Plotly Interactive Visualizations")
    st.write("Plotly provides rich, interactive hover states, zoom, and export features via `st.plotly_chart`.")
    
    if not filtered_df.empty:
        col_plot1, col_plot2 = st.columns(2)
        
        with col_plot1:
            fig_scatter = px.scatter(
                filtered_df,
                x="Volume",
                y="Score",
                color="Group",
                size="Score",
                hover_data=["Date"],
                title="Score vs. Volume by Category",
                color_continuous_scale=chart_theme
            )
            fig_scatter.update_layout(template="plotly_white")
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col_plot2:
            fig_box = px.box(
                filtered_df,
                x="Group",
                y="Score",
                color="Group",
                points="all",
                title="Distribution of Scores per Group"
            )
            fig_box.update_layout(template="plotly_white")
            st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.warning("No data available to plot. Please select categories from the sidebar.")

# ------------------------------------------------------------------------------
# TAB 3: Matplotlib & Seaborn
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Matplotlib & Seaborn Plots")
    st.write("Traditional data science visualization libraries render seamlessly via `st.pyplot(fig)`.")
    
    if not filtered_df.empty:
        col_sns1, col_sns2 = st.columns(2)
        
        with col_sns1:
            st.markdown("**Distribution & KDE Plot (Seaborn)**")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(data=filtered_df, x="Score", hue="Group", kde=True, ax=ax)
            ax.set_title("Score Density across Groups")
            st.pyplot(fig)
            plt.close(fig)

        with col_sns2:
            st.markdown("**Correlation Matrix (Seaborn Heatmap)**")
            fig, ax = plt.subplots(figsize=(6, 4))
            numeric_cols = filtered_df.select_dtypes(include=[np.number])
            sns.heatmap(numeric_cols.corr(), annot=True, cmap=chart_theme.lower(), fmt=".2f", ax=ax)
            ax.set_title("Feature Correlations")
            st.pyplot(fig)
            plt.close(fig)
    else:
        st.warning("No data to plot.")

# ------------------------------------------------------------------------------
# TAB 4: Streamlit Workflow Explanation
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("Streamlit Core Architecture & Workflow")
    st.markdown("""
    ### 1. The Reactive Execution Cycle
    Unlike web frameworks like Flask or Django where you configure routes and request handlers:
    - **Streamlit treats your entire script as the run routine.**
    - When a user interacts with a widget (e.g., changes a slider), Streamlit simply executes the script **from top to bottom again**.
    - Variables assigned to widgets (`selected_categories = st.sidebar.multiselect(...)`) automatically receive the updated state.

    ### 2. State & Caching
    - **`st.session_state`**: Stores variables across reruns (e.g. login tokens, counters, user sessions).
    - **`@st.cache_data`**: Caches function return values (e.g. loading large CSV files, model predictions) so your app stays fast.

    ### 3. Visual Layout Elements
    - **`st.sidebar`**: Side drawer for inputs and controls.
    - **`st.columns`**: Divides the horizontal space into multiple columns.
    - **`st.tabs`**: Groups related content into switchable tabs.
    - **`st.expander`**: Collapsible drawers for advanced data or raw tables.
    """)

# ==============================================================================
# 6. RAW DATA INSPECTION (st.expander)
# ==============================================================================
st.divider()
with st.expander("🔍 Click to inspect raw DataFrame"):
    st.dataframe(filtered_df, use_container_width=True)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
