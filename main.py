from src.scrapper import Scrapper

global sy

if __name__ == '__main__' :
    # Create a Scrapper instance
    scrapper = Scrapper()
    scrapper.load_login()
    scrapper.load_csrf_token()
    scrapper.captcha_resolver()
    scrapper.post_data()
    
    while True : 
        print("\nType of getting academic system information : ")
        print("[1] Subjects")
        print("[2] Grades")
        select = int(input("Please Select the type : "))
        
        if select == 2 : 
            print("Select the school year : ")
            print("[1] 2022/2023")
            print("[2] 2023/2024")
            print("[3] 2024/2025")
            sy_select = int(input("Please select school year : "))
            
            match sy_select : 
                case 1 : 
                    sy = "2223"
                case 2 : 
                    sy = "2324"
                case 3 : 
                    sy = "2425"
                case _ : 
                    sy = None
            
            print("\nSelect semester : ")
            print("[1] Odd")
            print("[2] Even")
            smt_select = input("Please select semester : ")
            
            scrapper.fetch_grades_data(ta = sy, smt = smt_select)
            scrapper.parse_grades_file()
            break
        elif select == 1 : 
            scrapper.fetch_subjects_data()
            scrapper.parse_subjects_file()
            break
        else : 
            print("Invalid Type!!")
    