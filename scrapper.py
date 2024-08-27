import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
from data import Data

class Scrapper :    
    def __init__(self) :
        self.data = Data()
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': self.data.get_login()
        }
        
    def load_login(self) :
        login_response = self.session.get(self.data.get_login())
        self.login_parser = BeautifulSoup(login_response.content, 'html.parser')
        if self.login_parser is None : 
            print("Failed to parsing data!!")
            return False
        else : 
            return True
        
    def load_csrf_token(self) :
        csrf_token = self.login_parser.find('input', {'name': 'csrf_token'})
        if csrf_token:
            self.data.set_csrf_token_payload(csrf_token['value'])
            return True
        else :
            print("No CSRF token found!")
            return False
    
    def captcha_resolver(self) : 
        captcha_response = self.session.get(self.data.get_captcha())
        
        with open('captcha.jpg', 'wb') as f:
            f.write(captcha_response.content)
        
        os.system("captcha.jpg")
        captcha_solve = input('Please enter the captcha solution: ')
        self.data.set_captcha_payload(captcha_solve)
    
    def post_data(self) :
        self.login_response = self.session.post(self.data.get_login(), data=self.data.get_payload(), headers=self.headers)
        
        if 'logout' in self.login_response.text.lower() :
            return True
        else :
            print("Login Failed!")
            return False
        
    def fetch_data(self) :
        if self.post_data() :
            print("Login Successful!")
            data_response = self.session.get(self.data.get_url())
            
            if data_response.status_code == 200 :
                return data_response
            else :
                print("Failed to access data page!")
                print(data_response)
                return 0
        else : 
            print("Failed to fetch data!!")
            return 0
            
    def parse_file(self) : 
        if self.fetch_data() == 0 :
            print("Can't get fetched data!")
            return 0
        else : 
            print("Data page accessed successfully!")
            # Parse the HTML content of the data response
            soup = BeautifulSoup(self.fetch_data().content, 'html.parser')
            
            table_headers = None

            print("\nType to parse data : ")
            print("[1] KRS")
            print("[2] Schedule")
            ch = int(input("Please select the type : "))
            
            parent_div = None
            
            if (ch == 1) :
                parent_div = soup.find('div', {'id': 'nav-matakuliah'})    
                table_headers = [ "", "Hari", "Jam", "Kode Matkul", "Mata Kuliah", "Dosen", "Asisten Dosen", "Ruang", "Kelas", "Tatap Muka", "Angkatan", "Kapasitas" ]  
            elif (ch == 2) :
                parent_div = soup.find('div', {'id': 'nav-jadwalku'})
                table_headers = [ "", "Hari", "Jam", "Kelas", "Ruang", "Kode Matkul", "Mata Kuliah", "SKS", "Dosen", "Tatap Muka", "Jurusan", "Kapasitas" ]
            else : 
                print("Type not found!!")
                return 0

            # Ensure the div was found
            if parent_div:
                print("Found the parent div!")

                # Locate the table within the div
                table = parent_div.find('table')

                # Ensure the table was found
                if table:
                    print("Found the table within parent div!")
                    
                    file_name = input("Please enter file name : ")
                    file_name = file_name + ".xlsx"

                    # Extract table rows
                    rows = table.find_all('tr')
                    
                    i = 0
                    
                    table_data = []
                    
                    # Loop through rows and extract data
                    for row in rows:
                        columns = row.find_all('td')
                        data = [column.text.strip() for column in columns]
                        i = i + 1
                        table_data.append(data)
                        
                    print("Total data =", i)
                    
                    df = pd.DataFrame(table_data)
                    df.to_excel(file_name, index=False, header=table_headers)
                    print(f"Data saved to {file_name}!")
                    return 1
                else:
                    print("Table not found within parent div.")
                    return 0
            else:
                print("Parent Div with id not found.")
                return 0