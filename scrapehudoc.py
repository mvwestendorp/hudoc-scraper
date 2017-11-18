from selenium import webdriver
import selenium
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
import MySQLdb
import re
import sys
import scrapecase as sc
import concurrent.futures
from multiprocessing.dummy import Pool as ThreadPool


connection = MySQLdb.connect(   host = "localhost",
                                user = "root",
                                passwd = "phpsuperw8",
                                db = "HUDOC")
cursor = connection.cursor()
sql = """SELECT `Application Number` FROM `judgements` WHERE 1"""
cursor.execute(sql)
appnos = cursor.fetchall()
connection.commit()
cursor.close()
connection.close()
appnos = [appno for element in appnos for appno in element]
appnos = list(set(appnos)) #undouble
nothreads = 1
if int(sys.argv[1]):
    nothreads = int(sys.argv[1])
chunks = [appnos[x:x+round(len(appnos)/nothreads)] for x in range(0, len(appnos), round(len(appnos)/nothreads))]

#sc.scrapecases(appnos)
#spawn threads and scrape
executor = concurrent.futures.ProcessPoolExecutor(nothreads)
futures = [executor.submit(sc.scrapecases, chunk) for chunk in chunks]
concurrent.futures.wait(futures)
