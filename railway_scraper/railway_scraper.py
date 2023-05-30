from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import argparse

parser = argparse.ArgumentParser()

# Add arguments for multiple inputs
parser.add_argument("fromdate", help="From date")
parser.add_argument("todate", help="to date")
args = parser.parse_args()
# Function to enter fromDate
def fromDate(date, driver):
    day,month,year = date.split('/')
    Day = Select(driver.find_element(By.ID, "fromDay"))
    Month = Select(driver.find_element(By.ID, "fromMonth"))
    Year = Select(driver.find_element(By.ID, "fromYear"))
    Day.select_by_value(day)
    Month.select_by_value(month)
    Year.select_by_value(year)
    return "From Date Successfull"   


#Function to enter toDate
def toDate(date, driver):
    day,month,year = date.split('/')
    Day = Select(driver.find_element(By.ID, "toDay"))
    Month = Select(driver.find_element(By.ID, "toMonth"))
    Year = Select(driver.find_element(By.ID, "toYear"))
    Day.select_by_value(day)
    Month.select_by_value(month)
    Year.select_by_value(year)
    return "To Date Successfull"   


def data(soup):
    lit = soup.find('table').find_all('table')[1].text.split()
    final = []
    length_lit = len(lit)
    start = 1
    end = 2
    while length_lit>0:
        try:
            final.append(lit[lit.index(str(start)):lit.index(str(end))])
            length_lit -= len(lit[lit.index(str(start)):lit.index(str(end))])
            start +=1
            end +=1
        except:
            final.append(lit[lit.index(str(start)):])
            break
    return final
     
        
def cleanList(trial):
    if len(trial) == 6:
        return [trial[0],trial[1]+" "+trial[2],trial[3],trial[4],trial[5]]
    else:
        return [trial[0],trial[1]+" "+trial[2]+" "+trial[3],trial[4],trial[5],trial[6]]
    
#calling function
driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://122.252.248.53/html/internal/coach_outturn_ex.asp")
From_Date = args.fromdate
To_Date = args.todate
print(From_Date)
print(To_Date)
fromDate(From_Date, driver)
toDate(To_Date, driver)
submitButton = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td/form/table[2]/tbody/tr/td[2]/input')
submitButton.click()
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
Extracted_data = data(soup)
final_list = list(map(cleanList,Extracted_data))
header = ['S.No','Railways','Coach Type','Coach No','Despatched Date']
df = pd.DataFrame(final_list, columns = header)
df.to_csv('railway.csv')
