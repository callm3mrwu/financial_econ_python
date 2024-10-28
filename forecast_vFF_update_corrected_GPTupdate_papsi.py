import pandas as pd
import streamlit as st
import io
import requests
from openpyxl import load_workbook
import plotly.graph_objects as go
import math

# Set page config at the very beginning of the script
st.set_page_config(layout="wide")

# Updated URL of the Excel file
url = 'https://raw.githubusercontent.com/callm3mrwu/financial_econ_python/main/forecast_output_updated2.xlsx'

# Load the Excel file from the URL
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    excel_data = io.BytesIO(response.content)
    
    # Use openpyxl to load the workbook
    wb = load_workbook(excel_data, read_only=True, data_only=True)
    sheet = wb['forecast_output']
    
    # Convert the sheet to a DataFrame
    data = sheet.values
    columns = next(data)
    df = pd.DataFrame(data, columns=columns)
    
except Exception as e:
    st.error(f"Error loading the Excel file: {str(e)}")
    st.stop()

def create_interactive_chart(data, x_column, y_column, title, xlabel, format_func=lambda x: f'{x:.2f}'):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=data['Company Name'],
        x=data[x_column],
        orientation='h',
        text=[format_func(x) for x in data[x_column]],
        textposition='outside',
        hoverinfo='text',
        hovertext=[f"{company}: {format_func(value)}" for company, value in zip(data['Company Name'], data[x_column])],
        marker_color='lightblue',
        marker=dict(line=dict(width=1, color='black'))
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title="",
        height=500,
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showticklabels=False),
        hoverlabel=dict(bgcolor="white", font_size=12),
        hovermode="y"
    )
    
    # Add hover effect
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>%{hovertext}",
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    
    return fig

def display_multi_column_table(df, num_columns=3):
    num_rows = math.ceil(len(df) / num_columns)
    columns = st.columns(num_columns)
    
    for i in range(num_columns):
        with columns[i]:
            start_idx = i * num_rows
            end_idx = min((i + 1) * num_rows, len(df))
            st.table(df.iloc[start_idx:end_idx])

def main():
    st.title("SDAX Company Rankings")
    st.subheader("Most Investible to Least Investible, due to Refinancing Risk in 2025")

    # Sidebar for user input
    st.sidebar.header("Chart Settings")
    ranking_range = st.sidebar.selectbox(
        "Select ranking range",
        ["1-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70"]
    )

    # Convert ranking range to start and end indices
    start_idx = (int(ranking_range.split("-")[0]) - 1)
    end_idx = int(ranking_range.split("-")[1])

    # Chart for "Projected Interest Expense / Projected Net Income 2025"
    st.subheader("Ranking by Projected Interest Expense / Projected Net Income 2025 (Forecasted)")
    
    ratio_col = "Projected interest expense/ P. NetIncome 2025(forecasted)"
    
    if ratio_col in df.columns:
        sorted_df_interest_expense = df.sort_values(by=ratio_col, ascending=False)#.iloc[start_idx:end_idx] war vorher nicht auskommentiert
        
        #neu
        # DataFrame with non-negative values
        df_non_negative = sorted_df_interest_expense[sorted_df_interest_expense[ratio_col] >= 0]
        sorted_df_non_negative = df_non_negative.sort_values(by=ratio_col, ascending=True)
        

        # DataFrame with negative values
        df_negative = sorted_df_interest_expense[sorted_df_interest_expense[ratio_col] < 0]
        sorted_df_negative = df_negative.sort_values(by=ratio_col, ascending=True)
        
        #joining the 2 dataframes non-negative + negative values
        df_combined = pd.concat([sorted_df_negative, sorted_df_non_negative], axis=0).iloc[start_idx:end_idx]
        st.subheader("Combined Sorted DataFrame (Negative and Non-Negative Values)")
        #st.dataframe(df_combined)
        # bis hier neu

        #### 2. df combined (grosse positive Zahlen zuerst)
        # DataFrame with non-negative values
        df_non_negative_2 = sorted_df_interest_expense[sorted_df_interest_expense[eps_growth_col] >= 0]
        sorted_df_non_negative_2 = df_non_negative_2.sort_values(by=eps_growth_col, ascending=False)
        

        # DataFrame with negative values
        df_negative_2 = sorted_df_interest_expense[sorted_df_interest_expense[eps_growth_col] < 0]
        sorted_df_negative_2 = df_negative_2.sort_values(by=eps_growth_col, ascending=False)
        
        #joining the 2 dataframes non-negative + negative values
        df_combined_2 = pd.concat([sorted_df_non_negative_2,sorted_df_negative_2], axis=0).iloc[start_idx:end_idx]
        #### ende 2. df
        
        #3. dataframe combined
        # DataFrame with non-negative values
        df_non_negative_3 = sorted_df_interest_expense[sorted_df_interest_expense[eps_forecast_col] >= 0]
        sorted_df_non_negative_3 = df_non_negative_3.sort_values(by=eps_forecast_col, ascending=False)
        

        # DataFrame with negative values
        df_negative_3 = sorted_df_interest_expense[sorted_df_interest_expense[eps_forecast_col] < 0]
        sorted_df_negative_3 = df_negative_3.sort_values(by=eps_forecast_col, ascending=False)
        
        #joining the 3 dataframes non-negative + negative values
        df_combined_3 = pd.concat([sorted_df_non_negative_3,sorted_df_negative_3], axis=0).iloc[start_idx:end_idx]
        #### ende 3. df

        
        fig1 = create_interactive_chart(df_combined, #vorher: sorted_df_interest_expense
                            ratio_col,
                            "Company Name",
                            f"Ranking of Companies by Projected Interest Expense / Projected Net Income 2025 (Rank {ranking_range})",
                            "Interest Expense to Net Income Ratio",
                            lambda x: f'{x:.2f}x')  # Add 'x' after the number
        st.plotly_chart(fig1, use_container_width=True)
        
        # Display company names in a multi-column table
        display_multi_column_table(df_combined[["Company Name", ratio_col]].reset_index(drop=True))
    else:
        st.error(f"Column '{ratio_col}' not found in the DataFrame.")

    # Create two columns for the EPS charts
    col1, col2 = st.columns(2)

    with col1:
        # Chart for "EPS growth rates (2024-2025)"
        st.subheader("Ranking by EPS Growth Rates (2024-2025)")
        eps_growth_col = "EPS growth rates (2024-2025)"

        # Check if the column exists, if not, try an alternative name
        if eps_growth_col not in df.columns:
            eps_growth_col = "EPS growth rates (2024-2025) (%)"  # Try this alternative name

        if eps_growth_col in df.columns:
            #sorted_df_eps_growth = df.sort_values(by=eps_growth_col, ascending=True).iloc[start_idx:end_idx]
            fig2 = create_interactive_chart(df_combined_2,
                                eps_growth_col,
                                "Company Name",
                                f"Ranking by EPS Growth Rates (2024-2025) (Rank {ranking_range})",
                                "EPS Growth Rates (2024-2025)",
                                lambda x: f'{x:.2f}%')  # Display as percentage
            st.plotly_chart(fig2, use_container_width=True)
            
            # Display company names in a multi-column table
            display_multi_column_table(df_combined_2[["Company Name", eps_growth_col]].reset_index(drop=True))
        else:
            st.error(f"Column '{eps_growth_col}' not found in the DataFrame.")

    with col2:
        # Chart for "EPS forecasts 2025"
        st.subheader("Ranking by EPS Forecasts 2025")
        eps_forecast_col = "EPS forecasts 2025"

        # Check if the column exists, if not, try an alternative name
        if eps_forecast_col not in df.columns:
            eps_forecast_col = "EPS forecasts 2025 (€)"  # Try this alternative name

        if eps_forecast_col in df.columns:
            #sorted_df_eps_forecast = df.sort_values(by=eps_forecast_col, ascending=True).iloc[start_idx:end_idx]
            fig3 = create_interactive_chart(df_combined_3,
                                eps_forecast_col,
                                "Company Name",
                                f"Ranking by EPS Forecasts 2025 (Rank {ranking_range})",
                                "EPS Forecasts 2025 (in €)",
                                lambda x: f'{x:.2f}€')  # Add € symbol
            st.plotly_chart(fig3, use_container_width=True)
            
            # Display company names in a multi-column table
            display_multi_column_table(df_combined_3[["Company Name", eps_forecast_col]].reset_index(drop=True))
        else:
            st.error(f"Column '{eps_forecast_col}' not found in the DataFrame.")

if __name__ == "__main__":
    main()
