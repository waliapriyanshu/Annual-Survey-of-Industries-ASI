# Annual-Survey-of-Industries-ASI
A comprehensive interactive dashboard for visualizing and analyzing India's manufacturing sectors using Annual Survey of Industries (ASI) data.

## Dashboard Preview
![Dashboard Preview](https://dashboardasi.streamlit.app))

### Features
- **Sector Analysis**: Explore top manufacturing sectors by the number of factories.
- **Regional Distribution**: Visualize manufacturing distribution across Indian states.
- **Time Series Analysis**: Track growth trends over different time periods.
- **Multiple Visualization Options**: Bar charts, pie charts, treemaps, and more.

## Setup Guide

Follow these steps to set up and run the ASI Dashboard on your local system:

### 1. Clone the Repository
```bash
git clone https://github.com/waliapriyanshu/Annual-Survey-of-Industries-ASI.git
cd Annual-Survey-of-Industries-ASI
```
### 2. Download the ASI Dataset
Option 1: From esankhyiki:
- Visit the official ASI data portal: https://esankhyiki.mospi.gov.in/macroindicators?product=asi
- Navigate to the "Download" section.
- Click on "Download (CSV)" to obtain the latest ASI dataset.
- Save the downloaded file in the project directory.

Option 2: From Google Drive:
- Download the dataset directly from this Google Drive link: ```bash https://drive.google.com/file/d/10U5b7smwZoizWt51CBc5JFUeuZFccdVk/view```
- Save the downloaded file in the project directory.
### 3. Set Up a Virtual Environment (Recommended)
For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
### 4. Install Required Dependencies
Install all the necessary packages using the requirements.txt file:
```bash
pip install -r requirements.txt
```
This will install Streamlit, Pandas, Matplotlib, Plotly and other required libraries.

### 5. Run the Dashboard
Launch the Streamlit application:
```bash
streamlit run dashboard.py
```
The dashboard should open automatically in your default web browser

## Using the Dashboard

### Data Upload
You can upload your own Excel file using the sidebar uploader. The dashboard supports multiple sheets in a single Excel file. Ensure your data has columns for:
**NIC Description**
- State
- Year
- Value metrics

### Exploring Different Views
**Sector Analysis**:
- Adjust the number of sectors to display using the slider.
- Select different chart types (Bar Chart, Pie Chart, Treemap).
- Compare specific sectors using the comparison tool.
**Regional Distribution**:
- Select a specific manufacturing sector from the dropdown.
- Choose between total factory count or percentage views.
- Compare statistics across different states.
**Time Series Analysis**:
- Select a state and sector of interest.
- View growth trends over time with various visualization options.
- Analyze year-over-year growth and CAGR metrics.

## Troubleshooting
- Missing Data Columns: Ensure your dataset includes 'NIC Description', 'State', 'Year', and value columns.
- Value Column Detection: The dashboard attempts to identify value columns automatically, but will work best if columns contain terms like 'value', 'count', or 'number'.
- Browser Compatibility: For the best experience, use modern browsers like Chrome or Firefox.

## Acknowledgments
Data source: Annual Survey of Industries (ASI), Ministry of Statistics and Programme Implementation.
Dashboard created using Streamlit and Plotly.
