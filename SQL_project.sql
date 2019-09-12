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
  amount 			real check (amount + curr_bal > 0),
  curr_bal 		int default 0,
	trans_time 		timestamp without time zone DEFAULT current_timestamp
);
----------------------------------------------------------------------------------------------------------------
drop table Sponsor cascade;
create table Sponsor (
  id SERIAL,
  name 	varchar(20) NOT NULL,
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
	campaign_counts real default 0,
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
CREATE OR REPLACE FUNCTION input_account() RETURNS trigger AS $$
DECLARE
	balance INTEGER := 0;
BEGIN
	balance := (select curr_bal from Account where id = (select max(id) from Account));
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

CREATE TRIGGER donate_transactions
AFTER INSERT ON Donate
FOR EACH ROW EXECUTE PROCEDURE input_account();

CREATE TRIGGER paid_transactions
AFTER INSERT ON Paid
FOR EACH ROW EXECUTE PROCEDURE input_account();

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