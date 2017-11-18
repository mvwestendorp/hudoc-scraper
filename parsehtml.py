from bs4 import BeautifulSoup
import MySQLdb
import re
import sys

connection = MySQLdb.connect(   host = "localhost",
                                user = "root",
                                passwd = "phpsuperw8",
                                db = "HUDOC")
cursor = connection.cursor()
appno = sys.argv[1] #or just loop over all files in folder?
filename = "case_details_" + appno + ".txt"
file = open(filename,"r")
html = file.read()
#use beautifulsoup to parse html here
soup = BeautifulSoup(html, 'html.parser')
results = soup.find_all(class_='row noticefield')

for result in results:
    heading = result.find(class_='span2 noticefieldheading ')
    noticefield = result.find(class_='col-offset-2 noticefieldvalue')
    #print ("Heading: ", heading.get_text())
    fields = noticefield.find_all("div")

    if "Case-Law" in heading.get_text():
        #linked-case-law
        for field in fields:
            #print (field.get_text())
            #grep regex break on empty, todo check for double app-no's
            linkno = re.search("\d{4,6}\/\d{2}", field.get_text())
            if linkno is None:
                print ("Warning: empty linked-case-law line in: ",field)
                break
            linkno = linkno.group(0)
            linkno = linkno.replace('/','')
            if len(linkno) == 0:
                break
            sql = """REPLACE INTO `linked-case-law` (`Application Number`,`Link Number`) VALUES ({appnum}, {linknum});"""
            sql = sql.format(appnum=appno, linknum=linkno)          
            cursor.execute(sql)
    if "Article" in heading.get_text():
        #Articles
        for field in fields:
            #print (field.get_text())
            #grep regex linked-appno into artno *remove characters P articles? group \2 -> - dash
            pval = re.search("^P", field.get_text());
            line = re.search("(\d*(-)\d*|\d*)", field.get_text())
            if line is None:
                print ("Warning: empty articles line")
                break          
            artno = line.group(0)
            artno = artno.replace('-', '.') #into decimal sql -> regex leaves only 1 - for known variables
            if len(artno) == 0:
                break
            sql = """REPLACE INTO articles (`Application Number`,`Article Number`,`Protocol`) VALUES ({appnum}, {artnum}, {protval});"""
            if pval:
                sql = sql.format(appnum=appno, artnum=artno, protval=1)
            else:
                sql = sql.format(appnum=appno, artnum=artno, protval=0)
            #print(sql)     
            cursor.execute(sql)
    if "Keywords" in heading.get_text():
        #Keywords
        for field in fields:
            #print (field.get_text())
            keyword = field.get_text()
            if "more" in keyword:
                print("Warning: more should be clicked during scraping!")
                break
            #TODO remove multiline entries (are dups)
            sql = """REPLACE INTO `keywords` (`Application Number`, `Keyword`) VALUES ({appnum}, "{keyw}");"""
            sql = sql.format(appnum=appno, keyw=keyword)
            #print(sql)           
            cursor.execute(sql)
    if "Conclusion" in heading.get_text():
        #Conclusion
        for field in fields:
            #print (field.get_text())
            conclusion = field.get_text()
            if "more.." in conclusion:
                break
            sql = """REPLACE INTO conclusions (`Application Number`, `Conclusion`) VALUES ({appnum}, "{conc}");"""
            sql = sql.format(appnum=appno, conc=conclusion)      
            cursor.execute(sql)

cursor.execute(sql)
connection.commit()
cursor.close()
connection.close()
