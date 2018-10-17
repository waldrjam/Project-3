import os.path
def get_log():
	from urllib.request import urlretrieve
	url_path = 'https://s3.amazonaws.com/tcmg476/http_access_log'
	local_file = 'local_copy.log'
	#urlretrieve fetches what is saved in url_path and saves it as local_copy.log
	local_file, headers = urlretrieve(url_path, local_file)
	return()
def num_of_days(f,l):
	#each day and year, need to be converted to ints
	f_day = int(f[0])
	l_day = int(l[0])
	f_year = int(f[2])
	l_year = int(l[2])
	#month cant be converted so best way I can think to do this is to have if and elif for each month
	#I could just make it = 8 but that wouldn't work for a different log.
	if f[1] == 'Jan':
		f_month = 1
	elif f[1] == 'Feb':
		f_month = 2
	elif f[1] == 'Mar':
		f_month = 3
	elif f[1] == 'Apr':
		f_month = 4
	elif f[1] == 'May':
		f_month = 5
	elif f[1] == 'Jun':
		f_month = 6
	elif f[1] == 'Jul':
		f_month = 7
	elif f[1] == 'Aug':
		f_month = 8
	elif f[1] == 'Sep':
		f_month = 9
	elif f[1] == 'Oct':
		f_month = 10
	elif f[1] == 'Nov':
		f_month = 11
	elif f[1] == 'Dec':
		f_month = 12
    ## same for l_month
	if l[1] == 'Jan':
		l_month = 1
	elif l[1] == 'Feb':
		l_month = 2
	elif l[1] == 'Mar':
		l_month = 3
	elif l[1] == 'Apr':
		l_month = 4
	elif l[1] == 'May':
		l_month = 5
	elif l[1] == 'Jun':
		l_month = 6
	elif l[1] == 'Jul':
		l_month = 7
	elif l[1] == 'Aug':
		l_month = 8
	elif l[1] == 'Sep':
		l_month = 9
	elif l[1] == 'Oct':
		l_month = 10
	elif l[1] == 'Nov':
		l_month = 11
	elif l[1] == 'Dec':
		l_month = 12
	
	#find out the number of days between two points
	from datetime import date
	
	d0 = date(f_year, f_month, f_day)
	d1 = date(l_year, l_month, l_day)
	delta = d1 - d0
	return (delta.days)
	
def save_to_file(value, key):
	##creates a new file with the name of the key 
	##this should seperate each month of log file into their own thing
	filename = "%s.txt" % key
	f = open(filename , 'wb')
	with open(filename, 'w') as filehandle:  
		for line in value:
			filehandle.write('%s\n' % line)

#Checks if local_copy.log already exists, if it does get_log does not run.
file_name = 'local_copy.log'
if os.path.isfile(file_name):
	print ("file already exisits")
else:
	get_log()

code4xx = 0
code3xx = 0
total = 0
firstdate = ""
lastdate = ""
files={}
dates={
	"Oct":[],
	"Nov":[],
	"Dec":[],
	"Jan":[],
	"Feb":[],
	"Mar":[],
	"Apr":[],
	"May":[],
	"Jun":[],
	"Jul":[],
	"Aug":[],
	"Sep":[],
}

fh = open(file_name)
for line in fh:
	#splits line into a list
	breakup = line.split()
	if len(breakup) >= 10:
		monthsplit=line.split('/')
		#Firstdate should only update the first time around, 
		#Lastdate should update every time until the for loop ends
		if total >= 1:
			lastdate = breakup[3]
		elif total <= 0:
			firstdate = breakup[3]
		total += 1
		
		dates[monthsplit[1]].append(line)
		
		#adds 1 to 4xx or 3xx if 4 or 3 appear in the first spot in the second to last string
		breakup[6]
		if breakup[-2][0] == '4':
			code4xx += 1
		elif breakup[-2][0] == '3':
			code3xx += 1
		#checks if a file has already been made a key in the files dictionary
		#If it has it adds one to the value. If not it make the key and makes 1 the value
		if breakup[6] in files.keys():
			files[breakup[6]] += 1
		else:
			files[breakup[6]] = 1

for key in dates.keys():
	save_to_file(dates[key],key)
	
#removes open bracket
firstdate = firstdate.replace(firstdate[0],"")
lastdate = lastdate.replace(lastdate[0],"")
#removes colin
firstdate = firstdate.replace(":","/")
lastdate = lastdate.replace(":","/")
#sperates day month and year
firstdate = firstdate.split('/')
lastdate = lastdate. split('/')

totaldays = num_of_days(firstdate, lastdate)
avgdays = total/totaldays
avgweeks = total/(totaldays/7)
avgmonth = total/12

least_files=[]
most_files=[]
#find the min and max 
min = 9999
max = 0
for value in files.values():
	if value > max:
		max = value
	if value < min:
		min = value
##Since there maybe a tie in least or most any that qualify for either are added to a list.		
for key, value in files.items():
	if value == min:
		least_files.append(key)
	if value == max:
		most_files.append(key)

code4xx_per = code4xx/total*100
code3xx_per = code3xx/total*100

least_files_total = len(least_files)
		
print("1. Total requests made in the time period represented in the log: ",total)
print("2. Average requests made:\n","Per Day:",avgdays,"\n","Per Week:",avgweeks,"\n","Per Month:",avgmonth)
print("3. Percentage of requests that were not successful: ",code4xx_per,"%")
print("4. Percentage of requests that were redirected elsewhere: ",code3xx_per,"%")
print("5. The most requested files where:",most_files,"at",max,"requests.")
if least_files_total > 10:
	print("6.",least_files_total,"files were all request the least at",min,"time each.")
else:	
	print("6. The least requested files where:",least_files)
print("These results will be writen to a file name log_results.txt")

## write to log_results.write
log_results = open("log_results.txt", "w")
log_results.write("1. Total requests made in the time period represented in the log: %s\n" % total)
log_results.write("2. Average requests made:\nPer Day: %s\n" % avgdays)
log_results.write("Per Week: %s\n" % avgweeks)
log_results.write("Per Month: %s\n" % avgmonth)
log_results.write("3. Percentage of requests that were not successful: %s\n" % code4xx_per)
log_results.write("4. Percentage of requests that were redirected elsewhere: %s\n" % code3xx_per)
log_results.write("5. The most requested file was: %s " % most_files,)
log_results.write("at %s requests.\n" % max)
if least_files_total > 10:
	log_results.write("6. %s " % least_files_total)
	log_results.write("files were all requested the least at %s time each." % min)
else:
	log_results.write("6. The least requested files where: %s" % least_files)
