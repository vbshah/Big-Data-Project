# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 18:06:12 2018

@author: vbshah
"""

from mysql import connector
import pandas as pd
import random
from datetime import datetime

def load_data(*file_names):
    global data
    data = pd.read_csv(file_names[0])   # get Complaint dataCSV file
    location_data = pd.read_csv(file_names[1])
    """
    primary_data format: {table_name: {dbname: csv_name}}
    """    
    data["customer_name"] = ["John Doe"] * len(data)     # adding this for temporarily
    data['Age Range'] = [random.randint(20, 80) 
        for _ in range(len(data))]      # adding this for temporarily
    data['Income Range'] = [random.randint(50000,100000) 
        for _ in range(len(data))]
    data['State'] = location_data['State']
    data['Zipcode'] = pd.Series([str(i) for i in location_data['Zipcode']])
    data['City'] = location_data['City']
    data["Company ZIP"] = data['ZIP code']
    return data

configs = {
    "host": "localhost",
    "user": "root",
    "password": "temp1234",
    "database": "bigdataproject"
}
db = connector.connect(**configs)
cursor = db.cursor()
complaint_file = 'Consumer_Complaints.csv'
location_file ='free-zipcode-database-Primary.csv'
data = load_data(complaint_file, location_file)

rec_date_dict = dict()
sent_date_dict = dict()

cntr = 0
for i in range(len(data)):
    complaint_id = data['Complaint ID'][i]
    recieved_date = data['Date received'][i]
    sent_to_company = data['Date sent to company'][i]
    recieved_date = "'" + datetime.strptime(recieved_date, '%m/%d/%Y').strftime('%Y-%m-%d') + "'"
    sent_to_company = "'" + datetime.strptime(sent_to_company, '%m/%d/%Y').strftime('%Y-%m-%d') + "'"
    update_query = 'update cfpb_complaint set date_received = ' + recieved_date + ', date_sent_to_company = ' + sent_to_company + ' where complaint_ID = '  + str(complaint_id)
    cursor.execute(update_query)
    if cntr % 100 == 0:
        db.commit()
    if cntr % 1000 == 0:
        print("completed", cntr)
    cntr += 1

db.close()