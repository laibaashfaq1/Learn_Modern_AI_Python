# Streamlit — Web app banane ke liye use hota hai (UI/UX ke liye)
import streamlit as st

# hashlib — Passkey ko securely hash (encrypt) karne ke liye
import hashlib

# json — Agar aapko data ko save/load karna ho to use hota hai (filhal optional hai)
import json

# time — Time track karne ke liye (e.g. failed login attempts ke darmiyan wait)
import time

# cryptography.fernet — Data encryption aur decryption ke liye (very secure method)
from cryptography.fernet import Fernet

# base64 — Cryptographic key ko encode/decode karne ke liye (Fernet ke liye zaroori)
import base64

# Initialize session state variable if they don't exist
# Yeh ensure karta hai ke session ke variables reset na hon jab tak app refresh na ho
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0  # Failed login attempts ka counter
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}  # Stored data ki dictionary
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'  # Default page
if 'last_attempt_time' not in st.session_state:
    st.session_state.last_attempt_time = 0  # Last failed attempt ka timestamp

# Function to hash passkey
# Passkey ko hash (encrypt) karne ke liye
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to generate a key from passkey (for encryption)
# Passkey se ek unique key generate karte hain jo encrypted data ko safe rakhe
def generate_key_from_passkey(passkey):
    # Passkey ko hash karte hain, phir uss hash ko use karke ek key banate hain
    hashed = hashlib.sha256(passkey.encode()).digest()
    # Ensure it's valid for Fernet (32 URL-safe base64-encoded bytes)
    return base64.urlsafe_b64encode(hashed[:32])

# Function to encrypt data
# Data ko encrypt karte hain taake secure rahe
def encrypt_data(text, passkey):
    key = generate_key_from_passkey(passkey)  # Passkey se key generate
    cipher = Fernet(key)  # Fernet cipher banate hain
    return cipher.encrypt(text.encode()).decode()  # Data ko encrypt karte hain

# Function to decrypt data
# Data ko decrypt karte hain jab passkey sahi ho
def decrypt_data(encrypted_text, passkey, data_id):
    try:
        # Check if the passkey hash matches the stored hash for the given data_id
        # Yeh check karta hai ke passkey sahi hai ya nahi
        hashed_passkey = hash_passkey(passkey)
        if (
            data_id in st.session_state.stored_data and
            st.session_state.stored_data[data_id]['passkey_hash'] == hashed_passkey
        ):
            # If passkey matched, decrypt data
            # Agar passkey match ho gayi to data ko decrypt karte hain
            key = generate_key_from_passkey(passkey)
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_text.encode()).decode()
            st.session_state.failed_attempts = 0  # Reset failed attempts
            return decrypted
        else:
            # Increment failed attempts if passkey is incorrect
            # Agar passkey galat ho to failed attempts ko increase karte hain
            st.session_state.failed_attempts += 1
            st.session_state.last_attempt_time = time.time()
            return None
    except Exception as e:
        # Catch all other decryption errors
        # Agar koi aur error ho to bhi failed attempts ko increase karte hain
        st.session_state.failed_attempts += 1
        st.session_state.last_attempt_time = time.time()
        return None

# Function to generate a unique ID for data
# Data ke liye ek unique ID banate hain, jise baad mein retrieve kiya jaa sakta hai
def generate_data_id():
    import uuid  # UUID module ko import karte hain unique ID banane ke liye
    return str(uuid.uuid4())

# Function to reset failed attempts
# Jab passkey sahi ho jaye to failed attempts ko reset karte hain
def reset_failed_attempts():
    st.session_state.failed_attempts = 0

# Function to change page
# Page switch karne ke liye, jo selected page hai usko update karte hain
def change_page(page):
    st.session_state.current_page = page

# Streamlit UI
# Title of the app
st.title("Secure Data Storage System")

# Navigation
# Sidebar mein different pages ka selection dene ke liye
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu, index=menu.index(st.session_state.current_page))

# Update current page based on selection
# Jo page user select kare, usko session state mein store karte hain
st.session_state.current_page = choice

# Check if too many failed attempts
# Agar user ne 3 bar wrong attempts kiye hain to force login page pe redirect karte hain
if st.session_state.failed_attempts >= 3:
    # Force redirect to login page
    st.session_state.current_page = "Login"
    st.warning("Too many failed attempts. Please login again.")

# Display current page content
# Ab jo bhi current page selected hai, uske hisaab se UI dikhai dega
if st.session_state.current_page == "Home":
    st.subheader("Welcome to the Secure Data Storage System")
    st.write("Use the sidebar to navigate through the app.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Store New Data", use_container_width=True):
            change_page("Store Data")
    with col2:
        if st.button("Retrieve Existing Data", use_container_width=True):
            change_page("Retrieve Data")

    # Display stored data count
    st.info(f"Total stored data items: {len(st.session_state.stored_data)} encrypted items.")

elif st.session_state.current_page == "Store Data":
    st.subheader("Store New Data")
    user_data = st.text_area("Enter Data: ")  # User se data lene ke liye text area
    passkey = st.text_input("Enter Passkey: ", type="password")  # Passkey lene ke liye input field
    confirm_passkey = st.text_input("Confirm Passkey: ", type="password")  # Confirm passkey

    if st.button("Encrypt & Save"):  # Button press hone pe data store karte hain
        if user_data and passkey and confirm_passkey:
            if passkey != confirm_passkey:
                st.error("Passkeys do not match!")
            else:
                # Generate unique data ID
                data_id = generate_data_id()

                # Hash the passkey
                hashed_passkey = hash_passkey(passkey)

                # Encrypt the data
                encrypted_text = encrypt_data(user_data, passkey)

                # Store the encrypted data
                st.session_state.stored_data[data_id] = {
                    'encrypted_text': encrypted_text,
                    'passkey_hash': hashed_passkey
                }

                st.success("Data stored successfully!")

                # Display the data ID for retrieval
                st.code(data_id, language='text')
                st.info("Save this ID to retrieve your data later.")

        else:
            st.error("All fields are required!")

elif st.session_state.current_page == "Retrieve Data":
    st.subheader("Retrieve Existing Data")

    # Show attempt remaining
    attempts_remaining = st.session_state.failed_attempts
    st.info(f"Failed attempts: {attempts_remaining}")

    data_id = st.text_input("Enter Data ID: ")  # Data ID enter karne ke liye
    passkey = st.text_input("Enter Passkey: ", type="password")  # Passkey enter karne ke liye

    if st.button("Decrypt & Retrieve"):  # Button press hone par data decrypt karte hain
        if data_id and passkey:
            # Check if the data ID exists in stored data
            if data_id in st.session_state.stored_data:
                # Decrypt the data using the provided passkey
                encrypted_text = st.session_state.stored_data[data_id]['encrypted_text']
                decrypted_text = decrypt_data(encrypted_text, passkey, data_id)

                if decrypted_text:
                    st.success("Data retrieved successfully!")
                    st.markdown("### Your decrypted data:")
                    st.code(decrypted_text, language='text')
                else:
                    st.error(f"Incorrect passkey or data ID. Attempts remaining: {3 - st.session_state.failed_attempts}")
            else:
                st.error("Data ID not found!")

            # Check if too many failed attempts after this attempt
            if st.session_state.failed_attempts >= 3:
                st.warning("Too many failed attempts. Please login again.")
                st.session_state.current_page = "Login"
                st.rerun()
        else:
            st.error("Both fields are required!")

elif st.session_state.current_page == "Login":
    st.subheader("Reauthorization Required")

    # Add a simple timeout mechanism
    if time.time() - st.session_state.last_attempt_time < 10 and st.session_state.failed_attempts >= 3:
        remaining_time = int(10 - (time.time() - st.session_state.last_attempt_time))
        st.warning(f"Please wait {remaining_time} seconds before trying again.")
    else:
        login_pass = st.text_input("Enter Master Password:", type="password")

        if st.button("Login"):
            if login_pass == "admin123":  # Master password check
                reset_failed_attempts()
                st.success("Reauthorized successfully!")
                st.session_state.current_page = "Home"
                st.rerun()  # Update from experimental_rerun()
            else:
                st.error("Incorrect password!")

# Add a footer
st.markdown("---")
st.markdown("Secure Data Storage System")
