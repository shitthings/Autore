import streamlit as st
import requests
import random
import string
import csv
import threading

# Function to generate random URL and check its status
def generate_random_url():
    base_url = "https://autoreg.site/status/"
    random_string = ''.join(random.choices(string.hexdigits, k=32))
    url = base_url + random_string
    response = requests.get(url)
    if response.status_code == 200:
        return url
    else:
        return None

# Streamlit app
st.title("Random URL Generator")

# Create a lock to synchronize access to shared data
lock = threading.Lock()

# Lists to store successful and failed attempts
success_attempts = []
failed_attempts = []

# Function to run in a separate thread
def background_thread():
    global success_attempts
    global failed_attempts

    while not stop_thread:
        url = generate_random_url()
        
        with lock:
            if url:
                success_attempts.append(url)
            else:
                failed_attempts.append(url)

# Start button and stop button
start_button = st.button("Start Generating")
stop_button = st.button("Stop Generating")

if start_button and not stop_button:
    stop_thread = False
    thread = threading.Thread(target=background_thread)
    thread.start()

if stop_button:
    stop_thread = True

# Download successful attempts as CSV
if st.button("Download Successful Attempts CSV"):
    if success_attempts:
        with st.spinner("Generating CSV..."):
            with open('successful_attempts.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["URL"])
                writer.writerows([[url] for url in success_attempts])
        st.success("CSV file generated successfully!")
        st.markdown(f"Download [successful_attempts.csv](successful_attempts.csv)")

# Display statistics
st.header("Statistics")
st.text(f"Total Attempts: {len(success_attempts) + len(failed_attempts)}")
st.text(f"Successful Attempts: {len(success_attempts)}")
st.text(f"Failed Attempts: {len(failed_attempts)}")
