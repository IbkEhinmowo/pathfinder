from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import src.constant as value
import time

class Search:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def target_site(self):
        self.driver.get(value.BASE_URL)
        print("Navigated to site.")
        print(f"Current URL: {self.driver.current_url}")

        time.sleep(1)  # Add delay to ensure URL is updated
        print(f"URL after delay: {self.driver.current_url}")

        self.login(value.EMAIL, value.PASSWORD)
        



        time.sleep(4000)
        self.driver.quit()

    def login(self, email, password):
        wait = WebDriverWait(self.driver, 10)
        login = wait.until(EC.element_to_be_clickable((By.ID, "email")))
        password_field = wait.until(EC.element_to_be_clickable((By.ID, "pass")))
        login.send_keys(email)
        password_field.send_keys(password)
        button = wait.until(EC.element_to_be_clickable((By.NAME, "login")))
        button.click()

    def click_marketplace(self):
        """Click on the Marketplace button"""
        wait = WebDriverWait(self.driver,5)
        marketplace_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Marketplace"]')))
        marketplace_button.click()
        print("Successfully clicked Marketplace button")
