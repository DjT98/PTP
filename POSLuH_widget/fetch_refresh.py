from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def refresh():
    # Set Firefox options for headless mode
    options = Options()
    options.add_argument('-headless')

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox(options=options)

    # Navigate to the login page
    driver.get('https://acc.posluh.hr/clientarea.php?action=domains')

    # Fill in the login form
    username_input = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
    username_input.send_keys('youremail@example.com') ##Your email

    password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    password_input.send_keys('yourpassword') ##Your password
    password_input.send_keys(Keys.ENTER)

    # Wait for the page to load after login
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains('clientarea.php?action=domains'))

    #Sort the domains
    sorting_element = driver.find_element(By.CSS_SELECTOR, 'th.sorting:nth-child(6)')
    sorting_element.click()

    # Get the page source after login
    page_source = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the row with the name "Aktivne"
    rows = soup.select('tr')

    active_domains=[]

    for row in rows:
    # Check if the row has the name "Aktivne"
        status_element = row.select_one('.sorting_1 > span.label')
        if status_element and status_element.text.strip() == 'Aktivne':
            # Print the values of td:nth-child(3) > a:nth-child(1) and td:nth-child(5)
            name_element = row.select_one('td:nth-child(3) > a:nth-child(1)')
            date_element = row.select_one('td:nth-child(5)')

            if name_element and date_element:
                visible_date = date_element.contents[-1].strip()
                domain = name_element.text.strip()
                active_domains.append((domain, visible_date))

    # Save the parsed HTML to a file
    with open('active_domains.txt', 'w') as file:
        for domain, date in active_domains:
            file.write(f"{domain}\n")
            file.write(f"{date}\n")
            file.write("\n")

    # Close the browser
    driver.quit()



refresh()