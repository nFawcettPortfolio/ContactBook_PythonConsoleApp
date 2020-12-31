# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 18:55:41 2020

@author: Kami
"""

import mysql.connector
from datetime import date

cnx = mysql.connector.connect( user='root',password='<PASSWORD>',database='address_book')
cur = cnx.cursor()
running = True
while running:
    print("Options:\n1. Search by Last Name. \n2. Search by Prefix. \n3. Add/Edit Contact. \n4. Search Age Range. \n5. Quit")
    option = input("Please enter your option:")
    if int(option) == 5:
        running=False;
    elif int(option) == 1:
        name = input("Please enter last name:")
        cur.execute(" SELECT people_master.person_id, last_name, first_name, prefix, person_DOB, people_address.address_id, street_address, city, state, zipcode, start_date, end_date  FROM  people_master JOIN people_address ON people_master.person_id = people_address.person_id JOIN addresses ON people_address.address_id = addresses.address_id WHERE last_name = '{0}'".format(name))
        out = cur.fetchall()
        for o in out:
            print(o)
    elif int(option) == 2:
        prefix = input("Please enter a name prefix:")
        cur.execute(" SELECT people_master.person_id, last_name, first_name, prefix, person_DOB, people_address.address_id, street_address, city, state, zipcode, start_date, end_date  FROM  people_master JOIN people_address ON people_master.person_id = people_address.person_id JOIN addresses ON people_address.address_id = addresses.address_id WHERE prefix = '{0}'".format(prefix))
        out = cur.fetchall()
        for o in out:
            print(o)
    elif int(option) == 3:
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        prefix=input("Enter prefix: ")
        dob=input("Enter Date of Birth (YYYY-MM-DD): ")
        phone=input("Enter active phone number: ")
        street=input("Enter street address: ")
        city=input("Enter city: ")
        state=input("Enter state abbrieviation: ")
        zipcode=input("Enter zipcode: ")
        
        # CHECK IF PERSON EXISTS
        sql = "SELECT IF( EXISTS( SELECT * FROM people_master WHERE last_name =  '{0}' AND first_name = '{1}'), 1, 0)".format(last_name, first_name)
        cur.execute(sql)
        out=cur.fetchone()
        if '1' in str(out):
            
            # CONTACT EXISTS
            # UPDATE PHONE NUMBER
            sql = "UPDATE people_master SET active_phone_number = '{0}' WHERE first_name = '{1}' AND last_name = '{2}'".format(phone,first_name,last_name)
            cur.execute(sql)
            cnx.commit()
            
            #CHECK ADDRESS
            sql = "SELECT IF( EXISTS( SELECT * FROM addresses WHERE street_address =  '{0}' AND city = '{1}'), 1, 0)".format(street, city)
            cur.execute(sql)
            out=cur.fetchone()
            
            # INPUT NEW ADDRESS
            if '0' in str(out):
                sql = "INSERT INTO addresses (street_address, city, state, zipcode) VALUES ('{0}', '{1}', '{2}', '{3}');".format(street,city,state,zipcode)
                cur.execute(sql)
                cnx.commit()
                
                begin_date = input("Please enter the begin date for the new address (YYYY-MM-DD):")
                
                # GET PERSON ID
                sql = "SELECT person_id FROM people_master WHERE first_name = '{0}' AND last_name = '{1}'".format(first_name, last_name)
                cur.execute(sql)
                temp = cur.fetchall()
                person_id=temp[0][0];
                
                # GET ADDRESS ID
                sql = "SELECT address_id FROM addresses WHERE street_address = '{0}' AND city = '{1}'".format(street, city)
                cur.execute(sql)
                temp = cur.fetchall()
                address_id=temp[0][0];
                
                # UPDATE PEOPLE_ADDRESS END_DATE --- IF OLD CONTACT AND NEW ADDRESS
                sql = "UPDATE people_address SET end_date = '{0}' WHERE person_id = '{1}' AND end_date IS NULL".format(begin_date,person_id)
                cur.execute(sql)
                cnx.commit()
                
                # INPUT INFO PEOPLE_ADDRESS --- IF OLD CONTACT AND NEW ADDRESS
                sql = "INSERT INTO people_address (person_id, address_id, start_date) VALUES ('{0}', '{1}', '{2}');".format(person_id,address_id,begin_date)
                cur.execute(sql)
                cnx.commit()
                print("Contact updated")
            else:
                print("Contact and address already exist.\n")
                
        # NEW CONTACT    
        else:
            begin_date = input("Please enter the begin date for the new address (YYYY-MM-DD):")
            sql = "INSERT INTO people_master (first_name, last_name, prefix, person_DOB, active_phone_number) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');".format(first_name, last_name, prefix,dob,phone)
            cur.execute(sql)
            cnx.commit()
            #CHECK ADDRESS
            sql = "SELECT IF( EXISTS( SELECT * FROM addresses WHERE street_address =  '{0}' AND city = '{1}'), 1, 0)".format(street, city)
            cur.execute(sql)
            out=cur.fetchone()
            # INPUT NEW ADDRESS
            if '1' not in str(out):
                sql = "INSERT INTO addresses (street_address, city, state, zipcode) VALUES ('{0}', '{1}', '{2}', '{3}');".format(street,city,state,zipcode)
                cur.execute(sql)
                cnx.commit()
                
                # GET PERSON ID
                sql = "SELECT person_id FROM people_master WHERE first_name = '{0}' AND last_name = '{1}'".format(first_name, last_name)
                cur.execute(sql)
                temp = cur.fetchall()
                person_id=temp[0][0]
                print(person_id)
                
                # GET ADDRESS ID
                sql = "SELECT address_id FROM addresses WHERE street_address = '{0}' AND city = '{1}'".format(street, city)
                cur.execute(sql)
                temp = cur.fetchall()
                address_id=temp[0][0]
                print(address_id)
                
                # INPUT INFO PEOPLE_ADDRESS --- IF NEW CONTACT AND NEW ADDRESS
                sql = "INSERT INTO people_address (person_id, address_id, start_date) VALUES ('{0}', '{1}', '{2}');".format(person_id,address_id,begin_date)
                cur.execute(sql)
                cnx.commit()
                print("Contact added.\n")
            # NEW CONTACT OLD ADDRESS
            else:
                # GET PERSON ID
                sql = "SELECT person_id FROM people_master WHERE first_name = '{0}' AND last_name = '{1}'".format(first_name, last_name)
                cur.execute(sql)
                temp = cur.fetchall()
                person_id=temp[0][0];
                
                # GET ADDRESS ID
                sql = "SELECT address_id FROM addresses WHERE street_address = '{0}' AND city = '{1}'".format(street, city)
                cur.execute(sql)
                temp = cur.fetchall()
                address_id=temp[0][0];
                
                # INPUT INFO PEOPLE_ADDRESS --- IF NEW CONTACT AND NEW ADDRESS
                sql = "INSERT INTO people_address (person_id, address_id, start_date) VALUES ('{0}', '{1}', '{2}');".format(person_id,address_id,begin_date)
                cur.execute(sql)
                cnx.commit()
                print("Contact added.\n")
        
    elif int(option) == 4:
        age_min = input("Please enter minimum age:")
        age_max = input("Please enter maximum age:")
        dt = date.today()
        min_dt = dt.replace(year=dt.year-int(age_min))
        max_dt = dt.replace(year=dt.year-int(age_max))
        cur.execute(" SELECT people_master.person_id, last_name, first_name, prefix, person_DOB, people_address.address_id, street_address, city, state, zipcode, start_date, end_date  FROM  people_master JOIN people_address ON people_master.person_id = people_address.person_id JOIN addresses ON people_address.address_id = addresses.address_id WHERE person_DOB BETWEEN '{1}' AND '{0}'".format(min_dt, max_dt))
        out = cur.fetchall()
        d= out
        print("Showing contacts born between {1} and {0}".format(min_dt,max_dt))
        print(d[0][0])
        for o in out:
            print(o)
    else:
        print("Input was not a valid option. Please enter a valid option.")

cnx.close()