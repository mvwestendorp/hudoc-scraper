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
import cProfile

import MySQLdb
import re
#import concurrent.futures
from multiprocessing.dummy import Pool


def scrapecaselist(appnos):
    pr = cProfile.Profile()
    pr.enable()
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
    pr.disable()
    pr.print_stats(sort='time')
    print ("Quiting scrapecases function")

def insert_slash(string, index):
    return string[:index] + '/' + string[index:]
	
def scrapecases():
	connection = MySQLdb.connect(   host = "localhost",
									user = "root",
									passwd = "phpsuperw8",
									db = "hudoc")
	cursor = connection.cursor(nothreads = 1)
	#TODO change sql to get only missing items
	sql = """SELECT `Application Number` FROM `judgements` WHERE 1"""
	cursor.execute(sql)
	appnos = cursor.fetchall()
	connection.commit()
	cursor.close()
	connection.close()
	appnos = [appno for element in appnos for appno in element]
	appnos = list(set(appnos)) #undouble
	
	#nothreads = 1
	#if len(sys.argv) >= 2:
	#	nothreads = int(sys.argv[1])

	#sc.scrapecases(appnos)
	#spawn threads and scrape
	#executor = concurrent.futures.ProcessPoolExecutor(nothreads)
	#futures = [executor.submit(sc.scrapecases, chunk) for chunk in chunks]
	#concurrent.futures.wait(futures)

	with Pool(processes=nothreads) as pool:
		pool.map(scrapecaselist, [appnos[x:x+round(len(appnos)/nothreads)] for x in range(0, len(appnos), round(len(appnos)/nothreads))]) 
		pool.close()
		pool.join()

