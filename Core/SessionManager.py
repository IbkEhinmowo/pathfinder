from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional
import time
import json
from playwright_stealth import stealth_sync
import random
import os

class FacebookSessionManager:
    """
    Handles Facebook login and session persistence using Playwright.
    """
    def __init__(self, email: str, password: str, cookie_file: str = None):
        
        self.email = email
        self.password = password
        if cookie_file is None:
            home = os.path.expanduser("~")
            fb_auth_dir = os.path.join(home, "FBAuth")
            if not os.path.exists(fb_auth_dir):
                os.makedirs(fb_auth_dir, exist_ok=True)
            self.cookie_file = os.path.join(fb_auth_dir, "auth.json")
        else:
            self.cookie_file = cookie_file
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def _human_type(self, selector: str, text: str) -> None:
        """Type text into a field with random delays to simulate human typing."""
        for char in text:
            self.page.type(selector, char, delay=random.randint(80, 180))
            time.sleep(random.uniform(0.05, 0.2))

    def login(self, stay_open: bool = False) -> None:
        """
        Opens Facebook login page and lets the user sign in manually. After login, saves the session cookies.
        """
        with sync_playwright() as p:
            user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
            viewport = {"width": 1280, "height": 800}
            self.browser = p.chromium.launch(headless=False)
            self.context = self.browser.new_context(
                user_agent=user_agent,
                viewport=viewport
            )
            self.page = self.context.new_page()
            stealth_sync(self.page)
            self.page.goto("https://www.facebook.com")
            print("Please sign in to Facebook manually in the opened browser window.")
            print("After you have completed login and the page has fully loaded, press Ctrl+C here to save the session and close the browser.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Saving session and closing browser...")
                self.context.storage_state(path=self.cookie_file)
                print(f"Session saved to {self.cookie_file}")
                self.browser.close()

    def load_session(self):
        """
        Loads session from file and opens Facebook Marketplace. 
        Returns (context, page) for use in parser.
        """
        with sync_playwright() as p:
            user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
            viewport = {"width": 1280, "height": 800}
            try:
                self.browser = p.chromium.launch(headless=False)
                self.context = self.browser.new_context(
                    storage_state=self.cookie_file,
                    user_agent=user_agent,
                    viewport=viewport
                )
                self.page = self.context.new_page()
                stealth_sync(self.page)
                self.page.goto("https://www.facebook.com/marketplace/you/")
                print("Opened Facebook Marketplace with loaded session.")
                
                
                # Always return context and page, let caller manage browser
                return self.context, self.page
    
            except Exception as e:
                print(f"Failed to load session: {e}")
                print("You may need to re-login.")
                return None, None

# if __name__ == "__main__":
#     # Example usage
#     EMAIL = "ibkinside@gmail.com"
#     PASSWORD = "justicemen"

#     fb = FacebookSessionManager(EMAIL, PASSWORD)
#     # To login and save session:
#     # fb.login(stay_open=True)
#     # To load session and open Marketplace:
#     fb.load_session()
