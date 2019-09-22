# psql -U postgres nevents
# http://www.postgresqltutorial.com/postgresql-python/connect/
# http://initd.org/psycopg/docs/errors.html

from __future__ import print_function
import psycopg2
from psycopg2 import Date
import re
from tabulate import tabulate

# ----------------------------------------------------------------------------------------------
# HELPER METHOD:
# Description:
#		1. split_date(time): Use reggex to split year/month/day in the input
#		2. bar_plot(data): Create bar plot report 
#		3. suggested_id(entity,name): Suggest ID for list of item with the similar input name (allow a few mispellings)
#		4. view_given_item(entity,item_ID): View all information of a item with the given ID
#		5. view_options(input): Print an option menu + Return the response from user
# ----------------------------------------------------------------------------------------------
# 1. split_date(time): Use reggex to split year/month/day in the input
def split_date(time):
	result = []
	split = re.match(r"(\d\d\d\d)/(\d\d)/(\d\d)",time)
	split_time = split.groups()
	result.append(int(split_time[0]))
	result.append(int(split_time[1]))
	result.append(int(split_time[2]))
	return result

# 2. bar_plot(data): Create bar plot report 
def bar_plot(data):
	max_length = max(len(name) for name, _ in data)
	for name, value in data:
		bar = '|' * (abs(int(value)) // 1000)
		print(name + (' ' * (5 + max_length - len(name)))  + bar)

# 3. suggested_id(view_set,name): Suggest ID for list of item with the similar input name (allow a few mispellings)
def suggested_id(view_set,name):
	print('----------------------')
	cursor.execute("""
		SELECT * FROM %s
		WHERE name %% '%s'
	""" % (view_set,name))
	data = cursor.fetchall()
	if len(data)>0:
		print('List of suggested %s with given name %s: ' % (view_set,name))
		beauty_print(view_set,data)
	else: 
		print('There is no matching record')
		return 0
	print('----------------------')

# 4. view_given_item(entity,item_ID): View all information of a item with the given ID
def view_given_item(view_set,item_id):
	cursor.execute("""
		SELECT * FROM %s
		WHERE id = %s
	""" % (view_set,item_id))
	data = cursor.fetchall()
	if len(data)>0:
		beauty_print(view_set,data)
	else: 
		print('There is no matching record')
		return 0
	print('----------------------')

# 5. view_options(input): Print an option menu + Return the response from user
def view_options(req):
	print('--------------------------')
	if req == 'FULL':
		print('Menu: ',
			'1. Campaigns = record of campaigns info',
			'2. Events = record of events info',
			'3. Members = record of members info',
			'4. Sponsor = record of sponsors info',
			'5. Donate = record of in-flow transactions',
			'6. Paid = record of out-flow transactions',
			'7. Participate = record of member''s activity history', sep = '\n')
		view_set = input('Please choose a section (1/2/3/4/5/6/7): ')
		print('----------------------')
		if view_set == '1':
			return('Campaigns')
		elif view_set == '2':
			return('Events')
		elif view_set == '3':
			return('Members')
		elif view_set == '4':
			return('Sponsor')
		elif view_set == '5':
			return('Donate')
		elif view_set == '6':
			return('Paid')
		elif view_set == '7':
			return('Participate')
		else:
			print('Wrong input!')
			return 0

	elif req == 'entity':
		print('Menu: ',
			'1. Campaigns = record of campaigns info',
			'2. Events = record of events info',
			'3. Account = record of all transaction history', 
			'4. Members = record of members info',
			'5. Sponsor = record of sponsors info', sep = "\n")
		view_set = input('Please choose a section (1/2/3/4/5): ')
		print('----------------------')
		if view_set == '1':
			return('Campaigns')
		elif view_set == '2':
			return('Events')
		elif view_set == '3':
			return('Account')
		elif view_set == '4':
			return('Members')
		elif view_set == '5':
			return('Sponsor')
		else:
			print('Wrong input!')
			return 0

	elif req == 'time':
		print('Menu: ',
			'1. Campaigns = record of campaigns info',
			'2. Events = record of events info',
			'3. Account = record of all transaction history', sep = "\n")
		view_set = input('Please choose a section (1/2/3): ')
		print('----------------------')
		if view_set == '1':
			return('Campaigns')
		elif view_set == '2':
			return('Events')
		elif view_set == '3':
			return('Account')
		else:
			print('Wrong input!')
			return 0

	elif req == 'modify':
		print('Menu: ',
			'1. Campaigns = record of campaigns info',
			'2. Events = record of events info',
			'3. Members = record of members info',
			'4. Sponsor = record of sponsors info', sep = "\n")
		view_set = input('Please choose a section (1/2/3/4): ')
		print('----------------------')
		if view_set == '1':
			return('Campaigns')
		elif view_set == '2':
			return('Events')
		elif view_set == '3':
			return('Members')
		elif view_set == '4':
			return('Sponsor')
		else:
			print('Wrong input!')
			return 0

	
# 6. beauty_print(view_set,data): Print the data properly (spacing,header)
def beauty_print(view_set,data):
	if view_set == 'Campaigns':
		header_set = ['ID', 'NAME', 'CONCEPT', 'START DATE', 'END DATE']
	elif view_set == 'Account':
		header_set = ['ID', 'AMOUNT', 'BALANCE', 'TIME']
	elif view_set == 'Sponsor':
		header_set = ['ID', 'NAME', 'PHONE', 'COMPANY']
	elif view_set == 'Events':
		header_set = ['ID', 'PLACE', 'TYPE', 'START DATE', 'END DATE']
	elif view_set == 'Members':
		header_set = ['ID', 'NAME', 'PHONE', 'BIRTHDAY', 'HOMETOWN', 'COUNTS', 'DEPARTMENT', 'TIER']
	elif view_set == 'Paid':
		header_set = ['EVENT ID', 'AMOUNT', 'NOTICE']
	elif view_set == 'Participate':
		header_set = ['CAMP ID', 'CAMP NAME', 'MEM ID', 'MEM NAME', 'EVALUATION']
	elif view_set == 'Has':
		header_set = ['CAMP ID', 'CAMP NAME', 'EVENT ID']
	elif view_set == 'Donate':
		header_set = ['SPONSOR ID', 'SPONSOR NAME', 'AMOUNT']
	elif view_set == 'Report':
		header_set = ['ID', 'NAME', 'TOTAL']
	else:
		return	
	if len(data) > 0:
		print(tabulate(data, headers=header_set, tablefmt = "psql"))		
	else:
		print('There is no matching record')


# ----------------------------------------------------------------------------------------------
# TASK 1: VIEW DATA
# Description: 
# 1. view_all: Show all items in a set
# 2. view_last_updated: Show the last 10 updated items in a set
# 3. view_specific_time: Show all items of a set in the specific period of time
# 4. view_custom: Allow users to enter their own queries
# ----------------------------------------------------------------------------------------------
# 1. view_all: Show all items in a set
def view_all(entity):
	print('----------------------')
	print('Table %s:' % entity) 
	cursor.execute("""
		SELECT * FROM %s
	""" % (entity))
	data = cursor.fetchall()
	beauty_print(entity,data)

# 2. view_last_updated: Show the last 10 updated items in a set
def view_last_updated():
	view_set = view_options('entity')
	if view_set == 0: return
	print('----------------------')
	print('Last 10 items updated to %s' % view_set) 
	cursor.execute("""
		SELECT * FROM %s
		WHERE id in (SELECT id FROM %s ORDER BY id DESC LIMIT 10 ) 
		ORDER BY id
	""" % (view_set,view_set))
	data = cursor.fetchall()
	beauty_print(view_set,data)

# 3. view_specific_time: Show all items of a set in the specific period of time
def view_specific_time():
	view_set = view_options('time')
	if view_set == 0: return
	start_time = input('Please choose a start day (yyyy/mm/dd): ')
	end_time = input('Please choose an end day (yyyy/mm/dd): ')
	start_time = split_date(start_time)
	end_time = split_date(end_time)

	try:
		if view_set == 'Campaigns' or view_set == 'Events':
			cursor.execute("""
				SELECT *
				FROM %s 
				WHERE start_date >= %s AND end_date <= %s
			""" % (view_set,Date(start_time[0],start_time[1],start_time[2]),Date(end_time[0],end_time[1],end_time[2])))
	
		else:
			cursor.execute("""
				SELECT *
				FROM %s 
				WHERE trans_time >= %s AND trans_time <= %s
			""" % (view_set,Date(start_time[0],start_time[1],start_time[2]),Date(end_time[0],end_time[1],end_time[2])))
			
		print("--> All %s happening from %s to %s " % (view_set,str(start_time),str(end_time))) 
		data = cursor.fetchall()
		beauty_print(view_set,data)
	except psycopg2.DataError:
		print ("Data Error: e.g: Date type is invalid, etc")

# 4. view_custom: Allow users to enter their own queries
def view_custom():
	while True:
		view_set = view_options('FULL')
		print('--> Notice: You are only allowed to query SELECT in this task!!')
		request = input('Please input your query: ')
		if re.match(r"(?i)\W(CREATE|UPDATE|DELETE|DROP)\s",request): break
		try:
			cursor.execute(""" %s """ % request)
			print('Result: ') 
			data = cursor.fetchall()
			beauty_print(view_set,data)
		except psycopg2.ProgrammingError:
			print("Programming Error: e.g: table not found/already exists, syntax error in the SQL statement, wrong number of parameters specified, etc")
		finish = input('Do you want to retry (Y/N): ')
		if (finish == 'N'): break
		print('----------------------')

# ----------------------------------------------------------------------------------------------
# TASK 2: INSERT DATA
# Description: Allow users to add new item to any selected set
# ----------------------------------------------------------------------------------------------
def insertion(insertion_input):
	if insertion_input == 0: return
	print('Starting insert new item to %s' % insertion_input) 
	while True:
		print('----------------------')
		
		# 1. Campaigns
		if insertion_input == 'Campaigns':
			print('Please input the new campaign\'s infos: ')
			camp_name = input('1. Name = ')
			start_date = input('2. Start date (yyyy/mm/dd) = ')
			end_date = input('3. End date (yyyy/mm/dd) = ')
			camp_concept = input('4. Concept (Concert, Contest, Fair)= ')
			start_date = split_date(start_date)
			end_date = split_date(end_date)
			confirmation = input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Campaigns(name,concept,start_date,end_date) 
						VALUES (%s,%s,%s,%s)
					""" % (camp_name, camp_concept, Date(start_date[0],start_date[1],start_date[2]), Date(end_date[0],end_date[1],end_date[2])))
					print('%s added successfully' % camp_name)
				except psycopg2.DataError:
					print("DataError: There is error with data type.")
		
		# 2. Events
		if insertion_input == 'Events':
			print('Please input the new event''s infos: ')
			event_place = input('1. Place = ')
			event_type = input('2. Type of event (Main-event,Pop-up-event,Leaflet,Parade) = ')
			start_date = input('3. Start date (yyyy/mm/dd) = ')
			end_date = input('3. End date (yyyy/mm/dd) = ')
			start_date = split_date(start_date)
			end_date = split_date(end_date)
			confirmation = input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Events(place,types,start_date,end_date) 
						VALUES (%s,%s,%s,%s)
					""" % (event_place, event_type, Date(start_date[0],start_date[1],start_date[2]), Date(end_date[0],end_date[1],end_date[2])))
					print('Event added successfully. Now let''s add this event to a campaign')
					print('----------------------')
					camp_name = input('1. Campaign name: ')
					suggested_id('Campaigns', camp_name)
					camp_id = input('2. Campaign ID = ')
					cursor.execute(""" SELECT max(id) FROM Events """)
					row = cursor.fetchone()
					if (row is not None): event_id = row[0]
					cursor.execute(""" 
						INSERT INTO Has(camp_id,camp_name,event_id) 
						VALUES (%s,%s,%s)
					""" % (camp_id,camp_name,event_id))
					print('Event %s added successfully to campaign %s' % event_id,camp_name)
				except psycopg2.DataError:
					print("DataError: There is error with data type.")

		# 3. Members
		if insertion_input == 'Members':
			print('Please input the new member\'s infos: ')
			mem_name = input('1. Name = ')
			mem_phone = input('2. Phone = ')
			mem_birthday = input('3. Birthday (yyyy/mm/dd) = ')
			mem_hometown = input('4. Hometown = ')
			mem_department = input('5. Department (Marketing/Facility/Content/ER) = ')
			confirmation = input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Members(name,phone,birthday,hometown,department) 
						VALUES (%s,%s,%s,%s,%s)
					""" % (mem_name,mem_phone,mem_birthday,mem_hometown,mem_department))
					print('%s added successfully' % mem_name)
				except psycopg2.DataError:
					print("DataError: There is error with data type.")

		# 4. Sponsors
		if insertion_input == 'Sponsor':
			print('Please input the new sponsor\'s infos: ')
			spons_name = input('1. Name = ')
			spons_phone = input('2. Phone = ')
			spons_company = input('3. Company = ')
			confirmation = input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Sponsor(name,phone,company) 
						VALUES (%s,%s,%s)
					""" % (spons_name,spons_phone,spons_company))
					print('%s added successfully' % spons_name)
				except psycopg2.IntegrityError:
					print("IntegrityError: The selected ID of campaign is already existed")
		
		# 5. Donate
		if insertion_input == 'Donate':
			view_all('Sponsor')
			print('Please input the new donation\'s infos: ')
			spons_id = input('1. Sponsor ID = ')
			cursor.execute("""
				SELECT name FROM Sponsor
				WHERE id = %s
			""" % spons_id)
			data = cursor.fetchone()
			spons_name = data[0]
			amount = input('3. Amount = ')
			confirmation = input('Are you sure with your input (%s,%s,%s) (Y/N)? ' % (spons_id,spons_name,amount))
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Donate(sponsor_id,sponsor_name,amount) 
						VALUES (%s,'%s',%s)
					""" % (spons_id,spons_name,amount))
					print('Donation of %s added successfully' % spons_name)
				except psycopg2.IntegrityError:
					print("IntegrityError. eg: Value is not met the restriction (amount > 0)")
		
		# 6. Paid
		if insertion_input == 'Paid':
			print('Please input the new out-flow\'s infos: ')
			camp_name = input('1. Campaign name = ')
			if suggested_id('Campaigns', camp_name) == 0: return				
			camp_id = input ('2. Camp ID = ')
			print('All events related to campaign %s: ' % camp_id)
			cursor.execute("""
				SELECT * FROM Events
				WHERE id in (SELECT event_id FROM Has WHERE camp_id = %s)
			""" % camp_id)
			data = cursor.fetchall()
			beauty_print("Events",data)
			event_id = input('2. Event ID = ')
			amount = input('3. Amount < 0 (e.g: -100) = ')
			confirmation = input('Are you sure with your input: (%s,%s,%s) (Y/N)? ' % (camp_name,event_id,amount))
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Paid(event_id,amount) 
						VALUES (%s,%s)
					""" % (event_id,amount))
					print(dbconn.notices)
				except psycopg2.IntegrityError:
					print("IntegrityError. eg: Value is not met the restriction (amount < 0)")
		
		# 7. Particpate
		if insertion_input == 'Participate':
			print('Please input the new participation\'s infos: ')
			camp_name = input('1. Campaign name = ')
			if suggested_id('Campaigns', camp_name) == 0: return
			camp_id = input('2. Campaign ID = ')
			cursor.execute("""
				SELECT name FROM Campaigns
				WHERE id = %s
			""" % camp_id)
			data = cursor.fetchone()
			camp_name = data[0]
			mem_name = input('3. Member name = ')
			if suggested_id('Members', mem_name) == 0: return
			mem_id = input('4. Member ID = ')
			cursor.execute("""
				SELECT name FROM Members
				WHERE id = %s
			""" % mem_id)
			data = cursor.fetchone()
			mem_name = data[0]
			evaluation = input('5. Evaluation = ')
			confirmation = input('Are you sure with your input (%s,%s,%s,%s,%s) (Y/N): ' % (camp_name,camp_id,mem_name,mem_id,evaluation))
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						insert into Participate(camp_id,camp_name,mem_id,mem_name,evaluation) 
						values (%s,'%s',%s,'%s','%s')
					""" % (camp_id, camp_name, mem_id, mem_name, evaluation))
					print('Member %s added successfully to campaign %s' % (mem_name,camp_name))
				except psycopg2.IntegrityError:
					print("IntegrityError: The selected ID of campaign is already existed")

		finish = input('Do you want to continue inserting to %s (Y/N)? ' % insertion_input)
		if finish == 'N': break
			
# ----------------------------------------------------------------------------------------------
# TASK 3: UPDATE INFORMATION
# Description: Allow users to edit any specific information of a set's item
# ----------------------------------------------------------------------------------------------
def set_modify(modify_input):
	if modify_input == 'Campaigns':
		print('Updating CAMPAIGNS section.')
		while True:
			camp_name = input('Please input campaign name = ')
			if suggested_id('Campaigns', camp_name) == 0: break
			camp_id = input('Choose Campaign ID = ')
			if view_given_item('Campaigns', camp_id) == 0: break
			modify_column = input('Choose an information to modify (name/concept): ')
			if modify_column in ('name','concept'):
				modify_input = input('Please insert new campaign''s %s: ' % modify_column)
				try:
					cursor.execute("""
						UPDATE Campaigns
						SET %s = '%s'
						WHERE id = %s
					""" % (modify_column,modify_input,camp_id))
					print('Updating campaign successfully!')
					view_given_item('Campaigns', camp_id)
				except psycopg2.IntegrityError:
					print("IntegrityError. eg: The selected ID of campaign is not existed, wrong concept!")
			else:
				print('Wrong input!')
			finish = input('Do you want to continue modifying campaigns (Y/N)? ')
			if finish == 'N': break
					
	elif modify_input == 'Events':
		print('Updating EVENTS section.')
		while True:
			event_id = input('Please input ID of that event = ')
			if view_given_item('Events',event_id) == 0: break
			recheck = input('Is this your event you choose? (Y/N) ')
			if recheck == 'N': break
			modify_column = input('Choose an information to modify (place/types): ')
			if modify_column in ('place','types'):
				modify_input = input('Please insert new event''s %s: ' % modify_column)
				try:
					cursor.execute("""
						UPDATE Events
							SET %s = '%s'
							WHERE id = %s
						""" % (modify_column,modify_input,event_id))
					print('Updating event successfully!')
					view_given_item('Events', camp_id)
				except psycopg2.IntegrityError:
					print("IntegrityError. eg: The selected ID is not existed")
			else:
				print('Wrong input!')
			finish = input('Do you want to continue modifying events (Y/N)? ')
			if finish == 'N': break			
	
	elif modify_input == 'Members':
		print('Updating MEMBERS section.')
		while True:
			mem_name = input('Please input member name = ')
			if suggested_id('Members', mem_name) == 0: break
			mem_id = input('Choose Member ID = ')
			if view_given_item('Members', mem_id) == 0: break
			modify_column = input('Choose an information to modify (name/phone/hometown/department): ')
			if modify_column in ('name','phone','hometown','department'):
				modify_input = input('Please insert new member''s %s: ' % modify_column)
				try:
					cursor.execute("""
						UPDATE Members
						SET %s = '%s'
						WHERE id = %s
					""" % (modify_column,modify_input,mem_id))
					print('Updating member successfully!')
					view_given_item('Members', camp_id)
				except psycopg2.IntegrityError:
					print("IntegrityError: The selected ID is not existed")
			else:
				print('Wrong input!')
			finish = input('Do you want to continue modifying members (Y/N)? ')
			if finish == 'N': break

	elif modify_input == 'Sponsor':
		print('Updating SPONSOR section.')
		while True:
			spons_name = input('Please input sponsor name = ')
			if suggested_id('Sponsor', spons_name) == 0: break
			spons_id = input('Choose Sponsor ID = ')
			if view_given_item('Sponsor', spons_id) == 0: break
			modify_column = input('Choose an information to modify (name/phone/company): ')
			if modify_column in ('name','phone','company'):
				modify_input = input('Please insert new sponsor''s %s: ' % modify_column)
				try:
					cursor.execute("""
						UPDATE Sponsor
						SET %s = '%s'
						WHERE id = %s
					""" % (modify_column,modify_input,spons_id))
					print('Updating sponsor successfully!')
					view_given_item('Sponsor', spons_id)
				except psycopg2.IntegrityError:
					print("IntegrityError: The selected ID is not existed")
			else:
				print('Wrong input!')
			finish = input('Do you want to continue modifying sponsors (Y/N)? ')
			if finish == 'N': break

# ----------------------------------------------------------------------------------------------
# TASK 4: CREATE A REPORT
# Description: 
#	1. Campaign report:
#		 - State of campaign at a specific time
#	2. Member report:
#		 - General Information
#		 - History of activities
#	3. Account report (graphical + textual):
#		 a. In-flow and out-flow for a specific period of time 
#		 b. The total cost for each campaign
#		 c. The total donation for each donator
# ----------------------------------------------------------------------------------------------
# 1. Campaign report: State + Info of campaign at a specific time
def campaign_report():
	camp_name = input('Please input campaign name = ')
	suggested_id('Campaigns', camp_name)
	camp_id = input('Choose Campaign ID = ')
	print('Campaign report: ')
	view_given_item('Campaigns', camp_id)
	print('State of this campaign: ')
	print('1. Events: ')
	cursor.execute("""
		SELECT * FROM Events
		WHERE id IN (SELECT event_id FROM Has
		WHERE camp_id = %s)
	""" % (camp_id))
	data = cursor.fetchall()
	beauty_print('Events',data)
	print('2. Members participate: ')
	cursor.execute("""
		SELECT * FROM Members
		WHERE id IN (SELECT mem_id FROM Participate
		WHERE camp_id = %s)
	""" % (camp_id))
	data = cursor.fetchall()
	beauty_print('Members',data)			
	print('3. Cost: ')
	cursor.execute("""
		SELECT * FROM Paid
		WHERE event_id IN (SELECT event_id FROM Has WHERE camp_id = %s)
	""" % (camp_id))
	data = cursor.fetchall()
	beauty_print('Paid',data)	
	cursor.execute("""
		SELECT sum(amount) FROM Paid
		WHERE event_id IN (SELECT event_id FROM Has WHERE camp_id = %s)
		AND notice = 'VALID'
	""" % (camp_id))
	data = cursor.fetchone()					
	print('Total cost: %s' % data)

#	2. Member report: General Information + History of activities
def member_report():
	mem_name = input('Please input the member name to report: ')
	suggested_id('Members', mem_name)
	mem_id = input('Please select that member ID = ')
	print('Member report: ')
	view_given_item('Members', mem_id)
	print('Activities history of this member: ')
	try:
		cursor.execute("""
			SELECT * FROM Participate where mem_id = %s
		""" % (mem_id))
		data = cursor.fetchall()
		beauty_print('Participate',data)
	except psycopg2.IntegrityError:
		print ("IntegrityError. eg: The selected ID is not exist")
	except psycopg2.DataError:
		print ("DEBUG data error")

#	3. Account report (graphical + textual):
#		 a. In-flow and out-flow for a specific period of time 
#		 b. The total cost for each campaign
#		 c. The total donation for each donator		
def account_report():
	print('----------------------')
	print('Option: ',
		'1. Report the cost of every campaigns',
		'2. Report the donation of every donators', 
		'3. Report in/out flow for a specific period of time', sep = '\n')
	report_request = input('Please choose your report type (1/2/3): ')
	print('----------------------')

	# Report cost of campaigns
	if report_request == '1':
		print('This is the report for the cost of each campaigns')
		cursor.execute("""
			SELECT C.id, C.name, TEMP.total 
			FROM Campaigns C, (SELECT H.camp_id id, sum(P.amount) total
						FROM Has H INNER JOIN Paid P ON H.event_id = P.event_id
						WHERE P.notice = 'VALID' GROUP BY H.camp_id ) TEMP
			where C.id = TEMP.id
		""")
		data = cursor.fetchall()
		data_numeric = []
		print('--> Textual report - total cost for each campaign: ')
		beauty_print('Report',data)
		for row in data:
			data_numeric.append((row[1],int(row[2])))
		print('--> Graph report - total cost for each campaign: ')
		bar_plot(data_numeric)
					
	# Report donation by sponsors 
	elif report_request == '2':
		print('This is the report for the donation by sponsors')
		cursor.execute("""
			SELECT S.id, S.name, TEMP.total 
			FROM Sponsor S, (SELECT sponsor_id id, sum(amount) total
						FROM Donate D GROUP BY sponsor_id) TEMP
			where S.id = TEMP.id
		""")
		data = cursor.fetchall()
		data_numeric = []
		print('--> Textual report - total donation for each donator: ')
		beauty_print('Report',data)
		for row in data:
			data_numeric.append((row[1],int(row[2])))
		print('--> Graph report - total donation for each donator: ')
		bar_plot(data_numeric)
		
	# Report in/outflow for a specific period of time
	elif report_request == '3':
		start_time = input('What is the start time for the report (yyyy/mm/dd): ')
		end_time = input('What is the end time for the report (yyyy/mm/dd): ')
		print('-----------------------')
		print('This is the report for the period from %s to %s: ' % (start_time,end_time))

		start_time = split_date(start_time)
		end_time = split_date(end_time)
		
		# Textual report:
		print('--> Textual report:')
		print('In-flow: ')
		cursor.execute("""
			SELECT * 
			FROM Account
			WHERE trans_time >= %s AND trans_time <= %s AND amount > 0
		""" % (Date(start_time[0],start_time[1],start_time[2]), Date(end_time[0],end_time[1],end_time[2])))
		data = cursor.fetchall()
		beauty_print('Account',data)
		in_flow = 0
		for line in data:
			in_flow += line[1]
		print("-> Total in-flow: " + str(in_flow))
		
		print('Out-flow: ')
		cursor.execute("""
			SELECT * 
			FROM Account
			WHERE trans_time >= %s AND trans_time <= %s AND amount < 0
		""" % (Date(start_time[0],start_time[1],start_time[2]), Date(end_time[0],end_time[1],end_time[2])))
		data = cursor.fetchall()
		beauty_print('Account',data)
		out_flow = 0
		for line in data:
			out_flow += line[1]
		print("-> Total out-flow: " + str(out_flow))
		
		# Graphical report: Plotting ASCII graph
		print("\n--> Graph report: ")
		data = [('in_flow', in_flow), ('out_flow', abs(out_flow))]
		bar_plot(data)
	
	else:
		print('Invalid activity!')

# ----------------------------------------------------------------------------------------------
# MAIN PROGRAM
# Description: Receive the request from the customers
# ----------------------------------------------------------------------------------------------			
def main():
	while True:	
		print('----------------------')
		print('Menu: ',
				'1. View data',
				'2. Insert new input to database',
				'3. Edit information in database',
				'4. Create a report',
				'F. Finish', sep = "\n")
		request = input('Please choose an activity (1/2/3/4/F): ')

		print('----------------------')
		
		if request == '1':
			print('Menu: ',
				'1. View all items in a set',
				'2. View the last 10 updated items in a chosen set',
				'3. View all items in the specific period of time',
				'4. View custom - input your own query',sep = "\n")
			view_set = input('Please choose a type of data view (1/2/3/4): ')
			if view_set == '1':
				view_input = view_options('FULL')
				view_all(view_input)
			elif view_set == '2':
				view_last_updated()
			elif view_set == '2':
				view_specific_time()
			elif view_set == '3':
				view_custom()
			else:
				print('Wrong input!')

		elif request == '2':
			insertion_input = view_options('FULL')
			insertion(insertion_input)
	
		elif request == '3':
			modify_input = view_options('modify')
			set_modify(modify_input)
			
		elif request == '4':
			print('Menu: ',
				'1. Summary of Campaigns record',
				'2. Summary of Members info and history activities',
				'3. Summary of Account (cost/donation)',sep = "\n")
			report_input = input('Please choose a report (1/2/3): ')
			if report_input == '1':
				campaign_report()
			elif report_input == '2':
				member_report()
			elif report_input == '3':
				account_report()

		elif request == 'F':
			break
	
		else:
			print('--> Invalid activity!!')

# ----------------------------------------------------------------------------------------------
# CONNECTION
# Description: Set up connection, cursor and handle connection error
# ----------------------------------------------------------------------------------------------
try:
	#dbconn = psycopg2.connect(host='studsql.csc.uvic.ca', user='vistula', password='&;8QEE&&Ar')
	print('Connecting to the PostgreSQL database...')
	dbconn = psycopg2.connect(host="localhost", database="nevents", user="postgres", password="dung104.")
	cursor = dbconn.cursor()
	if __name__ == "__main__": main()
	dbconn.commit()
	print('Transaction committed successfully')
except (Exception, psycopg2.DatabaseError) as error :
    print ("Error in connection/transaction. Reset all the transaction to the original \n", error)
    dbconn.rollback()
finally:
	cursor.close()
	dbconn.close()
	print('PostgreSQL connection closed')
