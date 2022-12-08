import os
import sys
import requests
import shutil
from pathlib import Path

import pandas as pd
import numpy as np
from datetime import datetime, date

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import re
from os import listdir
from os.path import isfile, join

# data files path.
file_path = Path (r'/bigdata/data/source/elmis')

# Log files path and file names.
log_path = Path (r'/bigdata/logs')

process_log_file = ('extract_process_' + str(datetime.utcnow().strftime('%m%d%Y_%I%M%S')) + '.log')
error_log_file = ('extract_error_' + str(datetime.utcnow().strftime('%m%d%Y_%I%M%S')) + '.log')

error_log = open(log_path / error_log_file, 'w')

# Archive old files.

source = '/bigdata/data/source/elmis/'
archive = '/bigdata/data/source/elmis/archive'

files = os.listdir(source)

for f in files:
    shutil.move(source+f,archive)

# Script parameters (scheduled, adhoc)
# On schedule run, determine the [month] and [year] parameter values from the system date.
# On adhoc, prompt the user to enter the desired [month] and [year] parameters as an input.

parameter = sys.argv[1]
print ('Paramter selected=', parameter)

if parameter == 'scheduled':
  # Get previous month and year
    now = datetime.now()
    if now.month > 1 :
        day = now.day
        last_month = now.month-1
        file_year = now.year
        x = datetime(file_year,last_month,day)
        file_month = x.strftime('%m')
    else:
        file_month = 12
        file_year = now.year - 1

elif parameter == 'adhoc':
    now = datetime.now()
    day = now.day
    file_year = input("Enter desired year ex. 2020 :")
    listOfyears = ['2018' , '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028']
	# Validate file_year in list of years
    if file_year not in listOfyears :
       print("Desired year "+file_year+" NOT found in the possible List of years : " , listOfyears)
       quit()
    file_month = input("Enter desired month ex. 01 for Jan :")
    listOfmonths = ['01' , '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	# Validate file_month in list of months
    if file_month not in listOfmonths :
      print("Desired month "+file_month+" NOT found in the possible List of months : " , listOfmonths)
      quit()
	# Validate selected year and month are less then current year and month
    selected_date = datetime(int(file_year), int(file_month), int(day)).date()
    if selected_date >= now.date() :
      print("Desired year/month ("+file_year+"/"+file_month+") should be less then current year and month.")
      quit()
    print('\n')
    print('User entered year: '+ str(file_year))
    print('User entered month: '+ str(file_month))
    print('\n')

# Log file
info_log = open(log_path / process_log_file, 'w')
sys.stdout = info_log

# Email configration
def send_email(sender='bigdata@ghsc-psm.org',to='wirshad@ghsc-psm.org', subject='Extract Process Completed', body= 'Extract process completed. Please review the attched log files for any exceptions.', attach= log_path/error_log_file, attach1=log_path/process_log_file):
    cmd = 'echo "{b}" | mailx -r "{sender}" -s "{s}" -a "{a}" -a "{a1}" "{to}" '.format(b=body,sender=sender, s=subject, a=attach, a1=attach1, to=to)
    # print(cmd)
    os.system(cmd)

print('Parameter selected =', parameter)
if parameter == 'scheduled':
    print('system entered year: '+ str(file_year))
    print('system entered month: '+ str(file_month))
else:
    print('User entered year: '+ str(file_year))
    print('User entered month: '+ str(file_month))
print('\n')

# Print log files path
print ('## Log files path')
print (log_path)
print ('\n')

# Print log files name.
print ('## Log files name..')
print (process_log_file)
print (error_log_file)
print('\n')

# Data files name.
product_file_name =  'product_master_'+ str(file_month) + str(file_year) + '.csv'
facility_file_name = 'facility_master_'+ str(file_month) + str(file_year) + '.csv'
facility_status_file_name = 'facility_status_'+ str(file_month) + str(file_year) + '.csv'
stock_detail_file_name = 'stock_detail_'+ str(file_month) + str(file_year) + '.csv'

# Print data files path.
print ('## Data files path')
print (file_path)
print ('\n')

# Print the files name.
print ('## Data files name generated...')
print (product_file_name)
print (facility_file_name)
print (facility_status_file_name)
print (stock_detail_file_name)
print('\n')

# API URL's
product_url = "https://ospsante.org/api/v1/product.php?format=CSV&product_group=FP"
facility_url = "https://ospsante.org/api/v1/facility.php?format=CSV"
facility_status_url = "https://ospsante.org/api/v1/facility_report.php?format=CSV&year="+str(file_year)+"&month="+str(file_month)+"&product_group=FP"
stock_detail_url = "https://ospsante.org/api/v1/stock_detail.php?format=CSV&year="+str(file_year)+"&month="+str(file_month)+"&product_group=FP"

# Print the API's
print ("## API URL's generated...")
print (product_url)
print (facility_url)
print (facility_status_url)
print (stock_detail_url)
print('\n')

# Get data and write it to files
print ("## Extract process started on     : ", str(datetime.now()))

urls_files = [(product_url, product_file_name), (facility_url, facility_file_name), (facility_status_url, facility_status_file_name), (stock_detail_url, stock_detail_file_name)]

for url, file in urls_files:
	response = requests.get(url)
	with open(os.path.join(file_path, file), 'wb') as f:
		f.write(response.content)
		print ('Extract process completed for data file: ', file)

print ("## Extract process completed on   : ", str(datetime.now()))
print('\n')

# File validation (internal exceptions)
print ("## Internal exceptions identified in the source files..." , file = error_log)

api_errors = ["IP not authorized to call API","Parameters not valid", "Format not valid", "Year not valid", "Month not valid", "Product group not valid"]

for file in urls_files:
	with open(os.path.join(file_path, product_file_name), 'r') as searchfile:
    		read_data = searchfile.read()
	for err in api_errors:
    		if err in read_data:
            		print ('\n','Error found in file (' +file+ ') : ' + err, end='', file = error_log)

error_log.close()
info_log.close()

send_email()

#If scheduled run, run transformation and load


if(parameter=='scheduled'):
    
    '''
    eLMIS file extract path
    '''
    folder_path = r"/bigdata/data/source/elmis" "//"
    fac_path = folder_path + r"facility_master_052020.csv"
    fac_status = folder_path + r"facility_status_052020.csv"
    prod_path = folder_path + r"product_master_052020.csv"
    stock_path = folder_path + r"stock_detail_052020.csv"

    #Log path
    log_path = Path (r'C:\Users\BeckyLING\Box Sync\USAID GHSC-PSM\Big Data FP\Log Test')
    process_log_file = ('transformation_load_' + str(datetime.utcnow().strftime('%m%d%Y_%I%M%S')) + '.log')
    error_log_file = ('transformation_load_error_' + str(datetime.utcnow().strftime('%m%d%Y_%I%M%S')) + '.log')

    '''
    Local facility mapping
    Columns in file: district (in LMIS), facility_code (in LMIS), latitude, longitude, district from shapefile
    '''
    fac_map = pd.read_csv(r"C:\Users\BeckyLING\Box Sync\USAID GHSC-PSM\Big Data FP\facility_mapping.csv", index_col = 0)
    fac_map = fac_map.dropna()
    fac_map = fac_map.drop_duplicates().reset_index()
    fac_map = fac_map.rename(columns = {'district from shapefile':'demo_district'})
    fac_map = fac_map[['district','facility_code','demo_district']]
    fac_map.loc[fac_map['demo_district'].str.contains('Commune'),'demo_district'] = 'Dissolved'

    '''
    Establish database connection
    '''
    URI = 'postgresql://dbadmin:Bigdata2020@psm-to3-lx1.eastus2.cloudapp.azure.com/bigdata'
    engine = create_engine(URI  , echo=True)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()

    '''
    Get current tables in database
    '''

    class facility(Base):
        __tablename__ = "facility"
        __table_args__ = {'schema':'bigdata'}
        facility_code =     Column(String(100), primary_key = True)
        facility_name =     Column(String(100))
        facility_type =     Column(String(100))
        region_name =       Column(String(100))
        district =          Column(String(100))
        demo_district =     Column(String(100))
        owner_type =        Column(String(100))
        ppm =               Column(String(100))
        service_area =      Column(String(100))
        facility_address =  Column(String(100))
        assigned_group =    Column(String(100))
        facility_phone =    Column(String(100))
        facility_fax =      Column(String(100))
        facility_email =    Column(String(100))
        latitude =          Column(Float(11,8))
        longitude =         Column(Float(11,8))
        create_date =       Column(DateTime())
        creator_id =        Column(String(24))
        last_modified_date =Column(DateTime())
        last_modified_by =   Column(String(24))
        source_id =         Column(String(24))
        current_ind =       Column(String(1))

    class facility_status(Base):
        __tablename__ = "facility_status"
        __table_args__ = {'schema':'bigdata'}
        calendar_year =         Column(String(100), primary_key = True)
        month_number =          Column(Integer, primary_key = True)
        facility_code =         Column(String(24), primary_key = True)
        entered_ind =           Column(String(1))
        entry_date =            Column(DateTime())
        submitted_ind =         Column(String(1))
        submitted_date =        Column(DateTime())
        published_ind =         Column(String(1))
        published_date =        Column(DateTime())
        create_date =           Column(DateTime())
        creator_id =            Column(String(24))
        last_modified_data =    Column(DateTime())
        last_modified_by =      Column(String(24))
        source_id =             Column(String(24))
        current_ind =           Column(String(1))



    class product(Base):
        __tablename__ = "product"
        __table_args__ = {'schema':'bigdata'}
        product_code =      Column(String(100), primary_key = True)
        product_name =      Column(String(100))
        short_name =        Column(String(100))
        key_product =       Column(Boolean)
        product_subgroup =  Column(String(100))
        create_date =       Column(DateTime())
        creator_id =        Column(String(24))
        last_modified_date =Column(DateTime())
        last_modified_by =  Column(String(24))
        source_id =         Column(String(24))
        current_ind =       Column(String(1))

    class stock_detail(Base):
        __tablename__ = "stock_detail"
        __table_args__ = {'schema':'bigdata'}
        calendar_year =         Column(String(100), primary_key = True)
        month_number =          Column(Integer, primary_key = True)
        product_code =          Column(String(100), primary_key = True)
        facility_code =         Column(String(24), primary_key = True)
        obl =                   Column(Integer)
        received =              Column(Integer)
        dispensed =             Column(Integer)
        adjusted =              Column(Integer)
        stock_out_days =        Column(Integer)
        closing_stock =         Column(Integer)
        amc =                   Column(Integer)
        mos =                   Column(Float(12,5))
        inventory_turn_rate =   Column(Float(12,5))
        turn_rate_ind =         Column(String(1))
        fp_priority_score =     Column(Integer)
        create_date =           Column(DateTime())
        creator_id =            Column(String(24))
        last_modified_date =    Column(DateTime())
        last_modified_by =       Column(String(24))
        source_id =             Column(String(24))
        current_ind =           Column(String(1))



    facility_query = session.query(facility)
    facility_df = pd.read_sql(facility_query.statement, session.bind)

    product_query = session.query(product)
    product_df = pd.read_sql(product_query.statement, session.bind)

    facility_status_query = session.query(facility)
    facility_status_df = pd.read_sql(facility_status_query.statement, session.bind)

    stock_query = session.query(stock_detail)
    stock_detail_df = pd.read_sql(stock_query.statement, session.bind)



    '''
    Read in eLMIS extracts
    '''
    #facility_new = pd.read_csv(fac_path, sep = "|")
    #facility_status = pd.read_csv(fac_status, sep = "|")
    #product_new = pd.read_csv(prod_path, sep = "|")
    #stock_new = pd.read_csv(stock_path, sep = "|")


    '''
    Compare changes in the facility and product tables. Determine which lines need to be added or updated
    Dataframes should be cleaned so both new and existing tables have the same columns
    '''

    def get_extracts(folder_path):
        files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
        fac_ref_ptn = re.compile('^facility_master_.*') #file name patterns
        fac_status_ptn = re.compile('^facility_status_.*')
        prod_ref_ptn = re.compile('^product_master_.*')
        stock_ptn = re.compile('^stock_detail_.*')
        facility_match = [line for line in files if fac_ref_ptn.match(line)]
        e = []
        if (len(facility_match) > 1):
            e.append("Could not identify correct facility master file to use.")
            sys.exit('Could not identify correct facility master file to use.')
        else:
            facility_path = facility_match[0]
            facility_new = pd.read_csv(os.path.join(folder_path, facility_path), sep = "|")
        facility_stat_match = [line for line in files if fac_status_ptn.match(line)]
        if(len(facility_stat_match)>1):
            e.append('Could not identify correct facility status file to use.')
            sys.exit('Could not identify correct facility status file to use.')
        else:
            facility_status_path = facility_stat_match[0]
            facility_status = pd.read_csv(os.path.join(folder_path, facility_status_path), sep = "|")
        product_match = [line for line in files if prod_ref_ptn.match(line)]
        if(len(product_match)>1):
            e.append('Could not identify correct product reference file to use.')
            sys.exit('Could not identify correct product reference file to use.')
        else:
            product_path = product_match[0]
            product_new = pd.read_csv(os.path.join(folder_path, product_path), sep = "|")
        stock_match = [line for line in files if stock_ptn.match(line)]
        if (len(stock_match)>1):
            e.append('Could not idenfiy the correct stock detail report.')
            sys.exit('Could not idenfiy the correct stock detail report.')
        else:
            stock_detail_path = stock_match[0]
            stock_new = pd.read_csv(os.path.join(folder_path, stock_detail_path), sep = "|")
        
        return facility_new, facility_status, product_new, stock_new,facility_path, facility_status_path, product_path, stock_detail_path,e





    def df_comparison(og_df, new_df):
        """Compares new extracted reference to existing reference table in DB.

        Args:
            og_df (dataframe): Existing reference table in DB
            new_df (dataframe): New reference table extracted

        Returns:
            List: Lists of IDs to be deactivated and inserted
        """
        id_column = new_df.columns[0]
        merged = og_df.merge(new_df, on = id_column, indicator = True, how = 'outer')
        deact_id = merged[merged['_merge'] == 'left_only'].iloc[:,0]
        insert_id = merged[merged['_merge'] == 'right_only'].iloc[:,0]

        return deact_id, insert_id

    def df_multiple_comps(og_df, new_df, prim_keys):
        num_keys = len(prim_keys)
        new_keys = new_df[prim_keys]
        og_keys = og_df[prim_keys]
        merged = og_keys.merge(new_keys, on = prim_keys, indicator = True, how = 'outer')
        deact_id = merged[merged['_merge'] == 'left_only'].iloc[:,:num_keys]
        insert_id = merged[merged['_merge'] == 'right_only'].iloc[:,:num_keys]
        update_id = merged[merged['_merge'] == 'both'].iloc[:,:num_keys]
        update_df = update_id.merge(new_df, on = update_id.columns, how = 'left')

        return deact_id, insert_id, update_id, update_df

    def get_by_id(df, id_name, id_list):
        """Returns dataframe with corresponding ID

        Args:
            df (dataframe): Data table to be filtered
            id_name (String): column name containing the unique IDs
            id_list (list): List of IDs to be extracted from table

        Returns:
            dataframe: Filtered dataframe
        """
        new_df = df[df[id_name].isin(id_list)]
        return new_df

    def details_comps(og_df, new_df, id_col):
        """Compares details of tables that exist in both new extract and database

        Args:
            og_df (dataframe): Existing reference table in the database
            new_df (dataframe): New extracted reference table
            id_col (String): Name of ID column common to both tables

        Returns:
            dataframe: Dataframe to be updated with new details from the extract
        """
        merged = og_df.merge(new_df, on = id_col, indicator = True, how = 'outer')
        both_id = merged[merged['_merge'] == 'both'].iloc[0]

        og_both = og_df[og_df[id_col].isin(both_id)]
        new_both = new_df[new_df[id_col].isin(both_id)]
        inner = og_both.merge(new_both, on = list(og_both.columns), how = 'inner')
        update_df = new_both[~new_both[id_col].isin(inner[id_col])]

        return update_df

    def reference_update(og_df, new_df, id_col, df_class):
        """Compares reference table in DB with new extract, and conduct insertion, deactivation, and update to DB

        Args:
            og_df (dataframe): Existing reference table in the DB
            new_df (dataframe): New extracted reference table
            id_col (String): Name of ID column common to both tables
            df_class (String): Name of object corresponding to DB table
        """
        inserted = 0
        deactivated = 0
        updated = 0
        new_df.columns = og_df.columns
        if(og_df.empty):
            insert_db(df_class, new_df)
            inserted = len(new_df.index)
        else:
            if(isinstance(id_col, str)):
                #One id column
                deact_id, insert_id = df_comparison(og_df, new_df)
                #deact_df = get_by_id(og_df, id_col, deact_id)
                insert_df = get_by_id(new_df, id_col, insert_id)
                update_df = details_comps(og_df, new_df, id_col)
                #If the datasets are not empty, push to database
                if(insert_df.empty == False):
                    insert_db(df_class, insert_df)
                    inserted = len(insert_df.index)
                if len(deact_id) > 0:
                    deactivate_db(df_class, id_col, deact_id)
                    deactivated = len(deact_id)
                if not update_df.empty:
                    update_df.drop(columns = ['create_date','creator_id'], inplace = True)
                    update_db(df_class, id_col, update_df)
                    updated = len(update_df.index)
            else:
                deact_id, insert_id, update_id, update_df = df_multiple_comps(og_df, new_df, id_col)
                if(insert_df.empty == False):
                    insert_db(df_class, insert_df)
                    inserted = len(insert_df.index)
                if len(deact_id) > 0:
                    deactivate_db(df_class, id_col, deact_id)
                    deactivated = len(deact_id)
                if not update_df.empty:
                    update_df.drop(columns = ['create_date','creator_id'], inplace = True)
                    update_db(df_class, id_col, update_df)
                    updated = len(update_df.index)

        return inserted, deactivated, updated


    def insert_db(class_name, new_df):
        """Inserts data into DB table

        Args:
            class_name (String): Name of table
            new_df (dataframe): Table containing data to be inserted
        """
        session.bulk_insert_mappings(class_name, new_df.to_dict(orient="records"))
        session.commit()

    def deactivate_db(class_name, col_id, deact_id):
        """Deactivates records in reference table

        Args:
            class_name (String): Name of reference table
            col_id (String): Name of ID column
            deact_id (List): List of IDs to be deactivated
        """
        if (col_id == 'product_code'):
            results = session.query(class_name).filter(class_name.product_code.in_(deact_id)).all()
            for result in results:
                result.current_ind = 'N'
                result.last_modified_date = datetime.now()
            session.commit()
        elif(col_id == 'facility_code'):
            results = session.query(class_name).filter(class_name.facility_code.in_(deact_id)).all()
            for result in results:
                result.current_ind = 'N'
                result.last_modified_date = datetime.now()
            session.commit()
        elif((len(col_id)>1)&('product_code' in col_id)):
            #stock detail report
            results = session.query(class_name).filter(class_name.facility_code.in_(deact_id['facility_code']),class_name.product_code.in_(deact_id['product_code']),class_name.month_number.in_(deact_id['month_number']),class_name.calendar_year.in_(deact_id['calendar_year'])).all()
            keys = deact_id['facility_code']+deact_id['product_code']+deact_id['month_number']+deact_id['calendar_year']
            for result in results:
                if((result.facility_code + result.product_code + result.month_number + result.calnedar_year) in keys.unique()):
                    result.last_modified_date = datetime.now()
                    result.col_id = 'N'
            session.commit()
        elif((len(col_id)>1)&('product_code' not in col_id)):
            #facility status
            results = session.query(class_name).filter(class_name.facility_code.in_(deact_id['facility_code']),class_name.month_number.in_(deact_id['month_number']),class_name.calendar_year.in_(deact_id['calendar_year'])).all()
            keys = deact_id['facility_code']+deact_id['month_number']+deact_id['calendar_year']
            for result in results:
                if((result.facility_code + result.month_number + result.calnedar_year) in keys.unique()):
                    result.last_modified_date = datetime.now()
                    result.col_id = 'N'
            session.commit()

    def update_db(class_name, col_id, update_df):
        if col_id == 'facility_code':
            results = session.query(class_name).filter(class_name.facility_code.in_(update_df[col_id])).all()
            for result in results:
                update_row = update_df[update_df[col_id]==result.facility_code]
                update_dict = update_row.to_dict('records')
                for i in range(len(update_dict)):
                    dictionary = update_dict[i]
                    for key, value in dictionary.items():
                        setattr(result, key, value)
        elif col_id == 'product_code':
            results = session.query(class_name).filter(class_name.product_code.in_(update_df[col_id])).all()
            for result in results:
                update_row = update_df[update_df[col_id]==result.product_code]
                update_dict = update_row.to_dict('records')
                for i in range(len(update_dict)):
                    dictionary = update_dict[i]
                    for key, value in dictionary.items():
                        setattr(result, key, value)
        elif((len(col_id)>1)&('product_code' in col_id)):
            #stock detail report
            results = session.query(class_name).filter(class_name.facility_code.in_(update_df['facility_code']),class_name.product_code.in_(update_df['product_code']),class_name.month_number.in_(update_df['month_number']),class_name.calendar_year.in_(update_df['calendar_year'])).all()
            keys = update_df['facility_code']+update_df['product_code']+update_df['month_number']+update_df['calendar_year']
            for result in results:
                if((result.facility_code + result.month_number + result.calnedar_year) in keys.unique()):
                    update_row = update_df[(update_df['calendar_year']==result.calendar_year)&(update_df['month_number']==result.month_number)&(update_df['product_code']==result.product_code)&(update_df['facility_code']==result.facility_code)]
                    update_dict = update_row.to_dict('records')
                    for i in range(len(update_dict)):
                        dictionary = update_dict[i]
                        for key, value in dictionary.items():
                            setattr(result, key, value)
        elif((len(col_id)>1)&('product_code' not in col_id)):
            results = session.query(class_name).filter(class_name.facility_code.in_(update_df['facility_code']),class_name.month_number.in_(update_df['month_number']),class_name.calendar_year.in_(update_df['calendar_year'])).all()
            keys = update_df['facility_code']+update_df['month_number']+update_df['calendar_year']
            for result in results:
                if((result.facility_code + result.month_number + result.calnedar_year) in keys.unique()):
                    update_row = update_df[(update_df['calendar_year']==result.calendar_year)&(update_df['month_number']==result.month_number)&(update_df['facility_code']==result.facility_code)]
                    update_dict = update_row.to_dict('records')
                    for i in range(len(update_dict)):
                        dictionary = update_dict[i]
                        for key, value in dictionary.items():
                            setattr(result, key, value)
        session.commit()



    def groupbyfn(x):
        # x = dataframe that is a subset of the original data frame
        # d = a dictionary of functions
        #### keys are names of new columns
        #### values are functions operating on the columns of x and resulting in a single, aggregated value
        d = {}
        
        # Coefficient of variance of consumption = std(cons)/avg(cons) 
        #d['consumption_cov'] = x['Dispensed'].std()/x['Dispensed'].mean()
        
        # Inventory turnover = sum(cons)/avg(soh)
        d['inventory_turn_rate'] = x['Dispensed'].rolling(12).sum()/x['Closing Stock'].rolling(12).mean()
        
        # Count records
        #d['record_count'] = x['product_code'].shape[0]
        
        # Most recent record
        #x = x.sort_values(by='Period')
        #d['Last Record'] = x['Period'].iloc[-1]
        
        # Return d as a series
        return pd.Series(d, index = ['inventory_turn_rate'])

    def stock_transform(stock_df):
        stock_df = stock_df.sort_values(by = ['Year','Month'])
        metric_df = stock_df.groupby(['Year','Month','Product Code','Facility Code']).apply(lambda x: groupbyfn(x)).reset_index()
        stock_df = stock_df.merge(metric_df, on = ['Year','Month','Product Code', 'Facility Code'], how = 'left')

        stock_df = stock_df.rename(columns = {'Year':'calendar_year','Month':'month_number','Product Code':'product_code','Facility Code':'facility_code','OBL':'obl',
                                    'Received':'received','Dispensed':'dispensed','Adjusted':'adjusted','Stock Out Days':'stock_out_days',
                                    'Closing Stock':'closing_stock','AMC':'amc','MOS':'mos'})
        
        stock_df = stock_df[['calendar_year','month_number','product_code','facility_code','obl','received','dispensed','adjusted','stock_out_days','closing_stock','amc','mos']]
        stock_df.fillna(0, inplace=True)
        stock_df['create_date'] = datetime.now()
        stock_df['creator_id'] = 'admin'
        stock_df['last_modified_date'] = datetime.now()
        stock_df['last_modified_by'] = 'admin'
        stock_df['source_id'] = 'webapp'
        stock_df['current_ind'] = 'A'
        return stock_df

    def send_email2(sender='bigdata@ghsc-psm.org',to='wirshad@ghsc-psm.org', subject='Transformation and Load Process Completed', body= 'Transformation and Load process completed. Please review the attched log files for any exceptions.', attach= log_path/error_log_file, attach1=log_path/process_log_file):
        cmd = 'echo "{b}" | mailx -r "{sender}" -s "{s}" -a "{a}" -a "{a1}" "{to}" '.format(b=body,sender=sender, s=subject, a=attach, a1=attach1, to=to)
        # print(cmd)
        os.system(cmd)



    error_log = open(log_path / error_log_file, 'w')
    facility_new, facility_status_new, product_new, stock_new,facility_path, facility_status_path, product_path, stock_detail_path, e = get_extracts(folder_path)
    if e:
        print(*e, sep = '\n', end = '', file = error_log)
    #print(stock_new.iloc[0])
    facility_new['PPM'] = facility_new['PPM'].astype(str)
    facility_new['Facility Phone'] = facility_new['Facility Phone'].astype(str)
    facility_new['Facility Fax'] = facility_new['Facility Fax'].astype(str)
    facility_new['Facility Email'] = facility_new['Facility Email'].astype(str)
    facility_new = facility_new.merge(fac_map, how = 'left', left_on = ['District','Facility Code'], right_on = ['district','facility_code'])

    facility_new = facility_new.drop(columns = ['district','facility_code'])
    facility_new = facility_new[['Facility Code', 'Facility Name', 'Facility Type', 'Region Name',
    'District','demo_district', 'Owner Type', 'PPM', 'Service Area', 'Facility Address',
    'Assigned Group', 'Facility Phone', 'Facility Fax', 'Facility Email',
    'Latitude', 'Longitude']]
    facility_new['create_date'] = datetime.now()
    product_new['create_date'] = datetime.now()
    facility_new['creator_id'] = 'admin'
    product_new['creator_id'] = 'admin'
    facility_new['last_modified_date'] = datetime.now()
    product_new['last_modified_date'] = datetime.now()
    facility_new['last_modified_by'] = 'admin'
    product_new['last_modified_by'] = 'admin'
    facility_new['source_id'] = 'webapp'
    product_new['source_id'] = 'webapp'
    facility_new['current_ind'] = 'A'
    product_new['current_ind'] = 'A'

    facility_status_new.rename(columns = {'Entered':'entered_ind','Submitted':'submitted_ind','Published':'published_ind',
    'Year':'calendar_year','Month':'month_number', 'Facility Code':'facility_code','Entry Date':'entry_date','Submitted Date':'submitted_date',
    'Published Date':'published_date'}, inplace = True)
    #facility_status_new['entry_date'] = facility_status_new['entry_date'].fillna(value = None)
    #facility_status_new['submitted_date'] = facility_status_new['submitted_date'].fillna(value = None)
    #facility_status_new['published_date'] = facility_status_new['published_date'].fillna(value = None)
    facility_status_new = facility_status_new.where(pd.notnull(facility_status_new), None)
    facility_status_new['create_date'] = datetime.now()
    facility_status_new['creator_id'] = 'admin'
    facility_status_new['last_modified_data'] = datetime.now()
    facility_status_new['source_id'] = 'webapp'
    facility_status_new['current_ind'] = 'A'
    facility_status_new['last_modified_by'] = 'admin'

    # Log file
    info_log = open(log_path / process_log_file, 'w')
    sys.stdout = info_log
    print(facility_path)
    print(facility_status_path)
    print(product_path)
    print(stock_detail_path)
    print('\n')

    product_new['bKeyItem'] = product_new['bKeyItem'].astype(str)
    try:
        inserted, deactivated, updated = reference_update(facility_df, facility_new, 'facility_code',facility)
        print("Facility Table Updated: ")
        print("Completed on:", str(datetime.now()))
        print('Rows inserted in Facility: ',str(inserted))
        print('Rows deactivated in Facility: ', str(deactivated))
        print('Rows updated in Facility: ', str(updated))
        print('\n')
    except:
        e = sys.exc_info()[1]
        print('Error in facility table', file = error_log)
        print(e, end = '', file = error_log)
    
    try:
        inserted, deactivated, updated = reference_update(product_df, product_new, 'product_code', product)
        print("Product Table Updated: ")
        print("Completed on:", str(datetime.now()))
        print('Rows inserted in Product: ',str(inserted))
        print('Rows deactivated in Product: ', str(deactivated))
        print('Rows updated in Product: ', str(updated))
        print('\n')
    except:
        e = sys.exc_info()[1]
        print('Error in product table', file = error_log)
        print(e, end = '', file = error_log)

    try:
        inserted, deactivated, updated = reference_update(facility_status_df, facility_status_new, ['calendar_year','month_number','facility_code'], facility_status)
        print("Facility Status Table Updated: ")
        print("Completed on:", str(datetime.now()))
        print('Rows inserted in Facility Status: ',str(inserted))
        print('Rows deactivated in Facility Status: ', str(deactivated))
        print('Rows updated in Facility Status: ', str(updated))
        print('\n')
    except:
        e = sys.exc_info()
        print('Error in facility status table', file = error_log)
        print(e, end = '', file = error_log)
    
    stock_df = stock_transform(stock_new)
    try:
        insert_db(stock_detail, stock_df)
        stock_length = len(stock_df.index)
        print("Stock Detail Table Updated: ")
        print("Completed on:", str(datetime.now()))
        print('Rows inserted: ', str(stock_length))

        inserted, deactivated, updated = reference_update(stock_detail_df, stock_df, ['calendar_year','month_number','facility_code','product'], stock_detail)
        print("Stock Detail Table Updated: ")
        print("Completed on:", str(datetime.now()))
        print('Rows inserted in Stock Detail: ',str(inserted))
        print('Rows deactivated in Stock Detail: ', str(deactivated))
        print('Rows updated in Stock Detail: ', str(updated))
        print('\n')

    except:
        e = sys.exc_info()[1]
        print('Error in stock detail table', file = error_log)
        print(e, end = '', file = error_log)

    
    info_log.close()    
    error_log.close()
    

    

