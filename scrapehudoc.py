import pycurl
import MySQLdb
import re
import datetime
import scrapecase
import csv

def read_file(filename):
	with open(filename, mode='r') as infile:
		#reader = csv.reader(infile)
		#mydict = {rows[0]:rows[5] for rows in reader}
		#return mydict
		content = infile.readlines()
		content = [x.strip() for x in content] 
		return content

#param format: '%Y-%m-%d'
#cursor to database as cursor
def getcaselist(fromdate,todate, cursor):
	print("Parsing from date " + str(fromdate) + " to " + str(todate), end='\r')
	url = 'https://hudoc.echr.coe.int/app/transform/csv?library=echreng&query=contentsitename%3AECHR%20AND%20(NOT%20(doctype%3DPR%20OR%20doctype%3DHFCOMOLD%20OR%20doctype%3DHECOMOLD))%20AND%20((documentcollectionid%3D%22GRANDCHAMBER%22)%20OR%20(documentcollectionid%3D%22CHAMBER%22))%20AND%20(kpdate%3E%3D%22'+fromdate+'T00%3A00%3A00.0Z%22%20AND%20kpdate%3C%3D%22'+todate+'T00%3A00%3A00.0Z%22)&sort=&start=0&length=500&rankingModelId=11111111-0000-0000-0000-000000000000'
	#print(url)
	## Parse csv into database
	#post_data = ''
	fp = open('temp_file.csv','wb')
	#response = io.BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	#c.setopt(c.WRITEFUNCTION, response.write)
	c.setopt(c.WRITEFUNCTION, fp.write)
	#c.setopt(pycurl.VERBOSE, 1)
	#c.setopt(c.HTTPHEADER, 0)
	#c.setopt(c.POSTFIELDS, post_data)
	c.perform()
	
	
	#read downloaded csv file
	cr_dict = read_file('temp_file.csv')
	fp.close()
	#if response > 500 entries, split date and recall function
	# Check if file <501 lines
	#print(len(cr_dict))
	c.close()
	cr_dict.pop(0) # remove row with column names
	if len(cr_dict) <= 500:
		for case in cr_dict:
			cr = case.split(',')
			#print(cr)
			date = cr[4].split(" ")
			print(cr[1])
			sql = 'REPLACE INTO `judgements` (`Document Title`, `Application Number`, `Document Type`, `Originating Body`, `Date`, `Conclusion`) VALUES (%s,%s,%s,%s,%s,%s)';
			cursor.execute(sql, (cr[0], cr[1].replace("/",""), cr[2], cr[3], datetime.datetime.strptime(date[0], "%d/%m/%Y"), cr[5]))
	else:
		#date diff /2 -> call function two times for lower and upper bound (threads?)
		getcaselist(fromdate, fromdate + (todate-fromdate)/2 + 1)
		getcaselist(fromdate + (todate-fromdate)/2, todate)
	


def crawl(lastsync):
	### Establish connection to database
	connection = MySQLdb.connect(   host = "localhost",
									user = "root",
									passwd = "phpsuperw8",
									db = "hudoc")
	connection.set_character_set('utf8')
	
	cursor = connection.cursor()
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')
	today = datetime.datetime.now().strftime('%Y-%m-%d')
	getcaselist(lastsync,"2001-06-01",cursor)
	connection.commit()
	cursor.close()
	connection.close()
	return True
	
crawl("2001-05-01")