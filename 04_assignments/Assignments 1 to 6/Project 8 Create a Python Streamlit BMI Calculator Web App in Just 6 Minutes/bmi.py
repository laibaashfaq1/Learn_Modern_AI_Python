# A BMI Calculator in Python is a simple program that calculates a person’s 
# Body Mass Index (BMI) based on their weight and height. 
# BMI is a commonly used indicator to classify whether a person is underweight, normal, overweight, or obese.

import streamlit as st

# App Title and Description
st.title("🧮 BMI Calculator")
st.write("Enter your height and weight to calculate your Body Mass Index (BMI).")

# Input for Height and Weight
height = st.number_input("Height (in meters)", min_value=0.5, max_value=3.0, value=1.75)
weight = st.number_input("Weight (in kilograms)", min_value=10, max_value=200, value=70)

# Button to trigger BMI calculation
if st.button("Calculate BMI"):
    if height > 0 and weight > 0:
        bmi = weight / (height ** 2)
        st.success(f"✅ Your BMI is: {bmi:.2f}")

        # Display health message based on BMI range
        if bmi < 18.5:
            st.warning("You are underweight.")
        elif bmi < 24.9:
            st.success("You have a normal weight.")
        elif bmi < 29.9:
            st.warning("You are overweight.")
        else:
            st.error("You are obese.")
    else:
        st.error("Please enter valid height and weight values.")
