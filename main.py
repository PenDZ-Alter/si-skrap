from src.scrapper import Scrapper

if __name__ == '__main__' :
    # Create a Scrapper instance
    scrapper = Scrapper()
    scrapper.load_login()
    scrapper.load_csrf_token()
    scrapper.captcha_resolver()
    scrapper.post_data()
    scrapper.fetch_data()
    scrapper.parse_file()