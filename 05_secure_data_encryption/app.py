import streamlit as st
import hashlib
import json
import time
from cryptography.fernet import Fernet
import base64

# Initialize session state variable if they don't exist
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'
if 'last_attempt_time' not in st.session_state:
    st.session_state.last_attempt_time = 0

# function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# function to generate a key from passkey(for encryption)
def generate_key_from_passkey(passkey):
    # use the passkey to create a consistent key
    hashed = hashlib.sha256(passkey.encode()).digest()
    # ensure it's valid for Fernet(32 urlsafe base64-encoded bytes)
    return base64.urlsafe_b64encode(hashed[:32])

# function to encrypt data
def encrypt_data(text, passkey):
    key = generate_key_from_passkey(passkey)
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()

# function to decrypt data
def decrypt_data(encrypted_text, passkey, data_id):
    try:
        # Check if the passkey hash matches the stored hash for the given data_id
        hashed_passkey = hash_passkey(passkey)
        if (
            data_id in st.session_state.stored_data and
            st.session_state.stored_data[data_id]['passkey_hash'] == hashed_passkey
        ):
            # If passkey matched, decrypt data
            key = generate_key_from_passkey(passkey)
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_text.encode()).decode()
            st.session_state.failed_attempts = 0  # Reset failed attempts
            return decrypted
        else:
            # Increment failed attempts if passkey is incorrect
            st.session_state.failed_attempts += 1
            st.session_state.last_attempt_time = time.time()
            return None
    except Exception as e:
        # Catch all other decryption errors
        st.session_state.failed_attempts += 1
        st.session_state.last_attempt_time = time.time()
        return None

# function to generate a unique ID for data
def generate_data_id():
    import uuid
    return str(uuid.uuid4())

# function to reset failed attempts
def reset_failed_attempts():
    st.session_state.failed_attempts = 0

# function to change page
def change_page(page):
    st.session_state.current_page = page

# streamlit ui
st.title("Secure Data Storage System")

# Navigation
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu, index=menu.index(st.session_state.current_page))

# update current page based on selection
st.session_state.current_page = choice

# check if too many failed attempts
if st.session_state.failed_attempts >= 3:
    # force redirect to login page
    st.session_state.current_page = "Login"
    st.warning("Too many failed attempts. Please login again.")

# display current page
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
    user_data = st.text_area("Enter Data: ")
    passkey = st.text_input("Enter Passkey: ", type="password")
    confirm_passkey = st.text_input("Confirm Passkey: ", type="password")  # ✅ FIXED

    if st.button("Enrypt & Save"):
        if user_data and passkey and confirm_passkey:
            if passkey != confirm_passkey:
                st.error("Passkeys do not match!")
            else:
                # generate a unique id for the data
                data_id = generate_data_id()

                # hash the passkey
                hashed_passkey = hash_passkey(passkey)

                # encrypt the text
                encrypted_text = encrypt_data(user_data, passkey)

                # store in the required format
                st.session_state.stored_data[data_id] = {
                    'encrypted_text': encrypted_text,
                    'passkey_hash': hashed_passkey
                }

                st.success("Data stored successfully!")

                # display the data id for retrival
                st.code(data_id, language='text')
                st.info("Save this ID to retrieve your data later.")

        else:
            st.error("All the feilds are required!")

elif st.session_state.current_page == "Retrieve Data":
    st.subheader("Retrieve Existing Data")

    # show attempt remaining
    attempts_remaining = st.session_state.failed_attempts
    st.info(f"Failed attempts: {attempts_remaining}")

    data_id = st.text_input("Enter Data ID: ")
    passkey = st.text_input("Enter Passkey: ", type="password")

    if st.button("Decrypt & Retrieve"):
        if data_id and passkey:
            # Check if the data ID exists in stored data
            if data_id in st.session_state.stored_data:
                # Decrypt the data using the provided passkey
                encrypted_text = st.session_state.stored_data[data_id]['encrypted_text']
                decrypted_text = decrypt_data(encrypted_text, passkey, data_id)

                if decrypted_text:  # ✅ FIXED
                    st.success("Data retrieved successfully!")
                    st.markdown("### Your decrypted data:")
                    st.code(decrypted_text, language='text')
                else:
                    st.error(f"Incorrect passkey or data ID. Attempts remaining: {3 - st.session_state.failed_attempts}")
            else:
                st.error("Data Id not found!")

            # check if too many failed attempts after this attempt
            if st.session_state.failed_attempts >= 3:
                st.warning("Too many failed attempts. Please login again.")
                st.session_state.current_page = "Login"
                st.rerun()
        else:
            st.error("Both fields are required!")

elif st.session_state.current_page == "Login":
    st.subheader("Reauthorization Required")

    # add a simple timeout mechanism
    if time.time() - st.session_state.last_attempt_time < 10 and st.session_state.failed_attempts >=3:
        remaining_time = int(10 - (time.time() - st.session_state.last_attempt_time))
        st.warning(f"Please wait {remaining_time}for a while before trying again.")
    else:
        login_pass = st.text_input("Enter Master Password:", type="password")

        if st.button("Login"):
            if login_pass == "admin123":
                reset_failed_attempts()
                st.success("Reauthorized successfully!")
                st.session_state.current_page = "Home"
                st.rerun() #update from experimental_rerun()
            else:
                st.error("Incorrect password!")
                
# Add a footer
st.markdown("---")
st.markdown("Secure Data Storage System")