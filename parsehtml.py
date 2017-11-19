from bs4 import BeautifulSoup
import MySQLdb
import re
import sys
import concurrent.futures



from os import listdir
from os.path import isfile, join
import time
import cProfile

def parsecase(appnos):
    connection = MySQLdb.connect(   host = "localhost", user = "root", passwd = "phpsuperw8", db = "HUDOC")
    cursor = connection.cursor()
    succases = 0
    numcases = 0
    for appno in appnos:
        numcases +=1
        print(str(numcases)+": Start parsing case: " + str(appno) + " progress: " + str(succases/len(appnos)*100) + "% Running time: " + str(time.time()-start) + " failures: " + str(numcases-succases-1))
        filename = "./cases/case_details_" + str(appno) + ".txt"
        #print(filename)
        file = open(filename,"r")
        html = file.read()
        #print(html)
        #use beautifulsoup to parse html here
        soup = BeautifulSoup(html, 'html.parser')
        
        #print("Insert case txt in database")
        findcasetxt = soup.find(class_='content')
        casetxt = str()
        #print('findcase is none?')
        if findcasetxt is None:
            casetxt = ''
        else:        
            casetxt = findcasetxt.get_text()
        #print('after findcase')
        sql = """INSERT INTO `case-text` (`Application Number`,`Case Text`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `Case Text` = %s;"""
        #sql = sql.format(appnum=appno, casetext=casetxt)
        #print(sql)
        try:
            cursor.execute(sql,(appno, casetxt, casetxt))
        except:
            print("SQL error in query: ", sql)
            exit()
        #print ("Inserted case txt in database.")

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
                    linkno = re.search("\d{2,6}\/\d{2}", field.get_text())
                    if linkno is None:
                        #print ("Warning: empty linked-case-law line in: ",field)
                        break
                    linkno = linkno.group(0)
                    linkno = linkno.replace('/','')
                    if len(linkno) == 0:
                        break
                    sql = """INSERT INTO `linked-case-law` (`Application Number`,`Link Number`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `Link Number`= %s;"""
                    #sql = sql.format(appnum=appno, linknum=linkno)          
                    cursor.execute(sql,(appno, linkno, linkno))
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
                    sql = """INSERT INTO articles (`Application Number`,`Article Number`,`Protocol`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `Article Number`=%s, `Protocol`=%s;"""
                    if pval:
                        protval=1
                    else:
                        protval=0
                    #print(sql)     
                    cursor.execute(sql,(appno,artno,protval,artno,protval))
            if "Keywords" in heading.get_text():
                #Keywords
                for field in fields:
                    #print (field.get_text())
                    keyword = field.get_text()
                    if "more" in keyword:
                        #print("Warning: more should be clicked during scraping!")
                        break
                    #TODO remove multiline entries (are dups)
                    sql = """INSERT INTO `keywords` (`Application Number`, `Keyword`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `Keyword`=%s;"""
                    #print(sql)           
                    cursor.execute(sql,(appno,keyword,keyword))
            if "Conclusion" in heading.get_text():
                #Conclusion
                for field in fields:
                    #print (field.get_text())
                    conclusion = field.get_text()
                    if "more.." in conclusion:
                        break
                    sql = """INSERT INTO conclusions (`Application Number`, `Conclusion`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `Conclusion`=%s;"""
                    sql = sql.format(appnum=appno, conc=conclusion)      
                    cursor.execute(sql,(appno,conclusion,conclusion))
        succases +=1    
    print("Closing sql connection, succesful cases: ", succases)
    connection.commit()
    cursor.close()
    connection.close()
    return succases

start = time.time()
pr = cProfile.Profile()
pr.enable()
mypath = "./cases"
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
appnos = list()
for filename in filenames:
    appno = re.findall("\d*",str(filename))
    appnos.extend(appno)
appnos = list(filter(None, appnos))
nothreads = 1
if len(sys.argv) == 2:
    nothreads = int(sys.argv[1])
cases = [appnos[x:x+round(len(appnos)/nothreads)] for x in range(0, len(appnos), round(len(appnos)/nothreads))]
print ("Parsing ", len(appnos), " cases")
print ("Spawning ", nothreads, " threads")
executor = concurrent.futures.ProcessPoolExecutor(nothreads)
futures = [executor.submit(parsecase, case) for case in cases]
concurrent.futures.wait(futures)

end = time.time()
print("Total execution time: ", end-start)
pr.disable()

#pr.print_stats(sort='time')
