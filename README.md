# Project 5: Streamlit Workflow & Data Visualization

An interactive Streamlit web application designed to demonstrate the Streamlit execution model, reactive widget system, and various data visualization libraries.

## 🚀 Features

- **Streamlit Reactive Workflow:** Top-to-bottom re-execution explained with interactive widgets.
- **Built-in Charts:** Line charts, area charts, and bar charts using native Streamlit functions (`st.line_chart`, `st.area_chart`, `st.bar_chart`).
- **Interactive Plotly Visualizations:** Scatter plots and box plots with hover states and custom color palettes.
- **Matplotlib & Seaborn:** Distribution KDE plots and correlation heatmaps integrated via `st.pyplot`.
- **Metrics & KPIs:** Dynamic KPI cards with delta values.
- **Data Export:** Filtered data inspection and direct CSV download.

## 🛠️ Setup & Installation

1. **Activate the Virtual Environment:**
   - **PowerShell:**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **Command Prompt (CMD):**
     ```cmd
     .venv\Scripts\activate.bat
     ```

2. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```powershell
   streamlit run main.py
   ```
