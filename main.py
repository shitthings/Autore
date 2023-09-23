import streamlit as st
import requests
import random
import string
import csv
from io import BytesIO

# Streamlit UI
st.title("Random URL Checker")

# Function to check URL
def check_url(url):
    response = requests.get(url)
    return response.status_code == 200, response.content

# Main Streamlit code
if st.button("Start Checking"):
    base_url = "https://autoreg.site/status/"
    success_attempts = []
    failed_attempts = []
    try:
        while True:
            random_string = ''.join(random.choices(string.hexdigits, k=32))
            url = base_url + random_string
            is_successful, response_content = check_url(url)

            if is_successful:
                success_attempts.append(url)
                st.write("Successfully accessed URL:", url)
                st.write("Response content:", response_content)
                print("Successfully accessed URL:", url)  # Print to console
            else:
                failed_attempts.append(url)

    except KeyboardInterrupt:
        pass  # Exit loop gracefully on user interrupt

    st.write("Successful attempts:", success_attempts)
    st.write("Failed attempts:", failed_attempts)

    # Store successful attempts in a CSV file
    if len(success_attempts) > 0:
        st.write("Storing successful attempts in a CSV file...")
        output_csv = BytesIO()
        csv_writer = csv.writer(output_csv)
        csv_writer.writerow(["URL"])
        csv_writer.writerows([[url] for url in success_attempts])

        st.download_button(
            "Download Successful Attempts CSV",
            output_csv.getvalue(),
            key="successful_attempts_csv",
            file_name="successful_attempts.csv",
        )
