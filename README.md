# to3-big-data

## Background
The Big Data Tool is a cloud-hosted solution including a dashboard in streamlit and an ETL process 

The tool combines demographic indicator data for a given country and inventory data for that country to identify target facilities for actions. 

Demographic data on family planning indicators comes from publicly available sources. Inventory data comes from the countries supply chain data system (such as an eLMIS).

See the Implementation Guide in the Documentation folder for information on the infrastructure required to stand up an instance of the tool. The documentation also contains an Installation Guide,  Maintenance Guide and a User Guide.



### ETL scripts

autmated_process.py
bigdata db ddl.sql
db_backup_scheduled.sh
extract_process.py
query.py
transformation_load.py
transformation.py

### Streamlit Application scripts

webapp.py 
streamlit-app folder

## To Run the Streamlit App

>> streamlit run webapp.py
