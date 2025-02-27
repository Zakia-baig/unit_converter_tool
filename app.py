

import streamlit as st
from PIL import Image
import base64

# Page configuration
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        color: #2e7d32;
        text-align: center;
        font-size: 3.5em;
        font-weight: bold;
        padding: 25px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .stSelectbox {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 8px;
        font-size: 1.2em;
    }
    .result-text {
        color: #1565c0;
        font-size: 2em;
        text-align: center;
        padding: 25px;
        background-color: #e3f2fd;
        border-radius: 10px;
        margin: 25px 0;
        font-weight: bold;
    }
    .category-text {
        color: #424242;
        font-size: 1.5em;
        font-weight: bold;
        margin: 15px 0;
    }
    .privacy-container {
        margin-top: 35px;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #1565c0;
    }
    .privacy-text {
        color: #424242;
        font-size: 1.2em;
        text-align: center;
        line-height: 1.5;
    }
    .developer-credit {
        color: #1565c0;
        font-weight: bold;
        margin-top: 12px;
        font-size: 1.3em;
    }
    .sidebar-title {
        color: #1565c0;
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar-card {
        background-color: #f5f5f5;
        border-left: 4px solid #2e7d32;
        padding: 15px;
        margin: 12px 0;
        border-radius: 5px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .sidebar-text {
        color: #424242;
        font-size: 1.2em;
        margin: 8px 0;
        line-height: 1.5;
    }
    .stNumberInput label {
        font-size: 1.2em !important;
        font-weight: 500 !important;
        color: #1565c0 !important;
    }
    .stNumberInput input {
        font-size: 1.2em !important;
    }
    .stSelectbox label {
        font-size: 1.2em !important;
        font-weight: 500 !important;
        color: #1565c0 !important;
    }

    /* Dropdown/Select box styling */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 2px solid #1565c0;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .stSelectbox > div > div:hover {
        border-color: #2e7d32;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }

    /* Dropdown options styling */
    .stSelectbox > div > div[data-baseweb="select"] > div {
        font-size: 1.2em;
        padding: 8px 12px;
    }

    /* Dropdown arrow styling */
    .stSelectbox [data-testid="stMarkdownContainer"] div[data-baseweb="select"] > div:last-child {
        padding-right: 32px;
    }

    /* Dropdown menu styling */
    div[data-baseweb="popover"] > div {
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 1px solid #e0e0e0;
        max-height: 300px;
        overflow-y: auto;
    }

    /* Dropdown option hover effect */
    div[data-baseweb="popover"] > div > div:hover {
        background-color: #f0f8ff;
    }

    /* Selected option styling */
    div[data-baseweb="popover"] > div > div[aria-selected="true"] {
        background-color: #e3f2fd;
        color: #1565c0;
        font-weight: bold;
    }

    /* Custom scrollbar for dropdown */
    div[data-baseweb="popover"] > div::-webkit-scrollbar {
        width: 8px;
    }

    div[data-baseweb="popover"] > div::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }

    div[data-baseweb="popover"] > div::-webkit-scrollbar-thumb {
        background: #1565c0;
        border-radius: 4px;
    }

    div[data-baseweb="popover"] > div::-webkit-scrollbar-thumb:hover {
        background: #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# Title with icon
st.markdown("<h1 class='main-title'>🔄 Unit Converter</h1>", unsafe_allow_html=True)

# Conversion categories
categories = {
    "Length": {
        "units": ["Meters", "Kilometers", "Miles", "Feet", "Inches", "Centimeters"],
        "icon": "📏"
    },
    "Weight": {
        "units": ["Kilograms", "Grams", "Pounds", "Ounces"],
        "icon": "⚖️"
    },
    "Temperature": {
        "units": ["Celsius", "Fahrenheit", "Kelvin"],
        "icon": "🌡️"
    },
    "Time": {
        "units": ["Seconds", "Minutes", "Hours", "Days"],
        "icon": "⏰"
    }
}

# Category selection
selected_category = st.selectbox(
    "Select Category",
    list(categories.keys()),
    key="category_select"
)

st.markdown(f"<p class='category-text'>{categories[selected_category]['icon']} {selected_category}</p>", unsafe_allow_html=True)

# Input and output unit selection
col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox(
        "From",
        categories[selected_category]["units"],
        key="from_unit_select"
    )
with col2:
    to_unit = st.selectbox(
        "To",
        categories[selected_category]["units"],
        key="to_unit_select"
    )

# Input value
value = st.number_input("Enter Value", value=0.0)

# Conversion functions
def convert_length(value, from_unit, to_unit):
    # Convert everything to meters first
    meters = {
        "Meters": value,
        "Kilometers": value * 1000,
        "Miles": value * 1609.34,
        "Feet": value * 0.3048,
        "Inches": value * 0.0254,
        "Centimeters": value * 0.01
    }
    # Convert from meters to target unit
    conversion = {
        "Meters": meters[from_unit],
        "Kilometers": meters[from_unit] / 1000,
        "Miles": meters[from_unit] / 1609.34,
        "Feet": meters[from_unit] / 0.3048,
        "Inches": meters[from_unit] / 0.0254,
        "Centimeters": meters[from_unit] / 0.01
    }
    return conversion[to_unit]

def convert_weight(value, from_unit, to_unit):
    # Convert everything to grams first
    grams = {
        "Kilograms": value * 1000,
        "Grams": value,
        "Pounds": value * 453.592,
        "Ounces": value * 28.3495
    }
    # Convert from grams to target unit
    conversion = {
        "Kilograms": grams[from_unit] / 1000,
        "Grams": grams[from_unit],
        "Pounds": grams[from_unit] / 453.592,
        "Ounces": grams[from_unit] / 28.3495
    }
    return conversion[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
    return value

def convert_time(value, from_unit, to_unit):
    # Convert everything to seconds first
    seconds = {
        "Seconds": value,
        "Minutes": value * 60,
        "Hours": value * 3600,
        "Days": value * 86400
    }
    # Convert from seconds to target unit
    conversion = {
        "Seconds": seconds[from_unit],
        "Minutes": seconds[from_unit] / 60,
        "Hours": seconds[from_unit] / 3600,
        "Days": seconds[from_unit] / 86400
    }
    return conversion[to_unit]

# Perform conversion
if st.button("Convert"):
    result = 0
    if selected_category == "Length":
        result = convert_length(value, from_unit, to_unit)
    elif selected_category == "Weight":
        result = convert_weight(value, from_unit, to_unit)
    elif selected_category == "Temperature":
        result = convert_temperature(value, from_unit, to_unit)
    elif selected_category == "Time":
        result = convert_time(value, from_unit, to_unit)
    
    st.markdown(f"<div class='result-text'>{value} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)

# Add privacy policy below the convert button
st.markdown("""
<div class='privacy-container'>
    <p class='privacy-text'>🔒 Privacy Notice: This unit converter respects your privacy. No personal data is collected or stored.</p>
    <p class='privacy-text developer-credit'>© 2024 Developed by Zakia Baig</p>
</div>
""", unsafe_allow_html=True)

# Update sidebar to remove the developer info
with st.sidebar:
    st.markdown("""
    <div class='sidebar-title'>📌 Quick Guide</div>

    <div class='sidebar-card'>
        <p class='sidebar-text'>1️⃣ Select conversion category</p>
        <p class='sidebar-text'>2️⃣ Choose units (from/to)</p>
        <p class='sidebar-text'>3️⃣ Enter value</p>
        <p class='sidebar-text'>4️⃣ Click 'Convert'</p>
    </div>

    <div class='sidebar-card'>
        <p class='sidebar-text'><b>Available Categories:</b></p>
        <p class='sidebar-text'>📏 Length</p>
        <p class='sidebar-text'>⚖️ Weight</p>
        <p class='sidebar-text'>🌡️ Temperature</p>
        <p class='sidebar-text'>⏰ Time</p>
    </div>
    """, unsafe_allow_html=True) 