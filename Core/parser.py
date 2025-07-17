from SessionManager import FacebookSessionManager
import time

def main():
    # No credentials needed; user will sign in manually if required
    import os
    home = os.path.expanduser("~")
    fb_auth_dir = os.path.join(home, "FBAuth")
    auth_path = os.path.join(fb_auth_dir, "auth.json")
    fb = FacebookSessionManager(email=None, password=None)

    if not os.path.exists(auth_path):
        print(f"No session file found at {auth_path}. You must log in manually.")
        fb.login(stay_open=True)

    try:
        context, page = fb.load_session()
        time.sleep(10)  # Give time for page to load

        if page:
            html = page.content()
            print("Successfully loaded Facebook Marketplace!")
            print(html)
            # from bs4 import BeautifulSoup
            # soup = BeautifulSoup(html, "html.parser")
            # ... your parsing logic here ...
            time.sleep(100)
        else:
            print("No valid session found. Please log in manually.")
            fb.login(stay_open=True)
            # After manual login, try again
            context, page = fb.load_session()
            if page:
                print("Successfully logged in and loaded Marketplace!")
                html = page.content()
                print(html)
                # Your scraping logic here
                time.sleep(100)
            else:
                print("Failed even after manual login.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Trying manual login...")
        fb.login(stay_open=True)
        context, page = fb.load_session()
        if page:
            print("Successfully logged in after error!")
            time.sleep(100)
        else:
            print("Failed even after manual login.")

if __name__ == "__main__":
    main()