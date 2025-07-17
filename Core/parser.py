from SessionManager import FacebookSessionManager

def main():
    EMAIL = "ibkinside@gmail.com"
    PASSWORD = "justicemen"
    fb = FacebookSessionManager(EMAIL, PASSWORD)
    context, page = fb.load_session()
    if page:
        html = page.content()
        # Example: print the HTML or parse it with BeautifulSoup
        print(html)
        # from bs4 import BeautifulSoup
        # soup = BeautifulSoup(html, "html.parser")
        # ... your parsing logic here ...
        fb.browser.close()
    else:
        print("Failed to load session or page.")

if __name__ == "__main__":
    main()