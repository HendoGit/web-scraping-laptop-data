import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as bs

#Run webdriver in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

#Url contains webpage for laptop listings at best-buy
def open_url(driver):
    url = 'https://www.bestbuy.com/site/laptop-computers/all-laptops/pcmcat138500050001.c?id=pcmcat138500050001'
    driver.get(url)


def collect_all_laptops_from_current_page(driver):
    page_cards = driver.find_elements_by_class_name("sku-item")
    return page_cards


def next_page(driver):
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "sku-list-page-next")))
    driver.find_element_by_class_name("sku-list-page-next").click()


def select_state(driver):
    xpath_US_button = '/html/body/div[2]/div/div/div/div[1]/div[2]/a[2]'
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, xpath_US_button)))
    driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]/a[2]').click()


def save_to_csv(records, file_name, mode='+'):
    header = ['Laptop Description', 'Screen Size (Inches)', 'Processor']
    with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(header)
        if records:
            writer.writerow(records)


def get_laptops_from_current_page(driver):
    html = driver.page_source
    soup = bs(html, 'html.parser')
    mydivs = soup.find_all(class_="sku-item")
    return mydivs


processors = ['i3', 'i5', 'i7', 'i9', 'Intel Celeron', 'Apple M1', 'AMD Ryzen 3', 'AMD Ryzen 5', 'AMD Ryzen 7', 'AMD Ryzen 9']

def parse_processor(text):
    for processor in processors:
        if processor in text:
            return processor
        else:
            return False

def parse_screen_size(text):
    ind = text.find('"')
    if ind == -1:
        ind = text.find('”')
        if ind == -1:
            ind = text.find('-inch')
    else:
        pass
    space_loc = 0
    for i in range(2, 8):
        cha = text[ind - i]
        if cha == ' ':
            print(cha)
            space_loc = ind - i
            break
    return text[space_loc+1:ind]


def main(file_name):
    #Create blank csv file to store laptop records in
    save_to_csv(None, file_name, 'header')
    #Initiate chromedriver and navigate to bestbuy.com
    driver = webdriver.Chrome()
    open_url(driver)
    select_state(driver)
    #Iterate through all of the pages on bestbuy
    for pages in range(46):
        #Sleep for 20 seconds (Website is slow and takes ages to fully load)
        time.sleep(20)
        laptop_divs = get_laptops_from_current_page(driver)

        for i in laptop_divs:
            try:
                t1 = i.find_all(class_="sku-title")[0]
                title = t1.text

                processor = parse_processor(title)
                screen_size = parse_screen_size(title)

                span_elements = i.find_all("span")

                for j in span_elements:
                    span = j.text
                    try:
                        if span[0] == '$':
                            price = float(span.replace('$', "").replace(',', ''))
                    except:
                        pass
            except:
                pass

            laptop = [title, price, screen_size, processor]
            save_to_csv(laptop, file_name)
            

if __name__ == '__main__':
    file_name = 'laptop_data.csv'
    main(file_name)
