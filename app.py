import streamlit as st
import sys
import os
import json
from src.config import cerebras_llm
from src.crew import create_crew  # Assuming you have a function that creates the crew setup

# Ensure the src folder is part of the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Function to run the entire crew
def run_crew(product_name, country, model_name):
    # Create the crew with agents and tasks
    event_management_crew = create_crew(product_name, country, model_name)

    # Format the input for the crew
    event_details = {'product': product_name, 'country': country, 'model': model_name}

    # Execute Crew (this will run all the tasks)
    event_analysis = event_management_crew.kickoff(inputs=event_details)
    
    return event_analysis

# Function to clean the output and remove unwanted fields
def clean_output(output):
    if isinstance(output, dict):
        output = json.dumps(output, indent=4)
        output = output.replace('"pydantic":null,', '')
        output = output.replace('"json_dict":null,', '')
        output = output.replace('"tasks_output":[]', '')
        output = output.replace('"token_usage":', '')
        return output
    return output

# Streamlit Page Config
st.set_page_config(page_title="AI Price Comparator", page_icon="🛒", layout="wide")

# Initialize session states for history and reports
if 'history' not in st.session_state:
    st.session_state.history = []
if 'reports' not in st.session_state:
    st.session_state.reports = {}

# Sidebar for API Key Uploads, History, and Model Selection
with st.sidebar:
    st.header("🔑 **API Keys**")
    cerebras_api_key = st.text_input("🧠 Cerebras API Key", type="password")
    serper_api_key = st.text_input("🔍 Serper API Key", type="password")
    
    # Model Selection
    # Sidebar Model Selection
    st.header("🧠 **Select Model**")
    model_name = st.selectbox(
        "Choose a Model",
        ["cerebras/llama-3.1-8b", "cerebras/llama-3.3-70b", "cerebras/deepseek-r1-distill-llama-70b"]
    )

    # History Tab
    st.header("📜 **Search History**")
    if st.session_state.history:
        for idx, search in enumerate(st.session_state.history):
            if st.button(f"🔎 {search['product_name']} in {search['country']}", key=f"search_{idx}"):
                st.session_state.selected_search = search  # Store selected search
                st.rerun()
    else:
        st.write("No previous searches yet.")

# **Main UI**
st.markdown("## 🚀 **Welcome to the Price Comparison Tool!** 🛒")
st.write("Enter the product details below to compare prices across multiple platforms. 📉")

# **Inputs for product and country (always visible)**
selected_search = st.session_state.get('selected_search', {})

product_name = st.text_input(
    "💡 **Product Name**", 
    selected_search.get('product_name', "Sony WH-1000XM5")
)
country = st.text_input(
    "🌍 **Country**", 
    selected_search.get('country', "United States")
)

# **Button to compare prices**
if st.button("🔍 **Compare Prices**", help="Click to analyze prices and get a detailed comparison"):
    if product_name and country:
        st.write(f"🛒 **Analyzing prices for** **{product_name}** in **{country}**... 📈")

        # Run the crew and get the results
        event_analysis = run_crew(product_name, country, model_name)

        # Clean the output and display the results
        cleaned_output = clean_output(event_analysis)
        
        st.subheader("📊 **Price Comparison Report**")
        st.markdown(cleaned_output)

        # Store the search and report
        search_key = f"{product_name}_{country}"
        search_data = {'product_name': product_name, 'country': country, 'model_name': model_name}
        
        if search_data not in st.session_state.history:
            st.session_state.history.append(search_data)

        st.session_state.reports[search_key] = cleaned_output  # Save the report
        
        # Clear selected search after displaying results
        st.session_state.selected_search = {'product_name': product_name, 'country': country}
    else:
        st.error("❌ Please enter both product name and country.")

# **Display saved report if a past search is selected**
search_key = f"{product_name}_{country}"
if search_key in st.session_state.reports:
    st.subheader("📊 **Saved Price Comparison Report**")
    st.markdown(st.session_state.reports[search_key])

    # **Download Button for the Report**
    # report_json = st.session_state.reports[search_key].encode('utf-8')
    # st.download_button(
    #     label="📥 Download Report",
    #     data=report_json,
    #     file_name=f"{search_key}.json",
    #     mime="application/json"
    # )