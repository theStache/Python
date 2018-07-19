#Need python 3.3 or higher for ipaddress module
#Helpful info - look at the python modules 'ipaddress' and 'collections', they may make life super easy.

import csv, ipaddress, collections
infile = path//to//file.csv


#1
# Given a list of known bad user account names, determine if any of these users are active during this collection.
# User Blacklist: kevind.d.mitnick, jonny.l.miller, Dade.ZeroCool.Murphy, Ramon.ThePhantomPhreak.Sanchez, Emmanuel.CerealKiller.Goldstein, Paul.LordNikon.Cook, Raymond.Red.Reddington
#Bonus - If there is a hit, what IP address did the user use to authenticate?
'''
blacklist = ['kevind.d.mitnick', 'jonny.l.miller', 'Dade.ZeroCool.Murphy', 'Ramon.ThePhantomPhreak.Sanchez', 'Emmanuel.CerealKiller.Goldstein', 'Paul.LordNikon.Cook', 'Raymond.Red.Reddington']
with open(infile) as f:
	reader = csv.DictReader(f)
		for row in reader:
			for x in blacklist:
				if x in row['USERNAME_TARGET']:
					print ("Found blacklist persona" row['USERNAME_TARGET']+" on IP :"+row['IP_WINDOWSEVENT'])
'''

#2
#Given the list of known good subnets, determine if any other IPs are active during this collection.
#Known good subnets 129.189.0.0/16,140.160.0.0/16,141.201.0.0/16
'''
whitelistSubnets = [ipaddress.IPv4Network('129.189.0.0/16'),ipaddress.IPv4Network('140.160.0.0/16'),ipaddress.IPv4Network('141.201.0.0/16')]
with open(infile) as f:
	reader = csv.DictReader(f)
		for row in reader:
			switchvar = False
			for net in whitelistSubnets:
				if ipaddress.IPv4Address(row['IP_WINDOWSEVENT']) in net:
					switchvar = True
					continue
				else:
					continue
				if swtichvar == False:
					print(row["IP_WINDOWSEVENT"] "found on the network outside of white list range")
'''

#3
#Given the collection time range, determine if any DTG have been altered.
#Collection time range 2018-04-04T00:00:00.00Z - 2018-04-06T00:00:00.000Z
#Bonus - If there is a discrepancy, what user was logged in?
'''
minDate = '2018-04-04T00:00:00.00Z'
maxDate = '2018-04-06T00:00:00.000Z'
with open(infile) as f:
	reader = csv.DictReader(f)
		for row in reader:
			if row["DATETIME_SYSTEMTIME_LOGSTART"] > maxDate or < minDate:
				print("possible time stomping : DTG" + row['DATETIME_SYSTEMTIME_LOGSTART'] +"Logged in user at this time is : "+ row['USERNAME_TARGET'])


				
'''

#4
#Determine who the top five users that utilize the smart card pre-authentication method.
#Pre-Authorization Type for smart card use is '15'
'''
with open(infile) as f:
	reader = csv.DictReader(f)
	newarray = []
		for row in reader:
			if row['PREAUTHTYPE'] == '15':
				newarray.append(row['PREAUTHTYPE'])
		counter = collections.counter(newarray)
		print(counter.most_common(5))
'''
					
					
					
