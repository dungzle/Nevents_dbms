#!/usr/bin/env python3
# https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL
import psycopg2
from psycopg2 import Date
import re
import pprint

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

# 3. suggested_id(entity,name): Suggest ID for list of item with the similar input name (allow a few mispellings)
def suggested_id(entity,name):
	print('----------------------')
	print('List of suggested %s with given name %s: ' % (entity,name))
	cursor.execute("""
		SELECT * FROM %s
		WHERE name % %s
	""", [entity,name])
	data = cursor.fetchall()
	pprint.pprint(data)
	print('----------------------')

# 4. view_given_item(entity,item_ID): View all information of a item with the given ID
def view_given_item(entity,item_id):
	cursor.execute("""
		SELECT * FROM %s
		WHERE id = %s
	""", [entity,item_id])
	data = cursor.fetchone()
	if data is not NONE:
		pprint.pprint(data)

# 5. view_options(input): Print an option menu + Return the response from user
def view_options(input):
	if input = 'regular':
		print('Menu: ',
			'1. Campaigns = record of campaigns info',
			'2. Events = record of events info',
			'3. Members = record of members info',
			'4. Sponsor = record of sponsors info',
			'5. Donate = record of in-flow transactions',
			'6. Paid = record of out-flow transactions',
			'7. Participate = record of member''s activity history', sep = "\n")
		view_input = raw_input('Please choose a section (1/2/3/4/5/6/7): ')
		if view_input = '1':
		return 'Campaigns'
		elif view_input = '2':
			return 'Events'
		elif view_input = '3':
			return 'Members'
		elif view_input = '4':
			return 'Sponsor'
		elif view_input = '5':
			return 'Donate'
		elif view_input = '6':
			return 'Paid'
		elif view_input = '7':
			return 'Participate'
		else:
			print('Wrong input!')
			return 0

	elif input = 'time':
		print('Menu: ',
			'1. Campaigns = record of campaigns info',
			'2. Events = record of events info',
			'3. Account = record of all transaction history', sep = "\n")
		view_input = raw_input('Please choose a section (1/2/3): ')
		if view_input = '1':
			return 'Campaigns'
		elif view_input = '2':
			return 'Events'
		elif view_input = '3':
			return 'Account'
		else:
			print('Wrong input!')
			return 0
	

# ----------------------------------------------------------------------------------------------
# TASK 1: VIEW DATA
# Description: 
# 1. view_last_updated: Show the last 10 updated items in a set
# 2. view_specific_time: Show all items of a set in the specific period of time
# ----------------------------------------------------------------------------------------------

# 1. view_last_updated: Show the last 10 updated items in a set
def view_last_updated():
	view_input = view_options('regular')
	print('----------------------')
	print('Last 10 items updated to %s' % view_input) 
	cursor.execute("""
		SELECT *
		FROM %s
		ORDER BY id DESC
		LIMIT 10
	""")
	data = cursor.fetchall()
	pprint.pprint(data)

# 2. view_specific_time: Show all items of a set in the specific period of time
def view_specific_time():
	view_input = view_options('time')
	if view_input == 0: return
	start_time = raw_input('Please choose a start day (yyyy/mm/dd): ')
	end_time = raw_input('Please choose an end day (yyyy/mm/dd): ')
	start_time = split_date(start_time)
	end_time = split_date(end_time)

	try:
		if view_input == 'Campaigns' or view_input == 'Events':
			cursor.execute("""
				SELECT *
				FROM %s 
				WHERE start_date >= %s AND end_date <= %s
			""", [Date(start_time[0],start_time[1],start_time[2]),Date(end_time[0],end_time[1],end_time[2])])
	
		else:
			cursor.execute("""
				SELECT *
				FROM %s 
				WHERE trans_time >= %s AND trans_time <= %s
			""", [Date(start_time[0],start_time[1],start_time[2]),Date(end_time[0],end_time[1],end_time[2])])
			
		print "--> All %s happening from %s to %s " % (view_input,str(start_time),str(end_time)) 
		data = cursor.fetchall()
		pprint.pprint(data)
	
	except psycopg2.ProgrammingError, pe:
		print ("DEBUG programming error")
	except psycopg2.DataError, de:
		print ("DEBUG data error")

# ----------------------------------------------------------------------------------------------
# TASK 2: INSERT DATA
# Description: Allow users to add new item to any selected set
# ----------------------------------------------------------------------------------------------
def insertion(insertion_input):
	print('Starting insert new item to %s' % insertion_input) 
	while True:
		print('----------------------')
		
		# 1. Campaigns
		if insertion_input == 'Campaigns':
			print('Please input the new campaign\'s infos: ')
			camp_name = raw_input('1. Name = ')
			start_date = raw_input('2. Start date (yyyy/mm/dd) = ')
			end_date = raw_input('3. End date (yyyy/mm/dd) = ')
			camp_concept = raw_input('4. Concept = ')
			start_date = split_date(start_date)
			end_date = split_date(end_date)
			confirmation = raw_input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Campaigns(name,concept,start_date,end_date) 
						VALUES (%s,%s,%s,%s)
					""", [camp_name, camp_concept, Date(start_date[0],start_date[1],start_date[2]), Date(end_date[0],end_date[1],end_date[2])])
					print('%s added successfully' % camp_name)
				except psycopg2.IntegrityError, ie:
					print("IntegrityError: The selected ID of campaign is already existed")
		
		# 2. Events
		if insertion_input == 'Events':
			print('Please input the new event''s infos: ')
			event_place = raw_input('1. Place = ')
			event_type = raw_input('2. Type of event (Main-event,Pop-up-event,Leaflet,Parade) = ')
			start_date = raw_input('3. Start date (yyyy/mm/dd) = ')
			end_date = raw_input('3. End date (yyyy/mm/dd) = ')
			start_date = split_date(start_date)
			end_date = split_date(end_date)
			confirmation = raw_input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Events(place,types,start_date,end_date) 
						VALUES (%s,%s,%s,%s)
					""", [event_place, event_type, Date(start_date[0],start_date[1],start_date[2]), Date(end_date[0],end_date[1],end_date[2])])
					print('Event added successfully. Now let''s add this event to a campaign')
					print('----------------------')
					camp_name = raw_input('1. Campaign name: ')
					suggested_id('Campaigns', camp_name)
					camp_id = raw_input('2. Campaign ID = ')
					cursor.execute(""" SELECT max(id) FROM Events """)
					row = cursor.fetchone()
					if (row is not None): event_id = row[0]
					cursor.execute(""" 
						INSERT INTO Has(camp_id,camp_name,event_id) 
						VALUES (%s,%s,%s)
					""", [camp_id,camp_name,event_id])
					print('Event %s added successfully to campaign %s' % event_id,camp_name)
				except psycopg2.IntegrityError, ie:
					print("IntegrityError: The selected ID of campaign is already existed")
		
		# 3. Members
		if insertion_input == 'Members':
			print('Please input the new member\'s infos: ')
			mem_name = raw_input('1. Name = ')
			mem_phone = raw_input('2. Phone = ')
			mem_birthday = raw_input('3. Birthday (yyyy/mm/dd) = ')
			mem_hometown = raw_input('4. Hometown = ')
			mem_department = raw_input('5. Department (Marketing/Facility/Content/ER) = ')
			confirmation = raw_input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Members(name,phone,birthday,hometown,department) 
						VALUES (%s,%s,%s,%s,%s)
					""", [mem_name,mem_phone,mem_birthday,mem_hometown,mem_department])
					print('%s added successfully' % mem_name)
				except psycopg2.IntegrityError, ie:
					print("IntegrityError: The selected ID of campaign is already existed")
		
		# 4. Sponsors
		if insertion_input == 'Sponsors':
			print('Please input the new sponsor\'s infos: ')
			spons_name = raw_input('1. Name = ')
			spons_phone = raw_input('2. Phone = ')
			spons_company = raw_input('3. Company = ')
			confirmation = raw_input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Sponsor(name,phone,company) 
						VALUES (%s,%s,%s)
					""", [spons_name,spons_phone,spons_company])
					print('%s added successfully' % spons_name)
				except psycopg2.IntegrityError, ie:
					print("IntegrityError: The selected ID of campaign is already existed")
		
		# 5. Donate
		if insertion_input == 'Donate':
			view_last_updated('Sponsor')
			print('Please input the new donation\'s infos: ')
			spons_name = raw_input('1. Sponsor name = ')
			spons_id = raw_input('2. Sponsor ID = ')
			amount = raw_input('3. Amount = ')
			confirmation = raw_input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Donate(sponsor_id,sponsor_name,amount) 
						VALUES (%s,%s,%s)
					""", [spons_id,spons_name,amount])
				except psycopg2.IntegrityError, ie:
					print("IntegrityError: The selected ID of campaign is already existed")
		
		# 6. Paid
		if insertion_input == 'Paid':
			print('Please input the new out-flow\'s infos: ')
			camp_name = raw_input('1. Campaign name = ')
			print('All events related to campaign %s: ' % camp_name)
			cursor.execute("""
				SELECT * FROM Events
				WHERE id in (SELECT id FROM Has WHERE camp_name = %s)
			""",[camp_name])
			data = cursor.fetchall()
			pprint.pprint(data)
			event_id = raw_input('2. Event ID = ')
			amount = raw_input('3. Amount < 0 (e.g: -100) = ')
			confirmation = raw_input('Are you sure with your input?\n(%s,%s,%s)\n (Y/N): ' % (camp_name,event_id,amount))
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						INSERT INTO Paid(event_id,amount) 
						VALUES (%s,%s)
					""",[event_id,amount])
				except psycopg2.IntegrityError, ie:
					print("IntegrityError: The selected ID of campaign is already existed")
		
		# 7. Particpate
		if insertion_input == 'Participate':
			print('Please input the new participation\'s infos: ')
			camp_name = raw_input('1. Campaign name = ')
			suggested_id('Campaigns', camp_name)
			camp_id = raw_input('2. Campaign ID = ')
			mem_name = raw_input('3. Member name = ')
			suggested_id('Members', mem_name)
			mem_id = raw_input('4. Member ID = ')
			evaluation = raw_input('5. Evaluation = ')
			confirmation = raw_input('Are you sure with your input?\n(%s,%s,%s,%s,%s)\n (Y/N): ' % (camp_name,camp_id,mem_name,mem_id,evaluation))
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						insert into Participate(camp_id,camp_name,mem_id,mem_name,evaluation) 
						values (%s,%s,%s,%s,%s)
					""", [camp_name, camp_id, mem_name, mem_id, evaluation])
					print('Member %s added successfully to campaign %s' % (mem_name,camp_name))
				except psycopg2.IntegrityError, ie:
					print("IntegrityError: The selected ID of campaign is already existed")
			
# ----------------------------------------------------------------------------------------------
# TASK 3: UPDATE INFORMATION
# Description: Allow users to edit any specific information of a set's item
# ----------------------------------------------------------------------------------------------
def set_modify(modify_input):
	if modify_input = 'Campaigns':
		print('Updating CAMPAIGNS section.')
		while TRUE:
			camp_name = raw_input('Please input campaign name = ')
			suggested_id('Campaigns', camp_name)
			camp_id = raw_input('Choose Campaign ID = ')
			view_given_item('Campaigns', camp_id)
			print('Menu: ',
					'1. Campaign name',
					'2. Campaign concept')
			modify_column = raw_input('Choose an information to modify (name/concept): ')
			if modify_column in ('name','concept'):
				modify_input = raw_input('Please insert new campaign''s %s: ' % modify_column)
				try:
					cursor.execute("""
						UPDATE Campaigns
						SET %s = %s
						WHERE id = %s
					""", [modify_column,modify_input,camp_id])
				except psycopg2.DataError:
					print("IntegrityError: The selected ID of campaign is already existed")
					
	elif modify_input = 'Events':
		print('Updating EVENTS section.')
		camp_name = raw_input('Please input campaign name of that event = ')
	
	elif modify_input = 'Members':
		print('Updating MEMBERS section.')
		mem_name = raw_input('Please input member name = ')
		suggested_id('Members', mem_name)
		camp_id = raw_input('Choose Member ID = ')
		view_given_item('Members', mem_id)
		modify_column = raw_input('Choose an information to modify (name,phone,birthday,department: ')
		if modify_column in ('name','phone','birthday','hometown','department'):
		modify_input = raw_input('Please insert new member''s %s: ' % modify_column)
			try:
				cursor.execute("""
					UPDATE Members
					SET %s = %s
					WHERE id = %s
				""", [modify_column,modify_input,mem_id])
			except psycopg2.DataError:
				print("IntegrityError: The selected ID of campaign is already existed")

	elif modify_input = 'Sponsor':
		print('Updating SPONSOR section.')
		spons_name = raw_input('Please input sponsor name = ')
		suggested_id('Sponsors', spons_name)
		spons_id = raw_input('Choose Sponsor ID = ')
		view_given_item('Sponsors', spons_id)
		modify_column = raw_input('Choose an information to modify: ')
		if modify_column in ('name','phone','company'):
		modify_input = raw_input('Please insert new sponsor''s %s: ' % modify_column)
			try:
				cursor.execute("""
					UPDATE Sponsors
					SET %s = %s
					WHERE id = %s
				""", [modify_column,modify_input,spons_id])
			except psycopg2.DataError:
				print("IntegrityError: The selected ID of campaign is already existed")
	
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
	camp_name = raw_input('Please input campaign name = ')
	suggested_id('Campaigns', camp_name)
	camp_id = raw_input('Choose Campaign ID = ')
	view_given_item('Campaigns', camp_id)
	print('State of this campaign: ')
	print('----------------------')
	print('1. Events: ')
	cursor.execute("""
		SELECT * FROM Events
		WHERE id IN (SELECT event_id FROM Has
		WHERE camp_id = %s)
	""", [camp_id])
	data = cursor.fetchall()
	if data is None:
		print('There is no events in this campaign')
	else:
		pprint.pprint(data)

	print('----------------------')
		
	print('2. Members: ')
	cursor.execute("""
		SELECT * FROM Members
		WHERE mem_id IN (SELECT mem_id FROM Participate
		WHERE camp_id = %s)
	""", [camp_id])
	if data is None:
		print('There is no members in this campaign')
	else:
		pprint.pprint(data)						

	print('----------------------')

	print('3. Cost: ')
	cursor.execute("""
		SELECT * FROM Paid
		WHERE event_id IN (SELECT event_id FROM Has WHERE camp_id = %s)
	""", [camp_id])
	data = cursor.fetchall()
	if data is None:
		print('There is no transactions in this campaign')
	else:
		pprint.pprint(data)						

#	2. Member report: General Information + History of activities
def member_report():
	mem_name = raw_input('Please input the member name to report: ')
	suggested_id('Members', mem_name)
	mem_id = raw_input('Please select that member ID = ')
	view_given_item('Members', mem_id)
	print('Activities history of this member: ')
	try:
		cursor.execute("""
			SELECT * FROM Participate where mem_id = %s
		""", [mem_request_ID])
		data = cursor.fetchall()
		if data is None:
			print('There is no record of activities')
		else:
			pprint.pprint(data)
	except psycopg2.ProgrammingError, pe:
		print ("DEBUG programming error")
	except psycopg2.DataError, de:
		print ("DEBUG data error")

#	3. Account report (graphical + textual):
#		 a. In-flow and out-flow for a specific period of time 
#		 b. The total cost for each campaign
#		 c. The total donation for each donator		
def account_report():
	print('Option: 1. Report the cost of every campaigns, 2. Report the donation of every donators, 3. Report in/out flow for a specific period of time')
	report_request = raw_input('Please choose your report type (1/2/3): ')
	print('----------------------')

	# Report cost of campaigns
	if report_request == '1':
		cursor.execute("""
			SELECT C.name, TEMP.total 
			FROM Campaigns C, (SELECT H.camp_id, sum(P.amount) total
						FROM Has H INNER JOIN Paid P ON H.event_id = P.event_id
						GROUP BY H.camp_id HAVING P.notice = 'VALID') TEMP
			where C.camp_id = TEMP.camp_id
		""")
		data = []
		print('Textual report - total cost for each campaign: ')
		for row in cursor.fetchall():
			print ("%s %s" % (row[0], row[1]))
			data.append((row[0],int(row[1]))) 
		print('\nGraph report - total cost for each campaign: ')
		bar_plot(data)
					
	# Report inflow by sponsors 
	elif report_request == '2':
		cursor.execute("""
			SELECT S.name, TEMP.total 
			FROM Sponsors S, (SELECT spons_id, sum(amount) total
						FROM Donate D GROUP BY don_id) TEMP
			where S.id = TEMP.spons_id
		""")
		data = []
		print('Textual report - total donation for each donator: ')
		for row in cursor.fetchall():
			print ("%s %s" % (row[0], row[1]))
			data.append((row[0],abs(int(row[1])))) 
		print('\nGraph report - total donation for each donator: ')
		bar_plot(data)
		
	# Report in/outflow for a specific period of time
	elif report_request == '3':
		start_time = raw_input('What is the start time for the report (yyyy/mm/dd): ')
		end_time = raw_input('What is the end time for the report (yyyy/mm/dd): ')

		print('This is the report for the period from %s to %s: ', [start_time,end_time])

		start_time = split_date(start_time)
		end_time = split_date(end_time)
		
		# Textual report:
		print('In-flow: ')
		cursor.execute("""
			SELECT * 
			FROM Account
			WHERE trans_time >= %s AND trans_time <= %s AND amount > 0
		""", [Date(start_time[0],start_time[1],start_time[2]), Date(end_time[0],end_time[1],end_time[2])])
		data = cursor.fetchall()
		pprint.pprint(data)
		total = 0
		for line in data:
			total += line[1]
		print "-> Total in-flow: " + str(in_flow)
		
		print('Out-flow: ')
		cursor.execute("""
			SELECT * 
			FROM Account
			WHERE trans_time >= %s AND trans_time <= %s AND amount < 0
		""", [Date(start_time[0],start_time[1],start_time[2]), Date(end_time[0],end_time[1],end_time[2])])
		data = cursor.fetchall()
		pprint.pprint(data)
		total = 0
		for line in data:
			total += line[1]
		print "-> Total in-flow: " + str(total)
		
		# Graphical report: Plotting ASCII graph
		print "\nGraph report: "
		data = [('in_flow', in_flow), ('out_flow', abs(out_flow))]
		bar_plot(data)
	
	else:
		print('Invalid activity!')

# ----------------------------------------------------------------------------------------------
# Task 5: CUSTOM QUERY
# Description: Let the customers write their own query
# ----------------------------------------------------------------------------------------------
def custom_query():
	while True:
		request = raw_input('Please input your own query: ')
		try:
			cursor.execute(""" %s """, [request])
			print('Result: ') 
			for row in cursor.fetchall():
				print ("%s %s %s" % (row[0], row[1], row[2]))
		except psycopg2.ProgrammingError, ie:
			print("IntegrityError: The selected ID of post is already existed")
		finish = raw_input('Do you want to retry (Y/N): ')
		if (finish == 'N'): break
		print('----------------------')

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
				'C. Custom query',
				'F. Finish', sep = "\n")
		request = raw_input('Please choose an activity (1/2/3/4/C/F): ')

		print('----------------------')
		
		if request == '1':
			print('Menu: ',
				'1. View the last 10 updated items in a chosen set',
				'2. View all items in the specific period of time',
				'3. View cai gi do',sep = "\n")
			view_input = raw_input('Please choose a type of data view (1/2/3): ')
			if view_input = '1':
				view_last_updated()
			elif view_input = '2':
				view_specific_time()

		elif request == '2':
			insertion_input = view_options('regular')
			insertion(insertion_input)
	
		elif request == '3':
			modify_input = view_options('regular')
			set_modify(modify_input)
			
		elif request == '4':
			print('Menu: ',
				'1. Campaigns = record of campaigns info',
				'2. Members = record of members info',
				'3. Account = record of all inflow-outflow transactions) ',sep = "\n")
			report_input = raw_input('Please choose a report (1/2/3): ')
			if report_input = '1':
				report_campaign()
			elif report_input = '2':
				report_member()
			elif report_input = '3':
				report_account()
	
		elif request == 'C':
			custom_query()
	
		elif request == 'F':
			break
	
		else:
			print('Invalid activity')
			print('----------------------')

try:
	dbconn = psycopg2.connect(host='studsql.csc.uvic.ca', user='vistula', password='&;8QEE&&Ar')
	cursor = dbconn.cursor()
	if __name__ == "__main__": main()
	dbconn.commit()
	print('Transaction committed successfully')
except (Exception, psycopg2.DatabaseError) as error :
    print ("Error in transaction. Reset all the transaction to the original", error)
    dbconn.rollback()
finally:
	cursor.close()
	dbconn.close()
	print('PostgreSQL connection closed')