import streamlit as st
import requests
import random
import string
import csv

# Function to generate a random URL and check its status
def generate_random_url():
    base_url = "https://autoreg.site/status/"
    random_string = ''.join(random.choices(string.hexdigits, k=32))
    url = base_url + random_string
    response = requests.get(url)
    return url, response.status_code == 200

# Streamlit app
st.title("Random URL Generator")

attempts_count = 0
successful_urls = []

if st.button("Start Generating"):
    while True:
        attempts_count += 1
        url, is_successful = generate_random_url()
        st.text(f"Attempt {attempts_count}: {url}")

        if is_successful:
            successful_urls.append(url)
        else:
            break

# Display download button for successful URLs as CSV
if successful_urls:
    st.header("Successful URLs")
    st.write(successful_urls)
    
    if st.button("Download Successful URLs as CSV"):
        with st.spinner("Generating CSV..."):
            with open('successful_urls.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["URL"])
                writer.writerows([[url] for url in successful_urls])
        st.success("CSV file generated successfully!")
        st.markdown(f"Download [successful_urls.csv](successful_urls.csv)")

st.header("Statistics")
st.text(f"Total Successful Attempts: {attempts_count}")
