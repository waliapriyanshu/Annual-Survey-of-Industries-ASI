import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="Indian Manufacturing Sectors Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for styling - improved visibility for text elements
st.markdown("""
<style>
    /* Improve text visibility */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Enhance section headers */
    h1, h2, h3 {
        color: #1e3a8a;
        font-weight: 700;
    }
    
    /* Improve button visibility */
    .stButton button {
        background-color: #1e88e5;
        color: white;
        font-weight: 600;
    }
    
    /* Enhance tab visibility */
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 5px;
        padding: 5px 10px;
        margin-right: 5px;
    }
    
    /* Active tab styling */
    .stTabs [aria-selected="true"] {
        background-color: #1e88e5 !important;
        color: white !important;
    }
    
    /* Improve metric visibility */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    
    /* Container styling for better organization */
    .chart-container {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    
    /* Reduce white space in containers */
    .stContainer, .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Reduce margins between elements */
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Make chart containers more compact */
    .chart-container {
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Reduce padding in expanders */
    .streamlit-expanderContent {
        padding: 0.5rem;
    }
    
    /* Reduce space between tabs and content */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to load data
@st.cache_data
def load_data():
    try:
        # Load your excel file
        # Replace 'your_data.xlsx' with the path to your actual Excel file
        df_all_india = pd.read_excel('/Users/priyanshuwalia7/Downloads/ASI data.xlsx', sheet_name='Sheet1')
        df_kerala = pd.read_excel('/Users/priyanshuwalia7/Downloads/ASI data.xlsx', sheet_name='Sheet2')
        df_haryana = pd.read_excel('/Users/priyanshuwalia7/Downloads/ASI data.xlsx', sheet_name='Sheet3')
        
        # Combine all dataframes into one
        combined_df = pd.concat([df_all_india, df_kerala, df_haryana], ignore_index=True)
        
        # Create a time series dataframe for analysis over years
        # Extract unique years from the data
        years = combined_df['Year'].unique().tolist()
        states = combined_df['State'].unique().tolist()
        
        # Prepare time series data (extracting from your existing data)
        time_df = combined_df.copy()
        
        return combined_df, time_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Return empty dataframes to prevent app from crashing
        return pd.DataFrame(), pd.DataFrame()

# Function to upload Excel file
def upload_excel_file():
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # Read all sheets
            sheet_names = pd.ExcelFile(uploaded_file).sheet_names
            sheet_dfs = []
            
            for sheet in sheet_names:
                df = pd.read_excel(uploaded_file, sheet_name=sheet)
                # Add sheet name as source if not already in columns
                if 'Source' not in df.columns:
                    df['Source'] = sheet
                sheet_dfs.append(df)
            
            # Combine all dataframes
            combined_df = pd.concat(sheet_dfs, ignore_index=True)
            
            # Create a time series dataframe
            time_df = combined_df.copy()
            
            return combined_df, time_df
        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")
            return pd.DataFrame(), pd.DataFrame()
    else:
        # If no file is uploaded, load sample data
        return load_data()

# Load data from uploaded file or use sample data
df, time_df = upload_excel_file()

# Dashboard header with improved styling
st.title("🏭 Indian Manufacturing Sectors Dashboard")
st.markdown("<p style='font-size: 1.2rem; color: #334155;'>An interactive exploration of manufacturing sectors across India</p>", unsafe_allow_html=True)

if df.empty:
    st.warning("Please upload your Excel file using the uploader in the sidebar.")
else:
    # Create tabs for different views with improved styling
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 **Sector Analysis**", 
        "🗺️ **Regional Distribution**", 
        "📈 **Time Series Analysis**", 
        "ℹ️ **About**"
    ])

    # Tab 1: Sector Analysis with improved visibility
    with tab1:
        st.markdown("<h2 style='color: #1e3a8a; font-weight: 700;'>Manufacturing Sector Analysis</h2>", unsafe_allow_html=True)
        
        # Control panel with improved organization
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Control Panel")
            col1, col2 = st.columns(2)
            
            with col1:
                # Get unique NIC descriptions from the data
                nic_descriptions = df['NIC Description'].unique()
                num_sectors = st.slider(
                    "Number of top sectors to display", 
                    min_value=5, 
                    max_value=min(15, len(nic_descriptions)), 
                    value=min(10, len(nic_descriptions))
                )
            
            with col2:
                chart_type = st.selectbox(
                    "Select chart type", 
                    ["Bar Chart", "Pie Chart", "Treemap"]
                )
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Main content area with better organization
        col1, col2 = st.columns([2, 1])
        
        # Filter for manufacturing sectors only
        manufacturing_df = df[df['NIC Description'].str.contains('Manufactur', case=False, na=False)]
        
        # If no manufacturing sectors are found, use all data
        if manufacturing_df.empty:
            manufacturing_df = df
            st.info("No specific 'Manufacture' entries found, displaying all sectors.")
        
        # Prepare data - group by NIC Description and sum values
        try:
            # Ensure 'Value' column exists and is numeric
            if 'Value' in manufacturing_df.columns:
                manufacturing_df['Value'] = pd.to_numeric(manufacturing_df['Value'], errors='coerce')
                top_factories = manufacturing_df.groupby('NIC Description')['Value'].sum().nlargest(num_sectors)
            else:
                # Try to find a value column based on columns containing "value" or similar
                value_cols = [col for col in manufacturing_df.columns if 'value' in col.lower() or 'count' in col.lower() or 'number' in col.lower()]
                if value_cols:
                    value_col = value_cols[0]
                    manufacturing_df[value_col] = pd.to_numeric(manufacturing_df[value_col], errors='coerce')
                    top_factories = manufacturing_df.groupby('NIC Description')[value_col].sum().nlargest(num_sectors)
                else:
                    st.error("Could not identify a value column in the data.")
                    top_factories = pd.Series()
        except Exception as e:
            st.error(f"Error processing sector data: {e}")
            top_factories = pd.Series()
        
        if not top_factories.empty:
            # Process labels for better display
            short_labels = []
            for label in top_factories.index:
                if isinstance(label, str) and 'Manufacture of' in label:
                    short_label = label.replace('Manufacture of', '').strip()
                    if len(short_label) > 25:
                        short_label = short_label[:22] + '...'
                    short_labels.append(short_label)
                else:
                    short_labels.append(str(label))
            
            # Create DataFrame for plotting
            plot_df = pd.DataFrame({
                'Sector': short_labels,
                'Factories': top_factories.values
            })
            
            # Visualization based on selected chart type with improved styling
            with col1:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                if chart_type == "Bar Chart":
                    st.markdown(f"<h3 style='color: #1e3a8a;'>Top {num_sectors} Manufacturing Sectors by Number of Factories</h3>", unsafe_allow_html=True)
                    fig = px.bar(
                        plot_df,
                        x='Sector',
                        y='Factories',
                        color='Factories',
                        color_continuous_scale='viridis',
                        text_auto='.2s',
                        height=600
                    )
                    fig.update_layout(
                        xaxis_title="Manufacturing Sector",
                        yaxis_title="Number of Factories",
                        font=dict(size=12),
                        xaxis={'categoryorder':'total descending'},
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(t=30, b=100, l=80, r=40)
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                
                elif chart_type == "Pie Chart":
                    st.markdown(f"<h3 style='color: #1e3a8a;'>Distribution of Top {num_sectors} Manufacturing Sectors</h3>", unsafe_allow_html=True)
                    fig = px.pie(
                        plot_df,
                        values='Factories',
                        names='Sector',
                        color_discrete_sequence=px.colors.sequential.Viridis,
                        height=600
                    )
                    fig.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        hole=0.4,
                        pull=[0.05 if i == 0 else 0 for i in range(len(plot_df))]
                    )
                    fig.update_layout(
                        font=dict(size=12),
                        legend_title_text='Sectors',
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(t=30, b=50, l=40, r=40)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                elif chart_type == "Treemap":
                    st.markdown(f"<h3 style='color: #1e3a8a;'>Treemap of Top {num_sectors} Manufacturing Sectors</h3>", unsafe_allow_html=True)
                    fig = px.treemap(
                        plot_df,
                        path=['Sector'],
                        values='Factories',
                        color='Factories',
                        color_continuous_scale='viridis',
                        height=600
                    )
                    fig.update_layout(
                        font=dict(size=14),
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(t=30, b=30, l=30, r=30)
                    )
                    # Fix the textinfo parameter - use a valid value
                    fig.update_traces(textinfo="label+value")
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Statistics and insights with improved styling
            with col2:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: #1e3a8a;'>Key Statistics</h3>", unsafe_allow_html=True)
                
                total_factories = int(top_factories.sum())
                st.metric("Total Factories", f"{total_factories:,}")
                
                if not plot_df.empty:
                    top_sector = plot_df.iloc[0]['Sector']
                    top_count = int(plot_df.iloc[0]['Factories'])
                    st.metric("Largest Sector", top_sector, f"{top_count:,} factories")
                    
                    avg_factories = int(top_factories.mean())
                    st.metric("Average Factories per Sector", f"{avg_factories:,}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Sector comparison with improved styling
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: #1e3a8a;'>Sector Comparison</h3>", unsafe_allow_html=True)
                
                selected_sectors = st.multiselect(
                    "Select sectors to compare",
                    options=plot_df['Sector'].tolist(),
                    default=plot_df['Sector'].tolist()[:min(3, len(plot_df))]
                )
                
                if selected_sectors:
                    comparison_df = plot_df[plot_df['Sector'].isin(selected_sectors)]
                    fig = px.bar(
                        comparison_df,
                        x='Sector',
                        y='Factories',
                        color='Sector',
                        height=300
                    )
                    fig.update_layout(
                        showlegend=False,
                        xaxis_title="",
                        yaxis_title="Factories",
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(t=20, b=30, l=60, r=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No sector data available for analysis. Please check your data format.")

    # Tab 2: Regional Distribution
    with tab2:
        st.markdown("<h2 style='color: #1e3a8a; font-weight: 700;'>Regional Distribution of Manufacturing</h2>", unsafe_allow_html=True)
        
        # Control panel
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Control Panel")
        col1, col2 = st.columns(2)
        
        with col1:
            # Get unique NIC descriptions
            nic_options = df['NIC Description'].unique().tolist()
            if nic_options:
                selected_sector = st.selectbox(
                    "Select manufacturing sector",
                    options=nic_options,
                    index=0
                )
            else:
                selected_sector = ""
                st.error("No NIC Descriptions found in the data.")
        
        with col2:
            map_metric = st.selectbox(
                "Map metric",
                options=["Total factories", "Percentage of national total"]
            )
        st.markdown("</div>", unsafe_allow_html=True)
        
        if selected_sector:
            # Filter data based on selection
            sector_df = df[df['NIC Description'] == selected_sector].copy()
            
            if not sector_df.empty:
                # Ensure 'Value' column is numeric
                value_col = 'Value'
                if value_col in sector_df.columns:
                    sector_df[value_col] = pd.to_numeric(sector_df[value_col], errors='coerce')
                else:
                    # Try to identify a value column
                    value_cols = [col for col in sector_df.columns if 'value' in col.lower() or 'count' in col.lower() or 'number' in col.lower()]
                    if value_cols:
                        value_col = value_cols[0]
                        sector_df[value_col] = pd.to_numeric(sector_df[value_col], errors='coerce')
                    else:
                        st.error("Could not identify a value column for regional distribution.")
                        value_col = None
                
                if value_col:
                    # Group by state and sum values
                    state_totals = sector_df.groupby('State')[value_col].sum().reset_index()
                    
                    # Calculate percentages if needed
                    if map_metric == "Percentage of national total":
                        total = state_totals[value_col].sum()
                        state_totals['Percentage'] = (state_totals[value_col] / total * 100).round(1)
                        map_column = 'Percentage'
                        map_title = f"Percentage Distribution of {selected_sector.replace('Manufacture of', '')}"
                        hover_data = {'Percentage': ':.1f%'}
                        colorbar_title = "% of Total"
                    else:
                        map_column = value_col
                        map_title = f"Number of {selected_sector.replace('Manufacture of', '')} Factories by State"
                        hover_data = {value_col: ':,'}
                        colorbar_title = "Factories"
                    
                    # Split into columns
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                        # Create bar chart of states
                        fig = px.bar(
                            state_totals.sort_values(map_column, ascending=False),
                            x='State',
                            y=map_column,
                            color=map_column,
                            color_continuous_scale='Viridis',
                            title=map_title,
                            height=600,
                            text_auto='.2s' if map_metric == "Total factories" else '.1f%'
                        )
                        fig.update_layout(
                            xaxis_title="State",
                            yaxis_title=colorbar_title,
                            xaxis={'categoryorder':'total descending'},
                            plot_bgcolor='rgba(0,0,0,0)',
                            margin=dict(t=50, b=50, l=60, r=40)
                        )
                        fig.update_xaxes(tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.info("Note: In a production application, this could be replaced with an actual choropleth map of Indian states using GeoJSON data.")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                        st.markdown("<h3 style='color: #1e3a8a;'>Top 5 States</h3>", unsafe_allow_html=True)
                        top_states = state_totals.sort_values(map_column, ascending=False).head(5)
                        
                        for i, row in top_states.iterrows():
                            state = row['State']
                            value = row[map_column]
                            
                            if map_metric == "Percentage of national total":
                                value_display = f"{value:.1f}%"
                            else:
                                value_display = f"{int(value):,}"
                            
                            st.markdown(f"**{i+1}. {state}**: {value_display}")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # State comparison
                        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                        st.markdown("<h3 style='color: #1e3a8a;'>State Comparison</h3>", unsafe_allow_html=True)
                        
                        selected_states = st.multiselect(
                            "Select states to compare",
                            options=state_totals['State'].tolist(),
                            default=state_totals.nlargest(min(3, len(state_totals)), map_column)['State'].tolist()
                        )
                        
                        if selected_states:
                            comparison_df = state_totals[state_totals['State'].isin(selected_states)]
                            fig = px.pie(
                                comparison_df,
                                values=map_column,
                                names='State',
                                height=300
                            )
                            fig.update_traces(textposition='inside', textinfo='percent+label')
                            st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("No valid value column found for regional analysis.")
            else:
                st.warning(f"No data available for the selected sector: {selected_sector}")
        else:
            st.warning("Please select a sector for regional distribution analysis.")

    # Tab 3: Time Series Analysis
    with tab3:
        st.markdown("<h2 style='color: #1e3a8a; font-weight: 700;'>Time Series Analysis</h2>", unsafe_allow_html=True)
        
        # Check if 'Year' column exists
        if 'Year' in time_df.columns:
            # Convert Year to numeric to ensure sorting works correctly
            time_df['Year'] = pd.to_numeric(time_df['Year'], errors='coerce')
            
            # Get unique years and sort them
            years = sorted(time_df['Year'].unique().tolist())
            
            if len(years) > 1:
                # Control panel with improved organization
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.subheader("Control Panel")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    states = sorted(time_df['State'].unique().tolist())
                    selected_state = st.selectbox(
                        "Select state",
                        options=['All States'] + states
                    )
                
                with col2:
                    sectors = sorted(time_df['NIC Description'].unique().tolist())
                    selected_time_sector = st.selectbox(
                        "Select sector",
                        options=['All Sectors'] + sectors,
                        key="time_sector"
                    )
                
                with col3:
                    trend_type = st.selectbox(
                        "Trend visualization",
                        options=["Line chart", "Area chart", "Bar chart"]
                    )
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Determine value column
                value_col = 'Value'
                if value_col not in time_df.columns:
                    value_cols = [col for col in time_df.columns if 'value' in col.lower() or 'count' in col.lower() or 'number' in col.lower()]
                    if value_cols:
                        value_col = value_cols[0]
                    else:
                        st.error("Could not identify a value column for time series analysis.")
                        value_col = None
                
                if value_col:
                    # Ensure value column is numeric
                    time_df[value_col] = pd.to_numeric(time_df[value_col], errors='coerce')
                    
                    # Filter data based on selection
                    if selected_state == 'All States' and selected_time_sector == 'All Sectors':
                        filtered_time_df = time_df.groupby('Year')[value_col].sum().reset_index()
                        chart_title = "Overall Growth in Manufacturing (All Sectors, All States)"
                    elif selected_state == 'All States':
                        filtered_time_df = time_df[time_df['NIC Description'] == selected_time_sector].groupby('Year')[value_col].sum().reset_index()
                        chart_title = f"Growth in {selected_time_sector.replace('Manufacture of', '')} (All States)"
                    elif selected_time_sector == 'All Sectors':
                        filtered_time_df = time_df[time_df['State'] == selected_state].groupby('Year')[value_col].sum().reset_index()
                        chart_title = f"Overall Manufacturing Growth in {selected_state} (All Sectors)"
                    else:
                        filtered_time_df = time_df[(time_df['State'] == selected_state) & (time_df['NIC Description'] == selected_time_sector)].groupby('Year')[value_col].sum().reset_index()
                        chart_title = f"Growth in {selected_time_sector.replace('Manufacture of', '')} in {selected_state}"
                    
                    # Ensure data is sorted by year
                    filtered_time_df = filtered_time_df.sort_values('Year')
                    
                    # Main visualization container
                    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                    
                    # Calculate growth metrics if data is available
                    if not filtered_time_df.empty and len(filtered_time_df) > 1:
                        first_year = filtered_time_df.iloc[0]['Year']
                        last_year = filtered_time_df.iloc[-1]['Year']
                        first_value = filtered_time_df.iloc[0][value_col]
                        last_value = filtered_time_df.iloc[-1][value_col]
                        
                        if first_value > 0:  # Avoid division by zero
                            total_growth = ((last_value - first_value) / first_value * 100).round(2)
                            cagr = ((last_value / first_value) ** (1 / (last_year - first_year)) - 1) * 100
                        else:
                            total_growth = 0
                            cagr = 0
                        
                        # Display metrics
                        col1, col2, col3 = st.columns(3)
                        col1.metric(f"First Year ({int(first_year)})", f"{int(first_value):,}")
                        col2.metric(f"Last Year ({int(last_year)})", f"{int(last_value):,}", f"{total_growth:.2f}% overall")
                        col3.metric("CAGR", f"{cagr:.2f}%")
                        
                        # Create time series visualization
                        if trend_type == "Line chart":
                            fig = px.line(
                                filtered_time_df,
                                x='Year',
                                y=value_col,
                                markers=True,
                                title=chart_title,
                                height=500
                            )
                            fig.update_traces(line=dict(width=3))
                        elif trend_type == "Area chart":
                            fig = px.area(
                                filtered_time_df,
                                x='Year',
                                y=value_col,
                                title=chart_title,
                                height=500
                            )
                        else:  # Bar chart
                            fig = px.bar(
                                filtered_time_df,
                                x='Year',
                                y=value_col,
                                title=chart_title,
                                height=500,
                                text_auto='.2s'
                            )
                        
                        fig.update_layout(
                            xaxis_title="Year",
                            yaxis_title="Number of Factories",
                            plot_bgcolor='rgba(0,0,0,0)',
                            margin=dict(t=50, b=50, l=60, r=40)
                        )
                        fig.update_xaxes(dtick=1)  # Show all years
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Year-over-Year comparison
                        st.markdown("<h3 style='color: #1e3a8a;'>Year-over-Year Growth</h3>", unsafe_allow_html=True)
                        
                        # Calculate YoY growth
                        filtered_time_df['YoY Growth'] = filtered_time_df[value_col].pct_change() * 100
                        
                        # Drop the first year (which has NaN growth)
                        yoy_df = filtered_time_df.dropna()
                        
                        if not yoy_df.empty:
                            fig = px.bar(
                                yoy_df,
                                x='Year',
                                y='YoY Growth',
                                title="Year-over-Year Percentage Growth",
                                height=300,
                                text_auto='.1f'
                            )
                            
                            # Color bars based on positive/negative growth
                            fig.update_traces(
                                marker_color=['#4CAF50' if x >= 0 else '#F44336' for x in yoy_df['YoY Growth']]
                            )
                            
                            fig.update_layout(
                                xaxis_title="Year",
                                yaxis_title="Growth (%)",
                                plot_bgcolor='rgba(0,0,0,0)',
                                margin=dict(t=50, b=50, l=60, r=40)
                            )
                            fig.update_xaxes(dtick=1)
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("Not enough data points to calculate year-over-year growth.")
                    else:
                        st.warning("Not enough data available for the selected filters to perform time series analysis.")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # State comparison over time (if All States is not selected)
                    if selected_state != 'All States' and selected_time_sector != 'All Sectors':
                        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                        st.markdown("<h3 style='color: #1e3a8a;'>State Comparison Over Time</h3>", unsafe_allow_html=True)
                        
                        # Get top 5 states by most recent year value
                        top_states = time_df[time_df['NIC Description'] == selected_time_sector].groupby('State')[value_col].sum().nlargest(5).index.tolist()
                        
                        # Ensure the selected state is included
                        if selected_state not in top_states:
                            top_states[-1] = selected_state
                        
                        # Filter data for these states
                        comparison_df = time_df[
                            (time_df['State'].isin(top_states)) & 
                            (time_df['NIC Description'] == selected_time_sector)
                        ].groupby(['Year', 'State'])[value_col].sum().reset_index()
                        
                        # Create line chart comparing states
                        fig = px.line(
                            comparison_df,
                            x='Year',
                            y=value_col,
                            color='State',
                            title=f"Comparison of {selected_time_sector.replace('Manufacture of', '')} Across Top States",
                            height=400,
                            markers=True
                        )
                        
                        fig.update_layout(
                            xaxis_title="Year",
                            yaxis_title="Number of Factories",
                            plot_bgcolor='rgba(0,0,0,0)',
                            legend_title="State",
                            margin=dict(t=50, b=50, l=60, r=40)
                        )
                        fig.update_xaxes(dtick=1)
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("No valid value column found for time series analysis.")
            else:
                st.warning("Not enough time series data available. Multiple years are required for trend analysis.")
        else:
            st.warning("No 'Year' column found in the data for time series analysis.")

    # Tab 4: About
    with tab4:
        st.markdown("<h2 style='color: #1e3a8a; font-weight: 700;'>About this Dashboard</h2>", unsafe_allow_html=True)
        
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("""
        This interactive dashboard visualizes manufacturing sector data across India, providing insights into:
        
        - Distribution of manufacturing sectors across the country
        - Regional concentration of specific manufacturing activities
        - Growth trends over time for different sectors and states
        
        The data used in this dashboard is based on information from the Annual Survey of Industries (ASI) data from the Ministry of Statistics and Programme Implementation.
        
        The dashboard provides several interactive features:
        - Filter by sector, state, and time period
        - Compare sectors and states
        - Visualize trends over time
        - Analyze growth patterns and regional distribution
        
        Dashboard created using Streamlit | Data source: Annual Survey of Industries (ASI)
        
        """)
        st.markdown("</div>", unsafe_allow_html=True)