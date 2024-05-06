import unittest
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestDictionaryAppIntegration(unittest.TestCase):
    def setUp(self):
        # Setup Selenium WebDriver with Firefox options
        firefox_options = Options()
        geckodriver_path = 'geckodriver'
        firefox_options.binary_location = '/Applications/Firefox.app/Contents/MacOS/firefox'

        # Setting up the WebDriver with the specified binary location
        self.driver = webdriver.Firefox(service=Service(
            geckodriver_path), options=firefox_options)
        self.driver.implicitly_wait(10)  # Set an implicit wait of 10 seconds
        self.driver.get('http://127.0.0.1:5000')  # URL of your Flask app
        # Assume Flask app is already running locally

    def test_submit_and_lookup(self):
        try:
            # Find the input element by its ID
            input_element = self.driver.find_element(By.ID, 'dict-input')

            # Simulate typing into the element
            input_element.send_keys('apple:fruit,banana:yellow')

            # Find the submit and lookup buttons
            submit_button = self.driver.find_element(By.ID, 'submit-btn')
            lookup_button = self.driver.find_element(By.ID, 'lookup-btn')

            # Click the submit button
            submit_button.click()
            time.sleep(2)

            # Wait for the AJAX request to complete and the result to be present
            # Wait for the outer div with id 'key-hashing' to be present and have exactly 2 children
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#key-hashing > div:nth-child(2)"))
            )

            # Further conditions based on the children's content
            boxes = self.driver.find_elements(
                By.CSS_SELECTOR, "#key-hashing > div")
            first_child = boxes[0].find_elements(By.TAG_NAME, 'span')
            second_child = boxes[1].find_elements(By.TAG_NAME, 'span')

            # Check for the expected result in the response
            self.assertIn(first_child[0].text, ['apple', 'banana'])
            self.assertIn(second_child[0].text, ['apple', 'banana'])

            # Wait for a specific duration before proceeding
            time.sleep(5)  # Adjust the duration as needed

            # Clear the input element
            input_element.clear()
            time.sleep(2)

            # Simulate typing a key into the input element
            input_element.send_keys("apple")

            # Click the lookup button
            lookup_button.click()
            time.sleep(5)

            # Get the value from the input element after the lookup
            value = input_element.get_attribute('value').split(":")[1]

            # Check if the obtained value matches the expected value
            self.assertIn(value, "fruit")

        except NoSuchElementException:
            self.fail("Could not find the required element on the page")
        except TimeoutException:
            self.fail("Timed out waiting for the AJAX request to complete")
        except Exception as e:
            self.fail(f"An unexpected error occurred: {str(e)}")

    def test_delete_feature(self):
        try:
            input_element = self.driver.find_element(By.ID, 'dict-input')

            # Simulate typing into the element
            input_element.send_keys('apple:fruit,banana:yellow')

            # Find the submit and lookup buttons
            submit_button = self.driver.find_element(By.ID, 'submit-btn')

            # Click the submit button
            submit_button.click()
            time.sleep(2)

            # Wait for the AJAX request to complete and the result to be present
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#key-hashing > div:nth-child(2)"))
            )

            # Find the input element by its ID
            input_element = self.driver.find_element(By.ID, 'dict-input')
            input_element.clear()
            time.sleep(1)
            # Simulate typing a key into the input element
            input_element.send_keys("apple")
            # Find the delete button
            delete_button = self.driver.find_element(By.ID, 'delete-btn')

            # Click the delete button
            delete_button.click()
            time.sleep(5)
            boxes = self.driver.find_elements(
                By.CSS_SELECTOR, "#key-hashing > div")

            first_child = boxes[0].find_elements(By.TAG_NAME, 'span')
            time.sleep(2)
            # check if has value is removed
            self.assertLess(len(first_child[0].text), 10)

        except NoSuchElementException:
            self.fail("Could not find the required element on the page")
        except TimeoutException:
            self.fail("Timed out waiting for the AJAX request to complete")
        except Exception as e:
            self.fail(f"An unexpected error occurred: {str(e)}")

    def tearDown(self):
        # Quit the WebDriver instance
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
