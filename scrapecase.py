from selenium import webdriver
import selenium
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
import time
import sys
from bs4 import BeautifulSoup
import os
import string

#TODO check why some webdrivers fail.

def scrapecases(appnos):
    options= Options()    
    options.add_argument('-headless')
    driver = webdriver.Firefox(executable_path='geckodriver', firefox_options=options)
    for appno in appnos:
        print ("Starting scraping of case:", appno)
        filename = "./cases/case_details_" + str(appno) + ".txt"
        filename = filename.replace(' ','')
        if os.path.isfile(filename):
            print("Case "+str(appno)+" has already been scraped, remove file to update")
        else:    
            try:           
                #print("Trying scraping case:"+str(appno))                
                strappno = str(appno)
                appnowslash = insert_slash(strappno, len(strappno)-2)
                driver.get('http://hudoc.echr.coe.int/eng#{"appno":["'+ appnowslash+'"]}')
                #print("First wait")                
                wd = WebDriverWait(driver, 30).until(
                    expected.presence_of_element_located((By.CLASS_NAME, 'document-link.headline'))
                )
                d = driver.find_element_by_class_name('document-link.headline')
                d.click()
                #print (d.get_attribute('href')) #contains itemid
                text = (str(driver.find_element_by_tag_name('html').text).encode('utf-8')) #to load casetext
                #print("Second wait")
                wd = WebDriverWait(driver, 30).until(
                    expected.presence_of_element_located((By.ID, 'notice'))
                )    
                d = driver.find_element_by_id('notice')
                d.click()
                #print("Third wait")
                wd = WebDriverWait(driver, 30).until(
                    expected.presence_of_element_located((By.CLASS_NAME, 'viewarea'))
                )
                #print("Before retrieving viewarea")
                rows = driver.find_element_by_class_name('viewarea')
                #print(rows)
                #print("Opening file")
                file = open(filename,"w")
                file.write(str(rows.get_attribute('innerHTML').encode('utf-8')))
                file.close()
            except:
                print("Error, restarting driver?")
                driver.quit() 
                driver = webdriver.Firefox(executable_path='geckodriver', firefox_options=options)               
    #driver.quit()
    print ("Quiting scrapecases function")
def insert_slash(string, index):
    return string[:index] + '/' + string[index:]

