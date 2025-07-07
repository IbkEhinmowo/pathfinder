# from playwright.sync_api import sync_playwright
# import src.constant as value
# import time

# class Search:
#     def __init__(self):
#         self.playwright = None
#         self.browser = None
#         self.page = None

#     def __enter__(self):
#         self.playwright = sync_playwright().start()
#         self.browser = self.playwright.chromium.launch(headless=False)
#         self.page = self.browser.new_page()
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.browser:
#             self.browser.close()
#         if self.playwright:
#             self.playwright.stop()

#     def target_site(self):
#         self.page.goto(value.BASE_URL)
#         print("Navigated to site.")
#         print(f"Current URL: {self.page.url}")

#         time.sleep(1)  # Add delay to ensure URL is updated
#         print(f"URL after delay: {self.page.url}")

#         self.login(value.EMAIL, value.PASSWORD)
        
#         time.sleep(4000)

#     def login(self, email, password):
#         # Wait for and fill email field
#         email_field = self.page.wait_for_selector("#email", timeout=10000)
#         email_field.fill(email)
        
#         # Wait for and fill password field
#         password_field = self.page.wait_for_selector("#pass", timeout=10000)
#         password_field.fill(password)
        
#         # Wait for and click login button
#         login_button = self.page.wait_for_selector('input[name="login"]', timeout=10000)
#         login_button.click()

#     def click_marketplace(self):
#         """Click on the Marketplace button"""
#         marketplace_button = self.page.wait_for_selector('[aria-label="Marketplace"]', timeout=5000)
#         marketplace_button.click()
#         print("Successfully clicked Marketplace button")
