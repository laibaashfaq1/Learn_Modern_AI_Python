import streamlit as st # streamlit is a library for creating web apps

# function to convert units
def convert_units(value, unit_from, unit_to):
    conversions = {

        # Length
        "meters_kilometers": 0.001, # 1 meter = 0.001 kilometers
        "kilometers_meters": 1000, # 1 kilometer = 1000 meters
        "meters_feet": 3.28084, # 1 meter = 3.28084 feet
        "feet_meters": 0.3048, # 1 foot = 0.3048 meters
        "meters_inches": 39.3701, # 1 meter = 39.3701 inches
        "inches_meters": 0.0254, # 1 inch = 0.0254 meters
        "miles_kilometers": 1.60934, # 1 mile = 1.60934 kilometers
        "kilometers_miles": 0.621371, # 1 kilometer = 0.621371 miles,


        # Weight
        "grams_kilograms": 0.001,  # 1 gram = 0.001 kilograms
        "kilograms_grams": 1000, # 1 kilogram = 1000 grams
        "grams_pounds": 0.00220462, # 1 gram = 0.00220462 pounds
        "pounds_grams": 453.592, # 1 pound = 453.592 grams
        "kilograms_pounds": 2.20462, # 1 kilogram = 2.20462 pounds
        "pounds_kilograms": 0.453592, # 1 pound = 0.453592 kilograms


        # Time
        "hours_minutes": 60, # 1 hour = 60 minutes
        "minutes_hours": 1/60, # 1 minute = 1/60 hours
        "hours_seconds": 3600, # 1 hour = 3600 seconds
        "seconds_hours": 1/3600, # 1 second = 1/3600 hours
        "minutes_seconds": 60, # 1 minute = 60 seconds
        "seconds_minutes": 1/60, # 1 second = 1/60 minutes
        "hours_days": 1/24, # 1 hour = 1/24 days
        "days_hours": 24, # 1 day = 24 hours


        # Speed
        "meters per second_kilometers per hour": 3.6, # 1 meter per second = 3.6 kilometers per hour
        "kilometers per hour_meters per second": 1/3.6, # 1 kilometer per hour = 1/3.6 meters per second
        "miles per hour_kilometers per hour": 1.60934, # 1 mile per hour = 1.60934 kilometers per hour
        "kilometers per hour_miles per hour": 0.621371, # 1 kilometer per hour = 0.621371 miles per hour
    }


    # Temperature conversion
    if unit_from == "Celsius" and unit_to == "Fahrenheit":
        return round((value * 9/5) + 32, 2)
    elif unit_from == "Fahrenheit" and unit_to == "Celsius": # we use elif for writting multi
        return round((value - 32) * 5/9, 2)
    elif unit_from == "Celsius" and unit_to == "Kelvin":
        return round(value + 273.15, 2)
    elif unit_from == "Kelvin" and unit_to == "Celsius":
        return round(value - 273.15, 2)
    elif unit_from == "Fahrenheit" and unit_to == "Kelvin":
        return round((value - 32) * 5/9 + 273.15, 2)
    elif unit_from == "Kelvin" and unit_to == "Fahrenheit":
        return round((value - 273.15) * 9/5 + 32, 2)


# Key for the conversion
    key = f"{unit_from}_{unit_to}"
    return round(value * conversions[key], 4) if key in conversions else "Not a valid conversion"


# Title of the app
st.title("🔄 Unit Converter")


# Dropdown to select the category
category = st.selectbox("Select a category:", ["Length", "Weight", "Temperature", "Time", "Speed"])


# Define unit options based on category
unit_options = {
    "Length": ["meters", "kilometers", "feet", "inches", "miles"],
    "Weight": ["grams", "kilograms", "pounds"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Time": ["seconds", "minutes", "hours", "days"],
    "Speed": ["meters per second", "kilometers per hour", "miles per hour"],
}


# User input
value = st.number_input("Enter value:", min_value=0.0, step=0.1)
unit_from = st.selectbox("Convert from:", unit_options[category])
unit_to = st.selectbox("Convert to:", unit_options[category])


# Convert button
if st.button("Convert"):
    result = convert_units(value, unit_from, unit_to)
    st.success(f"Converted Value: {result} {unit_to}")
