import os
import sys
import requests
import shutil
from pathlib import Path
from datetime import datetime, date

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
    exec(open("transformation_load.py").read())

