import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import base64

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://src.udiseplus.gov.in/locateSchool/schoolSearch'
driver.get(url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'stateName')))
select_element = Select(driver.find_element(By.ID, 'stateName'))
select_element.select_by_value('109')  # '109' corresponds to Uttar Pradesh

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//select[@id='districtId']/option[@value='1827']"))
)
select_element = Select(driver.find_element(By.ID, 'districtId'))
select_element.select_by_value('1827')  # '1827' corresponds to Lucknow

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//select[@id='blockId']/option[@value='18338']"))
)
select_element = Select(driver.find_element(By.ID, 'blockId'))
select_element.select_by_value('18338')  # '18338' corresponds to NAGAR SHAITRA LUCKNOW

search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='searchSchool'][@type='submit']"))
)
search_button.click()

time.sleep(10)

search_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.form-control.form-control-sm[type="search"]'))
)
search_input.send_keys("CITY MONTESSORI SCHOOL")
search_input.send_keys(Keys.ENTER)

WebDriverWait(driver, 35).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody > tr"))
)

original_window = driver.current_window_handle

first_row = driver.find_element(By.CSS_SELECTOR, "tbody > tr")
clickable_link = first_row.find_element(By.TAG_NAME, "a")
clickable_link.click()

time.sleep(3)

new_window = [window for window in driver.window_handles if window != original_window][0]
driver.switch_to.window(new_window)

WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.CLASS_NAME, "ulInlineFlex"))
)

col_7_elements = driver.find_elements(By.CLASS_NAME, "ulInlineFlex")

for element in col_7_elements:
    print(element.text)
    
    
buttons = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.ulInlineFlex.mb-2 > li:not(:first-child) button"))
)

for index, button in enumerate(buttons, start=1):
    button.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "myModalReport"))
    )

    pdf_embed = driver.find_element(By.ID, "ReportCardpdfopenModelURlEmbed")
    pdf_data = pdf_embed.get_attribute('src').split(',', 1)[1]

    with open(f"report{index:02}.pdf", "wb") as pdf_file:
        pdf_file.write(base64.b64decode(pdf_data))

    close_button = driver.find_element(By.CSS_SELECTOR, ".modal-header .close")
    close_button.click()

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element((By.ID, "myModalReport"))
    )
    
    file_path = f"./report{index:02}.pdf"

    with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[1]
        text = page.extract_text()
        array = text.split()
        try:
            delimiter_index = array.index("Source")
            newarray = array[:delimiter_index]
            print(newarray[-1])
        except ValueError:
            try:
                delimiter_index = array.index("Disclaimer")
                newarray = array[:delimiter_index]
                print(newarray[-1])
            except ValueError:
                print("Source and Disclaimer not found.")
                # WRITE CODE IF NOTHING IS COMING

    time.sleep(1)


time.sleep(20)

driver.quit()
