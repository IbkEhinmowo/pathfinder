from playwright.sync_api import sync_playwright
import time

# Constants
BASE_URL = "https://www.facebook.com"
EMAIL = "ibkinsidegmail.com"
PASSWORD = "justicemen"

def main():
    # Start Playwright
    with sync_playwright() as playwright:
        # Launch browser
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to Facebook
            page.goto(BASE_URL)
            print("Navigated to site.")
            print(f"Current URL: {page.url}")
            
            time.sleep(1)  # Add delay to ensure URL is updated
            print(f"URL after delay: {page.url}")
            
            # Login
            print("Logging in...")
            
            # Wait for and fill email field
            email_field = page.wait_for_selector("#email", timeout=10000)
            email_field.fill(EMAIL)
            
            # Wait for and fill password field
            password_field = page.wait_for_selector("#pass", timeout=10000)
            password_field.fill(PASSWORD)
            
            # Wait for and click login button
            time.sleep(3)
            login_button = page.wait_for_selector('input[name="login"]', timeout=10000)
            login_button.click()
            
            print("Login attempted...")
            
            # Wait a bit for login to process
         
            
            # Click marketplace
            print("Looking for Marketplace button...")
            marketplace_button = page.wait_for_selector('[aria-label="Marketplace"]', timeout=10000)
            marketplace_button.click()
            print("Successfully clicked Marketplace button")
            
            # Keep browser open for a while to see the result
            time.sleep(10)
            
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            # Close browser
            browser.close()

if __name__ == "__main__":
    main()