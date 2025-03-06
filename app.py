import streamlit as st
import requests

def get_exchange_rate(base_currency, target_currency):
    api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data['rates'].get(target_currency, None)
    return None

def convert_units(value, from_unit, to_unit, conversion_type):
    conversion_factors = {
        "Length": {"Meter": 1, "Kilometer": 0.001, "Mile": 0.000621371, "Foot": 3.28084},
        "Weight": {"Gram": 1, "Kilogram": 0.001, "Pound": 0.00220462, "Ounce": 0.035274},
        "Temperature": {"Celsius": lambda x: x, "Fahrenheit": lambda x: x * 9/5 + 32, "Kelvin": lambda x: x + 273.15},
        "Time": {"Second": 1, "Minute": 1/60, "Hour": 1/3600},
        "Speed": {"Meter/sec": 1, "Kilometer/hour": 3.6, "Mile/hour": 2.23694}
    }
    
    if conversion_type == "Temperature":
        return round(conversion_factors[conversion_type][to_unit](value), 2)
    else:
        return round(value * conversion_factors[conversion_type][to_unit] / conversion_factors[conversion_type][from_unit], 2)

def main():
    st.set_page_config(page_title="Google Converter Clone", page_icon="💱", layout="centered")
    
    custom_css = """
    <style>
        @import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');
        body { background-color:rgb(9, 10, 10); color: #cbd5e0; }
        .stApp { background-color:rgb(15, 15, 15); }
        .stButton>button { background-color: #4a5568; color: #edf2f7; padding: 10px; border-radius: 5px; }
        .stButton>button:hover { background-color: #2d3748; }
        .stSelectbox>div>div { background-color: #2d3748 !important; color: #edf2f7 !important; }
        .stNumberInput>div>div { background-color: #2d3748 !important; color: #edf2f7 !important; }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    st.title("🌎 Google Converter Clone")
    st.markdown("### Convert anything in real-time!")
    
    conversion_types = ["Currency", "Length", "Weight", "Temperature", "Time", "Speed"]
    conversion_type = st.selectbox("Select Conversion Type", conversion_types)
    
    if conversion_type == "Currency":
        currencies = ["USD", "EUR", "GBP", "PKR", "INR", "AUD", "CAD", "CNY", "JPY", "SAR"]
        base_currency = st.selectbox("From Currency", currencies, index=currencies.index("USD"))
        target_currency = st.selectbox("To Currency", currencies, index=currencies.index("PKR"))
    else:
        units = {
            "Length": ["Meter", "Kilometer", "Mile", "Foot"],
            "Weight": ["Gram", "Kilogram", "Pound", "Ounce"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Time": ["Second", "Minute", "Hour"],
            "Speed": ["Meter/sec", "Kilometer/hour", "Mile/hour"]
        }
        base_currency = st.selectbox("From Unit", units[conversion_type])
        target_currency = st.selectbox("To Unit", units[conversion_type])
    
    amount = st.number_input("Enter Amount", min_value=0.0, value=1.0, step=1.0)
    
    if st.button("Convert"): 
        if conversion_type == "Currency":
            rate = get_exchange_rate(base_currency, target_currency)
            if rate:
                converted_amount = round(amount * rate, 2)
                st.success(f"{amount} {base_currency} = {converted_amount} {target_currency}")
            else:
                st.error("Error fetching exchange rates. Please try again later.")
        else:
            converted_amount = convert_units(amount, base_currency, target_currency, conversion_type)
            st.success(f"{amount} {base_currency} = {converted_amount} {target_currency}")
    
    st.markdown("---")
    st.caption("💡 Powered by ExchangeRate-API & Custom Unit Conversions")

if __name__ == "__main__":
    main()
