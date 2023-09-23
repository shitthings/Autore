import streamlit as st
import requests
import random
import string
import csv

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

if st.button("Start Generating"):
    success_attempts = []
    failed_attempts = []
    attempts_count = 0

    while True:
        url = generate_random_url()
        attempts_count += 1
        st.text(f"Attempt {attempts_count}: {url}")

        if url:
            success_attempts.append(url)
        else:
            failed_attempts.append(url)

        # Check if the user wants to stop
        if not st.button("Stop"):
            break

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
st.text(f"Total Attempts: {attempts_count}")
st.text(f"Successful Attempts: {len(success_attempts)}")
st.text(f"Failed Attempts: {len(failed_attempts)}")
