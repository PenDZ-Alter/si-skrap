import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Define the login URL and the URL of the page you want to scrape
login_url = 'https://siakad.uin-malang.ac.id/cek_login.php'
data_url = 'https://siakad.uin-malang.ac.id/2.0/uin-PnjdwlnPmsrn'  # Adjust this URL to the correct one for your data page

# Define your login credentials
payload = {
    'username': os.getenv("USER"),
    'password': os.getenv("PASS"),
    'captcha_entered': 'your_captcha_solution'
}

# Start a session
session = requests.Session()

# Access the login page to get any necessary tokens (e.g., CSRF token)
login_page_response = session.get(login_url)
login_soup = BeautifulSoup(login_page_response.content, 'html.parser')

# Extract the CSRF token or other required fields if present (example with a hidden input field)
csrf_token = login_soup.find('input', {'name': 'csrf_token'})
if csrf_token:
    payload['csrf_token'] = csrf_token['value']

# If there's a captcha, you may need to handle it manually
captcha_image_url = 'https://siakad.uin-malang.ac.id/captcha.php'
captcha_response = session.get(captcha_image_url)

# Save the captcha image locally for manual solving
with open('captcha.jpg', 'wb') as f:
    f.write(captcha_response.content)

# Prompt user to enter the captcha solution
captcha_solution = input('Please enter the captcha solution: ')
payload['captcha_entered'] = captcha_solution

# Perform the login with headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': login_url
}

login_response = session.post(login_url, data=payload, headers=headers)

# Check if login was successful by inspecting the response URL or content
if 'logout' in login_response.text.lower():
    print("Login successful!")

    # Now access the data page
    data_response = session.get(data_url)

    # Check if the data page was accessed successfully
    if data_response.status_code == 200:
        print("Data page accessed successfully!")

        # Parse the HTML content of the data response
        soup = BeautifulSoup(data_response.content, 'html.parser')

        # Locate the div with id "nav-matakuliah"
        matakuliah_div = soup.find('div', {'id': 'nav-matakuliah'})

        # Ensure the div was found
        if matakuliah_div:
            print("Found the 'nav-matakuliah' div!")

            # Locate the table within the div
            table = matakuliah_div.find('table')

            # Ensure the table was found
            if table:
                print("Found the table within 'nav-matakuliah' div!")

                # Extract table rows
                rows = table.find_all('tr')
                
                i = 0

                # Loop through rows and extract data
                for row in rows:
                    columns = row.find_all('td')
                    data = [column.text.strip() for column in columns]
                    i = i + 1
                    print(data)
                    
                print("Total data = ", i)
            else:
                print("Table not found within 'nav-matakuliah' div.")
        else:
            print("Div with id 'nav-matakuliah' not found.")
    else:
        print("Failed to access data page. Status code:", data_response.status_code)
else:
    print("Login failed. Please check your credentials and try again.")