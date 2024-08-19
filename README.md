## Si Skrap

A simple program to get all data subjects and schedules of _siakad UIN Malang_ (Academic System of UIN Malang) to easily read data tables and convert it into excel file using data scrapper and python <br>

## How to use?
1. Clone this repository

2. Install Requirements <br>
    Run command
    ```bash
    pip install -r requirement.txt
    ```

3. Input your user credentials <br>
    WARNING! DON'T SHOW YOUR CREDENTIAL USER PUBLICLY!!! <br>

    You can see this payload settings in `.env.example`, and don't forget to rename it into `.env`
    ```env
    USER= # Your ID Number of Siakad UIN Malang
    PASS= # Your Password of Siakad UIN Malang
    ```

4. Run program
    ```bash
    python main.py
    ```

5. Input the captcha <br>
    After running the program, The image will appear and you need to solve problem and you need to input the solve in terminal

6. Name your excel files <br>
    Name your file whatever you likes

7. Done! <br>
    The excel files should be appear on this folder