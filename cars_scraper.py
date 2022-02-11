import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

PATH = "/Users/juanpih19/Desktop/Metis/Regression/Regression Project/chromedriver"
driver = webdriver.Chrome(PATH)

def access_website():
    driver.get('https://www.cars.com/')
    all_cars = driver.find_element_by_xpath('//*[@id="by-make-tab"]/div/div[7]/button')
    all_cars.click()
    time.sleep(3)
    return driver.page_source

def access_each_car(x):
    soup = BeautifulSoup(x, features='lxml')
    cars = soup.find(class_="vehicle-cards")
    #vehicle_details = cars.find_all(class_ ="mileage")
    #return vehicle_details
    return cars


def find_links(x):
    all_links = []
    soup = BeautifulSoup(x, features='lxml')
    links = soup.find_all('a', class_="vehicle-card-link js-gallery-click-link")
    for i in links:
        all_links.append(i['href'])
    return all_links


info = {"Title": [], "Used": [], "Mileage": [], "Price": [],
        "Exterior color": [], "Interior color": [], "Drive train": [],
         "MPG": [], "Fuel type": [], "Transmission": []}

def get_info(links):

    try:
        for link in links:
            driver.get(f'https://www.cars.com{link}')
            source = driver.page_source
            time.sleep(2)

            soup = BeautifulSoup(source, features='lxml')


            # Price info
            price = soup.find(class_='primary-price')
            info['Price'].append(price.text)

            # Title info
            title = soup.find(class_="listing-title")
            info['Title'].append(title.text)

            # Used info
            used = soup.find(class_="new-used")
            info['Used'].append(used.text)

            # Mileage info
            mileage = soup.find(class_="listing-mileage")
            info['Mileage'].append(mileage.text)

            time.sleep(1)


            basic_features = soup.find(class_="sds-page-section basics-section")
            all_features = basic_features.find_all('dd')

            info['Exterior color'].append(all_features[0].text)
            info['Interior color'].append(all_features[1].text)
            info['Drive train'].append(all_features[2].text)
            info['MPG'].append(all_features[3].text)
            info['Fuel type'].append(all_features[4].text)
            info['Transmission'].append(all_features[5].text)

            time.sleep(2)

    except:
        pass

    return info


def save_data(dictionary):
    data = pd.read_csv("/Users/juanpih19/Desktop/Metis/Regression/Regression Project/final_data2.csv")
    new_data = pd.DataFrame(dictionary)
    final_data = pd.concat([data, new_data], ignore_index=True)
    return final_data.to_csv("/Users/juanpih19/Desktop/Metis/Regression/Regression Project/final_data2.csv", index=False)


def next_page(num):
    driver.get(f'https://www.cars.com/shopping/results/?page={num}&page_size=20&list_price_max=&makes[]=&maximum_distance=20&models[]=&stock_type=all&zip=36608')
    return driver.page_source




if __name__ == '__main__':
    num = 30
    while num < 60:
        page_code = next_page(num)
        each_car = find_links(page_code)
        time.sleep(3)
        all_info = get_info(each_car)
        num += 1

    save_data(all_info)
