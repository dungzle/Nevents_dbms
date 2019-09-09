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
#		3. suggested_id(entity,name): Suggest list of item with the similar name (allow a few mispellings)
#		4. view_given_item(entity,item_ID): View all information of a item with the given ID
# ----------------------------------------------------------------------------------------------
def split_date(time):
	result = []
	split = re.match(r"(\d\d\d\d)/(\d\d)/(\d\d)",time)
	split_time = split.groups()
	result.append(int(split_time[0]))
	result.append(int(split_time[1]))
	result.append(int(split_time[2]))
	return result

def bar_plot(data):
	max_length = max(len(name) for name, _ in data)
	for name, value in data:
		bar = '|' * (abs(int(value)) // 1000)
		print(name + (' ' * (5 + max_length - len(name)))  + bar)

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

def view_given_item(entity,item_id):
	cursor.execute("""
		SELECT * FROM %s
		WHERE id = %s
	""", [entity,item_id])
	data = cursor.fetchone()
	if data is not NONE:
		pprint.pprint(data)

def view_Has():


# ----------------------------------------------------------------------------------------------
# TASK 1: VIEW DATA
# Description: Show the last 10 items updated to a field
# ----------------------------------------------------------------------------------------------
def view_data(view_input):
	print('Last 10 items updated to %s' % view_input) 
	while True:
		print('----------------------')
		cursor.execute("""
			SELECT *
			FROM %s
			ORDER BY id DESC
			LIMIT 10
		""")
		data = cursor.fetchall()
		pprint.pprint(data)
			
# ----------------------------------------------------------------------------------------------
# TASK 2: INSERT DATA
# Description: Adding new item to a selected field
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
						insert into Campaigns(name,concept,start_date,end_date) 
						values (%s,%s,%s,%s)
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
						insert into Members(name,phone,birthday,hometown,department) 
						values (%s,%s,%s,%s,%s)
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
						insert into Sponsors(name,phone,company) 
						values (%s,%s,%s)
					""", [spons_name,spons_phone,spons_company])
					print('%s added successfully' % spons_name)
				except psycopg2.IntegrityError, ie:
					print("IntegrityError: The selected ID of campaign is already existed")
		
		# 5. Donate
		if insertion_input == 'Donate':
			print('Please input the new donation\'s infos: ')
			spons_name = raw_input('1. Sponsor name = ')
			spons_id = raw_input('2. Sponsor ID = ')
			amount = raw_input('3. Amount = ')
			confirmation = raw_input('Are you sure with your input (Y/N)? ')
			if confirmation == 'Y':
				try:
					cursor.execute(""" 
						insert into Donate(sponsor_id,sponsor_name,amount) 
						values (%s,%s,%s)
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
						insert into Paid(event_id,amount) 
						values (%s,%s)
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
# Description: 
#		1. Update general information (entity set's item)
#		2. Update activity/transaction (relationship's item)
# ----------------------------------------------------------------------------------------------
def entity_set_modify():
	print('Menu: ',
		'1. Campaigns = record of campaigns info',
		'2. Events = record of events info',
		'3. Members = record of members info',
		'4. Sponsor = record of sponsors info', sep = "\n")
	modify_input = raw_input('Please choose a section to modify (1/2/3/4): ')
	if modify_input = '1':
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
				modify_input = raw_input('Please insert new campaign %s: ' % modify_column)
				try:
					cursor.execute("""
						UPDATE Campaigns
						SET %s = %s
						WHERE id = %s
					""", [modify_column,modify_input,camp_id])
				except psycopg2.DataError:
					print("IntegrityError: The selected ID of campaign is already existed")
					
	elif modify_input = '2':
		print('Updating EVENTS section.')
		camp_name = raw_input('Please input campaign name of that event = ')
	
	elif modify_input = '3':
		print('Updating MEMBERS section.')
		mem_name = raw_input('Please input member name = ')
		suggested_id('Members', mem_name)
		camp_id = raw_input('Choose Member ID = ')
		view_given_item('Members', mem_id)
		modify_column = raw_input('Choose an information to modify: ')
	
	elif modify_input = '4':
		print('Updating SPONSOR section.')
		spons_name = raw_input('Please input sponsor name = ')
		suggested_id('Sponsors', spons_name)
		spons_id = raw_input('Choose Sponsor ID = ')
		view_given_item('Sponsors', spons_id)
		modify_column = raw_input('Choose an information to modify: ')
		
def relationship_modify():
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
def campaign_report():
	# Option 1: Show state of the campaign:
	if camp_request == '1':
		print('State of this campaign: ')
		print('1. Events: ')
		cursor.execute("""
			select * from Events
			where event_id in (select event_id from Has
			where camp_id = %s)
		""", [camp_request_ID])
		row = cursor.fetchone()
		if row is None:
			print('There is no events in this campaign')
		else:
			for row in cursor.fetchall():
				print ("%s %s %s %s" % (row[0], row[1], row[2], row[3]))
			
		print('2. Members: ')
			cursor.execute("""
				select * from Members
				where mem_id in (select mem_id from Participate
				where camp_id = %s)
			""", [camp_request_ID])
					for row in cursor.fetchall():
						print ("%s %s %s" % (row[0], row[1], row[2]))
							
					print('4. Transactions: ')
					cursor.execute("""
						select * from Account
						where trans_id in (select trans_id from Out_camps
										where camp_id = %s)
					""", [camp_request_ID])
					for row in cursor.fetchall():
						print ("%s %s %s" % (row[0], row[1], row[2]))

def account_report():
	print('Option: 1. Report the cost of every campaigns, 2. Report the donation of every donators, 3. Report in/out flow for a specific period of time')
	report_request = raw_input('Please choose your report type (1/2/3): ')
	print('----------------------')
	# Report outflow by campaigns
	if report_request == '1':
		cursor.execute("""
			select camp_name, total 
			from Campaigns C, (select camp_id, sum(trans_amount) total
						from Out_camps O Inner Join Account A on O.trans_id = A.trans_id
						group by camp_id) temp_total
			where C.camp_id = temp_total.camp_id
		""")
		data = []
		print('Textual report - total cost for each campaign: ')
		for row in cursor.fetchall():
			print ("%s %s" % (row[0], row[1]))
			data.append((row[0],int(row[1]))) 
		print('\nGraph report - total cost for each campaign: ')
		bar_plot(data)
					
	# Report inflow by donators 
	elif report_request == '2':
		cursor.execute("""
			select don_name, total 
			from Donator, (select don_id, sum(trans_amount) total
						from Donate D Inner Join Account A on D.trans_id = A.trans_id
			group by don_id) temp_total
			where Donator.don_id = temp_total.don_id
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
		
		# Textual report for inflow - outflow
		print('In-flow: ')
		cursor.execute("""
			select trans_id, trans_amount, trans_date 
			from Account
			where trans_date >= %s and trans_date <= %s and trans_amount > 0
		""", [Date(start_time[0],start_time[1],start_time[2]), Date(end_time[0],end_time[1],end_time[2])])
		for row in cursor.fetchall():
			print ("%s %s %s" % (row[0], row[1], row[2]))
		cursor.execute("""
			select sum(trans_amount) 
			from Account
			where trans_date >= %s and trans_date <= %s and trans_amount > 0
		""", [Date(start_time[0],start_time[1],start_time[2]), Date(end_time[0],end_time[1],end_time[2])])	
		row = cursor.fetchone()
		if row is not None:
			in_flow = row[0]
			print "-> Total in-flow: " + str(in_flow)
		
		print('Out-flow: ')
		cursor.execute("""
			select trans_id, trans_amount, trans_date 
			from Account
			where trans_date >= %s and trans_date <= %s and trans_amount < 0
		""", [Date(start_time[0],start_time[1],start_time[2]), Date(end_time[0],end_time[1],end_time[2])])
		for row in cursor.fetchall():
			print ("%s %s %s" % (row[0], row[1], row[2]))
		cursor.execute("""
			select sum(trans_amount) 
			from Account
			where trans_date >= %s and trans_date <= %s and trans_amount < 0
		""", [Date(start_time[0],start_time[1],start_time[2]), Date(end_time[0],end_time[1],end_time[2])])	
		row = cursor.fetchone()
		if row is not None:
			out_flow = row[0]
			print "-> Total out-flow: " + str(out_flow)
		
		# Plotting ASCII graph
		print "\nGraph report: "
		data = [('in_flow', in_flow), ('out_flow', abs(out_flow))]
		bar_plot(data)
	
	else:
		print('Invalid activity!')

def member_report():
	mem_request_name = raw_input('Please input the member name to report: ')
	mem_request_id = raw_input('Select member ID: ')
	try:
		cursor.execute("""
			select * from Members
			where mem_id = %s
		""", [mem_request_ID])
		row = cursor.fetchone()
		if row is None:
			print('There is no member with that ID')
		else:
			print('Option:\n1. View activity history, 2. Modify activities')
			member_request = raw_input('Please select your activity (1/2): ')
			print('----------------------')
			# View the record of this member
			if member_request == '1':
				print('1. Info: ')
				print("%s %s %s %s %s %s" % (row[0], row[1], row[2], row[3], row[4], row[5]))
				cursor.execute("""
					select camp_name, start_date, end_date
					from Participate P inner join Campaigns C on P.camp_id = C.camp_id 
					where mem_id = %s
				""", [mem_request_ID])
				print('2. History of activities: ')
				for row in cursor.fetchall():
					print ("%s %s %s" % (row[0], row[1], row[2]))
					
			# Modify the record
			elif member_request == '2':
				print('Option for modifying:\n1. Change name, 2. Change phone, 3. Change tier')
				member_modify_request = raw_input('Please select your activity (1/2/3): ')
				if member_modify_request == '1':
					member_new_name = raw_input('Please enter new name: ')
					cursor.execute("""
						update Members
						set mem_name = %s
						where mem_id = %s
					""", [member_new_name, mem_request_ID])

				elif member_modify_request == '2':
					member_new_phone = raw_input('Please enter new phone: ')
					cursor.execute("""
						update Members
						set mem_phone = %s
						where mem_id = %s
					""", [member_new_phone, mem_request_ID])

				elif member_modify_request == '3':
					cursor.execute("""
						select count(*) 
						from Participate 
						where mem_id = %s
					""", [mem_request_ID])	
					row = cursor.fetchone()
					if row is not None:
						print('Number of participated campaigns: ', int(row[0]))
					cursor.execute("""
						select mem_tiers 
						from Members 
						where mem_id = %s
					""", [mem_request_ID])
					row = cursor.fetchone()
					if row is not None:
						print('Current tier of this member: ', row[0])
					else:
						print('There is no tier for this member')
					member_new_tier = raw_input('Please enter new tier (volunteer 1/2): ')
					if member_new_tier == 'voluteer 1' or member_new_tier == 'volunteer 2':
						cursor.execute("""
							update Members
							set mem_tiers = %s
							where mem_id = %s
						""", [member_new_tier, mem_request_ID])
					else: print('Wrong input tier')
	except psycopg2.ProgrammingError, pe:
		print ("DEBUG programming error")
	except psycopg2.InternalError, ie:
		print ("There is internal error")

				
# ----------------------------------------------------------------------------------------------
# PHASE 5: NEW IDEAS 
# ----------------------------------------------------------------------------------------------		
# Control number of events are happening in a specific time, at same place
def event_concurrency():
	print('Options:\n1. List events at a time, 2. Change time of events, 3. Change place of events')
	event_request = raw_input('Please choose your activity (1/2/3): ')
	
	if event_request == '1':
		start_time = raw_input('Please choose a start day (yyyy/mm/dd): ')
		end_time = raw_input('Please choose an end day (yyyy/mm/dd): ')
		
		start_time = split_date(start_time)
		end_time = split_date(end_time)
		try:
			cursor.execute("""
				select event_id, place, start_time, end_time
				from Events 
				where start_time >= %s AND end_time <= %s
			""", [Date(start_time[0],start_time[1],start_time[2]),Date(end_time[0],end_time[1],end_time[2])])
			print "--> All events happening from " + str(start_time) + " to " + str(end_time) 
			for row in cursor.fetchall():
				print ("%s %s %s %s" % (row[0], row[1], row[2], row[3]))
		except psycopg2.ProgrammingError, pe:
			print ("DEBUG programming error")
		except psycopg2.DataError, de:
			print ("DEBUG data error")
	
	elif event_request == '2':
		event_id_request = raw_input('Please choose ID event to change time: ')
		start_time = raw_input('Please choose a start day (yyyy/mm/dd): ')
		end_time = raw_input('Please choose an end day (yyyy/mm/dd): ')
		
		start_time = split_date(start_time)
		end_time = split_date(end_time)
		try:
			cursor.execute("""
				update Events
				set start_time = %s, end_time = %s
				where event_id = %s
			""", [Date(start_time[0],start_time[1],start_time[2]),Date(end_time[0],end_time[1],end_time[2]), event_id_request])
		except psycopg2.DataError, de:
			print ("DEBUG data error")
		except psycopg2.IntegrityError, ie:
			print ("DEBUG constraint of the start time > end time")
	
	elif event_request == '3':
		event_id_request = raw_input('Please choose ID event to change place: ')
		event_place_request = raw_input('Please choose a place: ')
		try:
			cursor.execute("""
				update Events
				set place = %s
				where event_id = %s
			""", [event_place_request, event_id_request])	
		except psycopg2.InternalError, ie:
			print ("There is internal error")				

# ----------------------------------------------------------------------------------------------
# Task 4: CUSTOM QUERY
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
		finish = raw_input('Do you want to continue (Y/N): ')
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
				'1. View last 10 updated to a field',
				'2. Insert new input to database',
				'3. Edit information in database',
				'4. Create a report',
				'C. Custom query',
				'F. Finish', sep = "\n")
		request = raw_input('Please choose an activity (1/2/3/O/F): ')
		print('----------------------')
		if request == '2':
			print('Menu: ',
				'1. Campaigns = record of campaigns info',
				'2. Events = record of events info',
				'3. Members = record of members info',
				'4. Sponsor = record of sponsors info',
				'5. Donate = record of in-flow budget',
				'6. Paid = record of out-flow budget',
				'7. Participate = record of member''s activity history', sep = "\n")
			insertion_input = raw_input('Please choose a section to add new item (1/2/3/4/5/6/7): ')
			if insertion_input in ['1','2','3','4','5','6','7','8']:
				insertion(insertion_input)
		elif request == '3':
			campaign_modify()
		elif request == '4':
			print('Menu: ',
				'1. Campaigns',
				'2. Members',
				'3. Account',sep = "\n")
			report_input = raw_input('Please choose a report (1/2/3/4/5/6/7/8): ')
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
