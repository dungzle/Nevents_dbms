# N-events Database Management System

This project includes database-tier and application-tier for the N-events organization's DBMS.
 
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- What things you need to install and how to install them:
	1. PostgreSQL 10
	2. Python 3 (packages: Psycopg2, RegEx, Tabulate)
```
1. PostgreSQL 10 (Windows): https://www.postgresql.org/download/windows/
2. Python 3: https://www.python.org/downloads/ 
	a) Installing pip: https://pip.pypa.io/en/stable/installing/
		python -m pip install -U pip
	b) Installing packages:
		pip install psycopg2
		pip install regex
		pip install tabulate
```

### Initalizing database-tier:
- How to initialize the PostgreSQL database on your local server
1. Go to the file project's location on your machine by using Command Prompt
2. Open PostgreSQL server on your machine, and input your password
3. Run the SQL file: "sql_project.sql"
4. You can modify the database on your own or exit and run the python file
```
1: cd Desktop/Project
2: psql -U postgres nevents
( then input your password )
3: \i sql_project.sql
4: \q
( exit server )
```

### Running the application-tier:
- Run the file: "sql_project.py" and try to interact with the program:
```
python sql_project.py
```

### Testing:
#### Testing Constraint:
	Input the data that conflict the constraints and see the errors:
	- Type: date, event type, campaigns concept
	- Value: paid amount < 0, paid amount < balance (if not: INVALID), donation amount > 0, End date > Start date
		
#### Testing Automatic Operations:
	- Update tiers of employees:
	( tiers will be automatically updated if his/her number of campaigns participation > 3 )
		Adding more activities to Participate of a member
		After having 3 campaigns, there is a notice to notify that he/she is promoted to new tier. And, you can check by using view function.
	- Add transaction to Account (record):
	( any new valid transaction adding to Donate/Paid will be added to Account for record automatically )
		Adding new items to Donate/Paid and use view Account to see the changed.

3. Testing trigram index against name:
	( it allows users to input the name with a few mispelling )
	- Adding new items to Events/Paid/Participate
	
## Authors
**Viet Dung, Le** - (https://github.com/dungzle)

## Acknowledgments
http://www.postgresqltutorial.com/postgresql-python/connect/ (space)
http://initd.org/psycopg/docs/errors.html (space)
https://pypi.org/project/tabulate/