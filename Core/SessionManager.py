from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional
import time
import json
from playwright_stealth import stealth_sync
import random

class FacebookSessionManager:
    """
    Handles Facebook login and session persistence using Playwright.
    """
    def __init__(self, email: str, password: str, cookie_file: str = "auth.json"):
        self.email = email
        self.password = password
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
        with sync_playwright() as p:
            user_agent = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
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
            print("Navigated to Facebook login page.")
            time.sleep(random.uniform(1.2, 2.5))
            self.page.click("#email")
            self._human_type("#email", self.email)
            time.sleep(random.uniform(0.5, 1.2))
            self.page.click("#pass")
            self._human_type("#pass", self.password)
            time.sleep(random.uniform(0.5, 1.2))
            self.page.hover('button[name="login"]')
            time.sleep(random.uniform(0.2, 0.6))
            self.page.click('button[name="login"]')
            print("Login submitted. Waiting for redirect...")
            self.page.wait_for_load_state("networkidle", timeout=30000)
            time.sleep(random.uniform(2.5, 4.5))
            # Save session
            self.context.storage_state(path=self.cookie_file)
            print(f"Session saved to {self.cookie_file}")
            if stay_open:
                print("Browser will stay open. Close it manually when done.")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("Browser closing...")
            self.browser.close()

    def load_session(self, stay_open: bool = True) -> None:
        """
        Loads session from file and opens Facebook Marketplace. Keeps browser open for inspection.
        """
        with sync_playwright() as p:
            user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
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
                # Check if redirected to login (session expired)
                if "/login" in self.page.url:
                    print("Session invalid or expired. Redirected to login.")
                    raise Exception("Session expired")
                if stay_open:
                    print("Browser will stay open. Close it manually when done.")
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("Browser closing...")
                self.browser.close()
            except Exception as e:
                print(f"Failed to load session: {e}")
                print("You may need to re-login.")

if __name__ == "__main__":
    # Example usage
    EMAIL = "ibkinside@gmail.com"
    PASSWORD = "justicemen"
    fb = FacebookSessionManager(EMAIL, PASSWORD)
    # To login and save session:
    # fb.login(stay_open=True)
    # To load session and open Marketplace:
    fb.load_session(stay_open=True)
