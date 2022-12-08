
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

from datetime import datetime

import pandas as pd
from app import engine

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


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

class product(Base):
    __tablename__ = "product"
    #__table_args__ = {'schema':'bigdata'}
    product_code =      Column(String(100), primary_key = True)
    product_name =      Column(String(100))
    short_name =        Column(String(100))
    key_product =       Column(Boolean)
    product_subgroup =  Column(String(100))

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

class priority_input(Base):
    __tablename__ = "priority_input"
    __table_args__ = {'schema':'bigdata'}
    id =                    Column(Integer, primary_key = True)
    preg_priority =         Column(Integer)
    preg_weight =           Column(Float(5,2))
    preg_score =            Column(Integer)
    preg_th_low_med =       Column(Float(5,2))
    preg_th_med_high =      Column(Float(5,2))
    umm_priority =          Column(Integer)
    umm_weight =            Column(Float(5,2))
    umm_score =             Column(Integer)
    umm_th_low_med =        Column(Float(5,2))
    umm_th_med_high =       Column(Float(5,2))
    ds_priority =           Column(Integer)
    ds_weight =             Column(Float(5,2))
    ds_score =              Column(Integer)
    ds_th_low_med =         Column(Float(5,2))
    ds_th_med_high =        Column(Float(5,2))
    umn_priority =          Column(Integer)
    umn_weight =            Column(Float(5,2))
    umn_score =             Column(Integer)
    umn_th_low_med =        Column(Float(5,2))
    umn_th_med_high =       Column(Float(5,2))
    pop_priority =          Column(Integer)
    pop_weight =            Column(Float(5,2))
    pop_score =             Column(Integer)
    pop_th_low_med =        Column(Float(5,2))
    pop_th_med_high =       Column(Float(5,2))
    create_date =           Column(DateTime)
    creator_id =            Column(String(100))
    last_modified_date =    Column(DateTime)
    last_modified_by =      Column(String(100))
    source_id =             Column(String(100))
    current_ind =           Column(String(1))
    bigdata_txt =           Column(String(100))

class demographic(Base):
    __tablename__ = "demographic"
    __table_args__ = {'schema':'bigdata'}
    demo_district =      Column(String(100), primary_key = True)
    region_name =       Column(String(100))
    area =              Column(Float(16,8))
    preg_min =          Column(Float(16,8))
    preg_max =          Column(Float(16,8))
    preg_range =        Column(Float(16,8))
    preg_median =       Column(Float(16,8))
    preg_mean =         Column(Float(16,8))
    preg_count =        Column(Integer)
    preg_sum =          Column(Float(16,8))
    preg_std =          Column(Float(16,8))
    umm_min =           Column(Float(16,8))
    umm_max =           Column(Float(16,8))
    umm_range =         Column(Float(16,8))
    umm_median =        Column(Float(16,8))
    umm_mean =          Column(Float(16,8))
    umm_count =         Column(Integer)
    umm_sum =           Column(Float(16,8))
    umm_std =           Column(Float(16,8))
    ds_min =            Column(Float(16,8))
    ds_max =            Column(Float(16,8))
    ds_range =          Column(Float(16,8))
    ds_median =         Column(Float(16,8))
    ds_mean =           Column(Float(16,8))
    ds_count =          Column(Integer)
    ds_sum =            Column(Float(16,8))
    ds_std =            Column(Float(16,8))
    umn_min =           Column(Float(16,8))
    umn_max =           Column(Float(16,8))
    umn_range =         Column(Float(16,8))
    umn_median =        Column(Float(16,8))
    umn_mean =          Column(Float(16,8))
    umn_count =         Column(Integer)
    umn_sum =           Column(Float(16,8))
    umn_std =           Column(Float(16,8))
    pop_min =           Column(Float(16,8))
    pop_max =           Column(Float(16,8))
    pop_range =         Column(Float(16,8))
    pop_median =        Column(Float(16,8))
    pop_mean =          Column(Float(16,8))
    pop_count =         Column(Integer)
    pop_sum =           Column(Float(16,8))
    pop_std =           Column(Float(16,8))
    pop_density =       Column(Float(16,8))
    preg_per_sq_km =    Column(Float(16,8))

#Initialize a priority
def create_priority(priority_df, class_name):
    if(priority_df.empty == True):
        new_row = {'id':1, 'preg_priority':3, 'preg_weight':2, 'preg_score':10,'preg_th_low_med':49.12,'preg_th_med_high':57.04,
        'umm_priority':2, 'umm_weight':2.5, 'umm_score':10, 'umm_th_low_med':0.035, 'umm_th_med_high': 0.082,
        'umn_priority':1, 'umn_weight':3, 'umn_score':10, 'umn_th_low_med':0.179, 'umn_th_med_high':0.283,
        'pop_priority':4, 'pop_weight':1.5, 'pop_score':10, 'pop_th_low_med':13.48, 'pop_th_med_high':49.86,
        'ds_priority':5, 'ds_weight':1, 'ds_score':10, 'ds_th_low_med':0.132, 'ds_th_med_high':0.211,
        'create_date': datetime.now(),'creator_id': 'admin','last_modified_date': datetime.now(),'last_modified_by': 'admin',
        'source_id': 'webapp','current_ind': 'A'}
        priority_df = pd.DataFrame(data = new_row, index = [0])
        session.bulk_insert_mappings(class_name, priority_df.to_dict(orient="records"))
        session.commit()
    
    return priority_df


def insert_db(class_name, new_df):
    """Inserts data into DB table

    Args:
        class_name (String): Name of table
        new_df (dataframe): Table containing data to be inserted
    """
    session.bulk_insert_mappings(class_name, new_df.to_dict(orient="records"))
    session.commit()

def update_priority(class_name, col_id, update_df):
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
    session.commit()

facility_query = session.query(facility)
facility_df = pd.read_sql(facility_query.statement, session.bind)

priority_query = session.query(priority_input)
priority_df = pd.read_sql(priority_query.statement, session.bind)

priority_df = create_priority(priority_df, priority_input)

product_query = session.query(product)
product_df = pd.read_sql(product_query.statement, session.bind)

stock_query = session.query(stock_detail)
stock_df = pd.read_sql(stock_query.statement, session.bind)

demo_query = session.query(demographic)
demographic = pd.read_sql(demo_query.statement, session.bind)