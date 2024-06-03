
import streamlit as st
import pandas as pd
import numpy as np

import numpy as np
import matplotlib.pyplot as plt
# Function to calculate NPV
def calculate_npv(cash_flows, interest_rate):
    npvs = []
    for t, cash_flow in enumerate(cash_flows):
        npv = cash_flow / (1 + interest_rate) ** t
        npvs.append(npv)
    return npvs
# Define the interest rate
interest_rate = 0.05  # Example interest rate
# Define the cash flows for two scenarios
cash_flows_scenario_1 = [10, 10, 10, 10, 10, 10, 10, 10, 10 ,10]  # Example cash flows for scenario 1
cash_flows_scenario_2 = [-5, -7, 4, 0, 4, 15, 25, 40, 50, 55]  # Example cash flows for scenario 2


# Calculate NPV for each scenario
npvs_scenario_1 = calculate_npv(cash_flows_scenario_1, interest_rate)
npvs_scenario_2 = calculate_npv(cash_flows_scenario_2, interest_rate)

data1 = pd.DataFrame(npvs_scenario_1)
data2 = pd.DataFrame(npvs_scenario_2)

npArray = np.Array([npvs_scenario_1, npvs_scenario_2])
dataFull = pd.Dataframe(npArray)

#data = data.set_index()
st.bar_chart(data1)


# Create bar chart
#plt.figure(figsize=(10, 6))
# Calculate the positions for the bars
#bar_width = 0.35
#index = np.arange(len(cash_flows_scenario_1))
# Plot NPV bars for scenario 1
#plt.bar(index, npvs_scenario_1, color='skyblue', label='Cash Cow', width=bar_width)
# Plot NPV bars for scenario 2
#plt.bar(index + bar_width, npvs_scenario_2, color='orange', label='Question Mark', width=bar_width)
# Add title and labels
#plt.title('Cash Cow vs Question Mark')
#plt.xlabel('Year')
#plt.ylabel('Value')
# Set ticks and labels for X-axis
#plt.xticks(index + bar_width / 2, [f'Year {i+1}' for i in range(len(cash_flows_scenario_1))])
# Add legend
#plt.legend()
# Display the chart
#plt.show()
