CREATE DATABASE nevents;
CREATE EXTENSION pg_trgm;
----------------------------------------------------------------------------------------------------------------
-- ENTITY SETS:
-- 1. Campaigns = record of campaigns' info
-- 2. Account = record of successful transaction(donation/paid) history
-- 3. Events = record of events' info
-- 4. Members = record of members' info
-- 5. Sponsor = record of sponsors' info
----------------------------------------------------------------------------------------------------------------
drop table Campaigns cascade;
create table Campaigns (
  id  SERIAL,
  name   varchar(50) NOT NULL,
	concept varchar(40) check (concept in ('Concert', 'Contest', 'Fair')),
  start_date	date NOT NULL,
  end_date	date check (end_date > start_date),
	primary key(id,name)
);
----------------------------------------------------------------------------------------------------------------
drop table Account cascade;
create table Account (
  id 				SERIAL primary key,
  amount 			int check (amount + curr_bal > 0),
  curr_bal 		int default 0,
	trans_time 		timestamp without time zone DEFAULT current_timestamp
);
----------------------------------------------------------------------------------------------------------------
drop table Sponsor cascade;
create table Sponsor (
  id SERIAL,
  name 	varchar(50) NOT NULL,
  phone 	varchar(20) NOT NULL,
	company varchar(50),
	primary key(id,name)
);
----------------------------------------------------------------------------------------------------------------
drop table Events cascade;
create table Events (
  id SERIAL primary key,
  place varchar(50) NOT NULL,
  types varchar(40) check (types in ('Main-event', 'Pop-up-event', 'Leaflet', 'Parade')),
  start_date date NOT NULL,
  end_date date check (end_date >= start_date)
);
----------------------------------------------------------------------------------------------------------------
drop table Members cascade;
create table Members (
  id 	SERIAL,
  name 	varchar(20) NOT NULL,
  phone 	varchar(20) NOT NULL,
	birthday date,
	hometown varchar(15),
	campaign_counts int default 0,
	department varchar(50) check (department in ('Marketing', 'Content', 'Facility', 'ER')),
	primary key(id,name),
	tiers	varchar(20) check (tiers in ('Volunteer', 'Member', 'Head')) default 'Volunteer'
);

----------------------------------------------------------------------------------------------------------------
-- RELATIONSHIP:
-- 1. Paid = record of all events' cost has been paid (INVALID/VALID) 
-- 2. Participate =	record of all activities related to members and his/her evaluation for that activitiy
-- 3. Has = record of every events belong to a campaign
-- 4. Donate = record of the donation (in-flow)
----------------------------------------------------------------------------------------------------------------	
drop table Paid cascade;
create table Paid (
  event_id INT,
  amount real check (amount < 0),
  notice varchar(20),
  foreign key(event_id) references Events(id)
   on delete cascade
   on update cascade
);
----------------------------------------------------------------------------------------------------------------
drop table Participate cascade;
create table Participate (
  camp_id INT,
  camp_name varchar(50),
  mem_id INT,
  mem_name varchar(50),
  evaluation varchar(50),
  primary key(camp_id,mem_id),
  foreign key(camp_id,camp_name) references Campaigns(id,name)
   on delete cascade
   on update cascade,
  foreign key(mem_id,mem_name) references Members(id,name)
   on delete cascade
   on update cascade
);
----------------------------------------------------------------------------------------------------------------
drop table Has cascade;
create table Has (
  camp_id int,
  camp_name varchar(50),
  event_id int,
  foreign key(camp_id,camp_name) references Campaigns(id,name)
   on delete cascade
   on update cascade,
  foreign key(event_id) references Events(id)
   on delete cascade
   on update cascade
);
----------------------------------------------------------------------------------------------------------------
drop table Donate cascade;
create table Donate (
  sponsor_id int,
  sponsor_name varchar(30),
  amount real check (amount > 0),
  foreign key(sponsor_id,sponsor_name) references Sponsor(id,name)
   on delete cascade
   on update cascade
);

----------------------------------------------------------------------------------------------------------------
-- TRIGGER --
-- 1. Account's transactions input:
--		With every new insert to Paid/Donate: add new transaction record to Account and update the current balance
--		If the Paid amount > current balance: not add that transaction to Account, and set notice of that Paid to INVALID
-- 2. Member's tier update:
--		With every new insert to Participate: increase the campaigns_count of that member. 
--		If campaign_counts > 3, change tiers of that member from volunteer to member
----------------------------------------------------------------------------------------------------------------	
-- 1: Account's transactions input
CREATE OR REPLACE FUNCTION input_acc() RETURNS trigger AS $$
DECLARE
	balance INTEGER := (select curr_bal from Account where id = (select max(id) from Account));
BEGIN
  if (balance IS NULL) then 
    balance = 0;
  end if;
	if (balance + NEW.amount < 0) then
		RAISE NOTICE 'PAYMENT FAILURE - The cost of event (%) is exceeded the current balance (%)',NEW.amount,balance;
		UPDATE Paid 
		SET notice = 'INVALID' 
		WHERE event_id = new.event_id;
	else
		INSERT INTO Account(amount,curr_bal)
		VALUES (NEW.amount, balance + NEW.amount);
		if (NEW.amount < 0) then
			UPDATE Paid
			SET notice = 'VALID' 
			WHERE event_id = new.event_id;
		end if;
	end if;
	return new;
END;
$$ LANGUAGE plpgsql;

--DROP TRIGGER IF EXISTS donate_trans on Donate;
CREATE TRIGGER donate_trans
AFTER INSERT ON Donate
FOR EACH ROW EXECUTE PROCEDURE input_acc();

--DROP TRIGGER IF EXISTS paid_trans on Paid;
CREATE TRIGGER paid_trans
AFTER INSERT ON Paid
FOR EACH ROW EXECUTE PROCEDURE input_acc();

-- 2: Member's tier update
CREATE OR REPLACE FUNCTION tier_update() RETURNS trigger AS $$
DECLARE
	counter INTEGER := (select campaign_counts from Members where id = NEW.mem_id) + 1;
BEGIN
	if (counter > 3) AND ((select tiers from Members where id = NEW.mem_id) = 'Volunteer') then
		UPDATE Members
		SET tiers = 'Member',campaign_counts = counter 
		WHERE id = new.mem_id;
		RAISE NOTICE 'Volunteer (%) is promoted to be a member',NEW.mem_name;
	else
		UPDATE Members
		SET campaign_counts = counter
		WHERE id = new.mem_id;
	end if;
	return new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tier_updating
AFTER INSERT ON Participate
FOR EACH ROW EXECUTE PROCEDURE tier_update();
----------------------------------------------------------------------------------------------------------------
-- INDEX --
--    Create trigram index (GIST) against name (in Campaigns, Members) to allow "a few mispelling" query 
----------------------------------------------------------------------------------------------------------------	
CREATE INDEX camp_name_trigram ON Campaigns
USING gist (name gist_trgm_ops);

CREATE INDEX member_name_trigram ON Members
USING gist (name gist_trgm_ops);
----------------------------------------------------------------------------------------------------------------
-- SAMPLE DATA --
--    Insert sample data to the database  
----------------------------------------------------------------------------------------------------------------  
-- Entity sets:
insert into Campaigns(name,concept,start_date,end_date) values ('Binh Minh Sinh Vien 2013', 'Concert', '2013-08-15', '2013-09-10');
insert into Campaigns(name,concept,start_date,end_date) values ('Hoi cho 360 do Xuan ver6', 'Fair','2013-12-15', '2014-02-06');
insert into Campaigns(name,concept,start_date,end_date) values ('Vu Dieu Tre IDANCE', 'Contest', '2014-01-15', '2014-03-20');
insert into Campaigns(name,concept,start_date,end_date) values ('Chia Tay Khoa Cuoi K53', 'Concert', '2014-04-15', '2014-05-30');
insert into Campaigns(name,concept,start_date,end_date) values ('Binh Minh Sinh Vien 2014', 'Concert', '2014-08-15', '2014-09-16');
insert into Campaigns(name,concept,start_date,end_date) values ('Hoi cho 360 do Xuan ver7', 'Fair', '2014-12-15', '2015-01-28');
insert into Campaigns(name,concept,start_date,end_date) values ('Tat Den Bat Y Tuong', 'Concert', '2015-01-15', '2015-04-02');
insert into Campaigns(name,concept,start_date,end_date) values ('Chia Tay Khoa Cuoi K54', 'Concert', '2015-04-15', '2015-06-01');

insert into Sponsor(name,phone,company) values ('Hoang Tung Anh', '(604)777-1111', 'PepsiCo');
insert into Sponsor(name,phone,company) values ('Lam Tung', '(604)778-1212', 'NEU student society');
insert into Sponsor(name,phone,company) values ('Dinh Nam', '(604)718-1333', 'NEU student society');
insert into Sponsor(name,phone,company) values ('Phan Vu', '(604)622-4542', 'NEU student society');
insert into Sponsor(name,phone,company) values ('Thao Robo', '(604)413-1455', 'NEU student society');

insert into Events(place,types,start_date,end_date) values ('KTX NEU', 'Pop-up-event', '2013-08-22', '2013-08-23');
insert into Events(place,types,start_date,end_date) values ('Giang duong NEU', 'Leaflet', '2013-09-02', '2013-09-06');
insert into Events(place,types,start_date,end_date) values ('1020 Tran Dai Nghia street, Ha Noi', 'Parade', '2013-09-07', '2013-09-07');
insert into Events(place,types,start_date,end_date) values ('KTX NEU', 'Main-event', '2013-09-08', '2013-09-08');

insert into Members(name,phone,birthday,hometown,department) values ('Le Viet Dung', '(250)555-1212', '1995-04-10', 'Ha Noi','Marketing');
insert into Members(name,phone,birthday,hometown,department) values ('Vo Ha Trang', '(250)818-3212', '1995-04-30', 'Thai Nguyen','Content');
insert into Members(name,phone,birthday,hometown,department) values ('Vu Thao Vi', '(250)516-1332', '1995-08-20', 'Hai Phong','Content');
insert into Members(name,phone,birthday,hometown,department) values ('Nguyen The Vinh', '(250)444-9696', '1995-03-15', 'Hai Duong','Facility');
insert into Members(name,phone,birthday,hometown,department) values ('Nguyen Duc Toan', '(250)444-9696', '1995-03-15', 'Thai Nguyen','Marketing');
insert into Members(name,phone,birthday,hometown,department) values ('Vu Khanh Linh', '(250)444-9696', '1995-03-15', 'Lao Cai','ER');
insert into Members(name,phone,birthday,hometown,department) values ('Nguyen Thao Ha', '(250)444-9696', '1995-03-15', 'Bac Giang','ER');

-- Relationship
insert into Donate values(1,'Hoang Tung Anh',150000);
insert into Donate values(2,'Lam Tung',500000);
insert into Donate values(3,'Dinh Nam',800000);
insert into Donate values(4,'Phan Vu',100000);
insert into Donate values(5,'Thao Robo',1000000);

insert into Paid(event_id,amount) values (1,-5000);
insert into Paid(event_id,amount) values (2,-15000);
insert into Paid(event_id,amount) values (3,-25000);
insert into Paid(event_id,amount) values (4,-20000000);

insert into Participate values(1,'Binh Minh Sinh Vien 2013',1,'Le Viet Dung','Excellent');
insert into Participate values(1,'Binh Minh Sinh Vien 2013',3,'Vu Thao Vi','Excellent');
insert into Participate values(1,'Binh Minh Sinh Vien 2013',4,'Nguyen The Vinh','Excellent');
insert into Participate values(3,'Vu Dieu Tre IDANCE',1,'Le Viet Dung','Excellent');
insert into Participate values(2,'Hoi cho 360 do Xuan ver6',2,'Vo Ha Trang','Excellent');
insert into Participate values(4,'Chia Tay Khoa Cuoi K53',5,'Nguyen Duc Toan','Excellent');
insert into Participate values(5,'Binh Minh Sinh Vien 2014',1,'Le Viet Dung','Excellent');
insert into Participate values(6,'Hoi cho 360 do Xuan ver7',1,'Le Viet Dung','Excellent');

insert into Has values(1,'Binh Minh Sinh Vien 2013',1);
insert into Has values(1,'Binh Minh Sinh Vien 2013',2);
insert into Has values(1,'Binh Minh Sinh Vien 2013',3);
insert into Has values(1,'Binh Minh Sinh Vien 2013',4);


