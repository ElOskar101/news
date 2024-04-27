from selenium.webdriver.common.by import By


def scrapping(driver, url):
    driver.get(url)
    box = driver.find_element(By.CSS_SELECTOR, 'form > input[type="text"]')
    box.click()
    box.send_keys("Today's news")
    driver.find_element(By.CSS_SELECTOR, 'button[value="Search"]').click()

