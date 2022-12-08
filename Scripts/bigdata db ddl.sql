-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.3-alpha
-- PostgreSQL version: 12.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- object: wirshad | type: ROLE --
-- DROP ROLE IF EXISTS wirshad;
CREATE ROLE wirshad WITH 
	SUPERUSER
	INHERIT
	LOGIN
	ENCRYPTED PASSWORD '********';
-- ddl-end --

-- object: dbadmin | type: ROLE --
-- DROP ROLE IF EXISTS dbadmin;
CREATE ROLE dbadmin WITH 
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	LOGIN
	ENCRYPTED PASSWORD '********';
-- ddl-end --

-- object: dbro | type: ROLE --
-- DROP ROLE IF EXISTS dbro;
CREATE ROLE dbro WITH 
	INHERIT
	LOGIN
	ENCRYPTED PASSWORD '********';
-- ddl-end --

-- object: dbrw | type: ROLE --
-- DROP ROLE IF EXISTS dbrw;
CREATE ROLE dbrw WITH 
	INHERIT
	LOGIN
	ENCRYPTED PASSWORD '********';
-- ddl-end --

-- object: dbadmin_cp | type: ROLE --
-- DROP ROLE IF EXISTS dbadmin_cp;
CREATE ROLE dbadmin_cp WITH 
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	LOGIN
	ENCRYPTED PASSWORD '********';
-- ddl-end --


-- Database creation must be done outside a multicommand file.
-- These commands were put in this file only as a convenience.
-- -- object: bigdata | type: DATABASE --
-- -- DROP DATABASE IF EXISTS bigdata;
-- CREATE DATABASE bigdata
-- 	ENCODING = 'UTF8'
-- 	LC_COLLATE = 'en_US.UTF-8'
-- 	LC_CTYPE = 'en_US.UTF-8'
-- 	TABLESPACE = pg_default
-- 	OWNER = postgres;
-- -- ddl-end --
-- 

-- object: bigdata | type: SCHEMA --
-- DROP SCHEMA IF EXISTS bigdata CASCADE;
CREATE SCHEMA bigdata;
-- ddl-end --
ALTER SCHEMA bigdata OWNER TO dbadmin;
-- ddl-end --

-- object: stgdata | type: SCHEMA --
-- DROP SCHEMA IF EXISTS stgdata CASCADE;
CREATE SCHEMA stgdata;
-- ddl-end --
ALTER SCHEMA stgdata OWNER TO dbadmin;
-- ddl-end --

SET search_path TO pg_catalog,public,bigdata,stgdata;
-- ddl-end --

-- object: public.user_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.user_id_seq CASCADE;
CREATE SEQUENCE public.user_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --
ALTER SEQUENCE public.user_id_seq OWNER TO dbadmin;
-- ddl-end --

-- object: bigdata.product | type: TABLE --
-- DROP TABLE IF EXISTS bigdata.product CASCADE;
CREATE TABLE bigdata.product (
	product_code varchar(24) NOT NULL,
	product_name varchar(100) NOT NULL,
	short_name varchar(60),
	key_product char(1),
	product_subgroup varchar(24),
	create_date timestamp NOT NULL,
	creator_id varchar(24) NOT NULL,
	last_modified_date timestamp NOT NULL,
	last_modified_by varchar(24) NOT NULL,
	source_id varchar(24) NOT NULL,
	current_ind varchar(1) NOT NULL,
	bigdata_txt varchar(1000),
	CONSTRAINT product_pk PRIMARY KEY (product_code)

);
-- ddl-end --
COMMENT ON COLUMN bigdata.product.product_code IS E'Unique identifier for each product.';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.product_name IS E'Product name';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.short_name IS E'Product short name';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.key_product IS E'Indicator (1 or 0) is used to identify if the product is an essential product. value 1 is essential, 0 is not essential.';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.product_subgroup IS E'Product subgroup Example Family Planning (FP)';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.create_date IS E'Timestamp the record is created.';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.creator_id IS E'User or application ID who created the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.last_modified_date IS E'Timestamp when the record was last modified.';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.last_modified_by IS E'User or application ID who modified the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.source_id IS E'ID of the source system (eLMIS, Worldpop, DHS, file, etc.)';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.current_ind IS E'A Boolean field used to indicate if the record is active or non-active (A/N).';
-- ddl-end --
COMMENT ON COLUMN bigdata.product.bigdata_txt IS E'Text field, a place holder for internal database comments.';
-- ddl-end --
ALTER TABLE bigdata.product OWNER TO dbadmin;
-- ddl-end --

-- object: bigdata.facility | type: TABLE --
-- DROP TABLE IF EXISTS bigdata.facility CASCADE;
CREATE TABLE bigdata.facility (
	facility_code varchar(24) NOT NULL,
	facility_name varchar(100) NOT NULL,
	facility_type varchar(40),
	region_name varchar(100),
	district varchar(100),
	demo_district varchar(24),
	owner_type varchar(100),
	service_area varchar(100),
	facility_address varchar(100),
	assigned_group varchar(100),
	facility_phone varchar(24),
	facility_fax varchar(24),
	facility_email varchar(40),
	latitude decimal(11,8),
	longitude decimal(11,8),
	create_date timestamp NOT NULL,
	creator_id varchar(24) NOT NULL,
	last_modified_date timestamp NOT NULL,
	last_modified_by varchar(24) NOT NULL,
	source_id varchar(24) NOT NULL,
	current_ind varchar(1) NOT NULL,
	bigdata_txt varchar(1000),
	CONSTRAINT facility_pk PRIMARY KEY (facility_code)

);
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.facility_code IS E'A unique code that is used to reference a facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.facility_name IS E'The facility name is the official name of a facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.facility_type IS E'Facility type: Central warehouse, Regional warehouse, District warehouse, Health facility';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.region_name IS E'Region name of the facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.district IS E'District of the facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.owner_type IS E'Owner type: Public or Private';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.service_area IS E'Service Area: Urban, Rural';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.facility_address IS E'Address of the facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.assigned_group IS E'Project assigned: Malaria, FP, MCH, HIV & AIDS';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.facility_phone IS E'Telephone number of the facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.facility_fax IS E'Fax number of the facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.facility_email IS E'Email address of the facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.latitude IS E'The latitude of the facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.longitude IS E'The longitude of the facility.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.create_date IS E'Timestamp the record is created.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.creator_id IS E'User or application ID who created the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.last_modified_date IS E'Timestamp when the record was last modified.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.last_modified_by IS E'User or application ID who modified the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.source_id IS E'ID of the source system (eLMIS, Worldpop, DHS, file, etc.)';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.current_ind IS E'A Boolean field used to indicate if the record is active or non-active (A/N).';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility.bigdata_txt IS E'Text field, a place holder for internal database comments.';
-- ddl-end --
ALTER TABLE bigdata.facility OWNER TO dbadmin;
-- ddl-end --

-- object: bigdata.stock_detail | type: TABLE --
-- DROP TABLE IF EXISTS bigdata.stock_detail CASCADE;
CREATE TABLE bigdata.stock_detail (
	facility_code varchar(24) NOT NULL,
	product_code varchar(24) NOT NULL,
	month_number integer NOT NULL,
	calendar_year varchar(4) NOT NULL,
	obl integer,
	received integer,
	dispensed integer,
	adjusted integer,
	stock_out_days integer,
	closing_stock integer,
	amc integer,
	mos decimal(12,5),
	inventory_turn_rate decimal(5,2),
	turn_rate_ind char(1),
	fp_priority_score integer,
	create_date timestamp NOT NULL,
	creator_id varchar(24) NOT NULL,
	last_modified_date timestamp NOT NULL,
	last_modified_by varchar(24) NOT NULL,
	source_id varchar(24) NOT NULL,
	current_ind varchar(1) NOT NULL,
	bigdata_txt varchar(1000)
);
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.obl IS E'Opening balance for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.received IS E'Received stock for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.dispensed IS E'Dispensed quantity for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.adjusted IS E'Adjusted quantity for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.stock_out_days IS E'stock out days for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.closing_stock IS E'Closing_stock quantity for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.amc IS E'Average monthly consumption for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.mos IS E'Months of stock for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.inventory_turn_rate IS E'Inventory turn rate for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.turn_rate_ind IS E'Turn rate indicator for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.fp_priority_score IS E'Family planning priority score for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.create_date IS E'Timestamp the record is created.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.creator_id IS E'User or application ID who created the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.last_modified_date IS E'Timestamp when the record was last modified.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.last_modified_by IS E'User or application ID who modified the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.source_id IS E'ID of the source system (eLMIS, Worldpop, DHS, file, etc.)';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.current_ind IS E'A Boolean field used to indicate if the record is active or non-active (A/N).';
-- ddl-end --
COMMENT ON COLUMN bigdata.stock_detail.bigdata_txt IS E'Text field, a place holder for internal database comments.';
-- ddl-end --
ALTER TABLE bigdata.stock_detail OWNER TO dbadmin;
-- ddl-end --

-- object: product_fk | type: CONSTRAINT --
-- ALTER TABLE bigdata.stock_detail DROP CONSTRAINT IF EXISTS product_fk CASCADE;
ALTER TABLE bigdata.stock_detail ADD CONSTRAINT product_fk FOREIGN KEY (product_code)
REFERENCES bigdata.product (product_code) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: facility_fk | type: CONSTRAINT --
-- ALTER TABLE bigdata.stock_detail DROP CONSTRAINT IF EXISTS facility_fk CASCADE;
ALTER TABLE bigdata.stock_detail ADD CONSTRAINT facility_fk FOREIGN KEY (facility_code)
REFERENCES bigdata.facility (facility_code) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: bigdata.facility_status | type: TABLE --
-- DROP TABLE IF EXISTS bigdata.facility_status CASCADE;
CREATE TABLE bigdata.facility_status (
	calendar_year varchar(4) NOT NULL,
	month_number integer NOT NULL,
	facility_code varchar(24) NOT NULL,
	entered_ind char(1),
	entry_date timestamp,
	submitted_ind varchar(1),
	submitted_date timestamp,
	published_ind varchar(1),
	published_date timestamp,
	create_date timestamp NOT NULL,
	creator_id varchar(24) NOT NULL,
	last_modified_data timestamp NOT NULL,
	last_modified_by varchar(24) NOT NULL,
	source_id varchar(24) NOT NULL,
	current_ind varchar(1) NOT NULL,
	bigdata_txt varchar(1000),
	CONSTRAINT facility_status_pk PRIMARY KEY (facility_code,month_number,calendar_year)

);
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.entered_ind IS E'Indicator (1 or 0) is used to identify if the facility entered their status in the system for the reported period. value 1 is entered , 0 is not entered.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.entry_date IS E'Entry date for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.submitted_ind IS E'Indicator (1 or 0) is used to identify if the facility submitted their status in the system for the reported period. value 1 is submitted , 0 is not submitted.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.submitted_date IS E'Submitted date for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.published_ind IS E'Indicator (1 or 0) is used to identify if the facility pubmished their status in the system for the reported period. value 1 is published , 0 is not published.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.published_date IS E'Pubmished date for the reported period.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.create_date IS E'Timestamp the record is created.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.creator_id IS E'User or application ID who created the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.last_modified_data IS E'Timestamp when the record was last modified.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.last_modified_by IS E'User or application ID who modified the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.source_id IS E'ID of the source system (eLMIS, Worldpop, DHS, file, etc.)';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.current_ind IS E'A Boolean field used to indicate if the record is active or non-active (A/N).';
-- ddl-end --
COMMENT ON COLUMN bigdata.facility_status.bigdata_txt IS E'Text field, a place holder for internal database comments.';
-- ddl-end --
ALTER TABLE bigdata.facility_status OWNER TO dbadmin;
-- ddl-end --

-- object: facility_fk | type: CONSTRAINT --
-- ALTER TABLE bigdata.facility_status DROP CONSTRAINT IF EXISTS facility_fk CASCADE;
ALTER TABLE bigdata.facility_status ADD CONSTRAINT facility_fk FOREIGN KEY (facility_code)
REFERENCES bigdata.facility (facility_code) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: bigdata.date | type: TABLE --
-- DROP TABLE IF EXISTS bigdata.date CASCADE;
CREATE TABLE bigdata.date (
	month_number integer NOT NULL,
	month_name varchar(24) NOT NULL,
	calendar_quarter varchar(2) NOT NULL,
	calendar_year varchar(4) NOT NULL,
	fiscal_quarter varchar(2) NOT NULL,
	fiscal_year varchar(4) NOT NULL,
	create_date timestamp NOT NULL,
	creator_id varchar(24) NOT NULL,
	last_modified_date timestamp NOT NULL,
	last_modified_by varchar(24) NOT NULL,
	source_id varchar(24) NOT NULL,
	current_ind varchar(1) NOT NULL,
	bigdata_txt varchar(1000),
	CONSTRAINT date_pk PRIMARY KEY (month_number,calendar_year)

);
-- ddl-end --
COMMENT ON COLUMN bigdata.date.month_number IS E'Month Number: 1, 2, 3';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.month_name IS E'Month Name: January, February, March';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.calendar_quarter IS E'Month Quarter: Q1, Q2, Q3';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.calendar_year IS E'Calendar Year: 2019, 2020, 2021';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.fiscal_quarter IS E'Fiscal Quarter: Q1, Q2, Q3';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.fiscal_year IS E'Fiscal Year: 2019, 2020, 2021';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.create_date IS E'Timestamp the record is created.';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.creator_id IS E'User or application ID who created the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.last_modified_date IS E'Timestamp when the record was last modified.';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.last_modified_by IS E'User or application ID who modified the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.source_id IS E'ID of the source system (eLMIS, Worldpop, DHS, file, etc.)';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.current_ind IS E'A Boolean field used to indicate if the record is active or non-active (A/N).';
-- ddl-end --
COMMENT ON COLUMN bigdata.date.bigdata_txt IS E'Text field, a place holder for internal database comments.';
-- ddl-end --
ALTER TABLE bigdata.date OWNER TO dbadmin;
-- ddl-end --

-- object: date_fk | type: CONSTRAINT --
-- ALTER TABLE bigdata.stock_detail DROP CONSTRAINT IF EXISTS date_fk CASCADE;
ALTER TABLE bigdata.stock_detail ADD CONSTRAINT date_fk FOREIGN KEY (month_number,calendar_year)
REFERENCES bigdata.date (month_number,calendar_year) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: bigdata.demographic | type: TABLE --
-- DROP TABLE IF EXISTS bigdata.demographic CASCADE;
CREATE TABLE bigdata.demographic (
	demo_district varchar(24) NOT NULL,
	region_name varchar(24),
	area decimal(16,8),
	preg_min decimal(16,8),
	preg_max decimal(16,8),
	preg_range decimal(16,8),
	preg_median decimal(16,8),
	preg_mean decimal(16,8),
	preg_count integer,
	preg_sum decimal(16,8),
	preg_std decimal(16,8),
	umm_min decimal(16,8),
	umm_max decimal(16,8),
	umm_range decimal(16,8),
	umm_median decimal(16,8),
	umm_mean decimal(16,8),
	umm_count integer,
	umm_sum decimal(16,8),
	umm_std decimal(16,8),
	ds_min decimal(16,8),
	ds_max decimal(16,8),
	ds_range decimal(16,8),
	ds_median decimal(16,8),
	ds_mean decimal(16,8),
	ds_count integer,
	ds_sum decimal(16,8),
	ds_std decimal(16,8),
	umn_min decimal(16,8),
	umn_max decimal(16,8),
	umn_range decimal(16,8),
	umn_median decimal(16,8),
	umn_mean decimal(16,8),
	umn_count integer,
	umn_sum decimal(16,8),
	umn_std decimal(16,8),
	pop_min decimal(16,8),
	pop_max decimal(16,8),
	pop_range decimal(16,8),
	pop_median decimal(16,8),
	pop_mean decimal(16,8),
	pop_count integer,
	pop_sum decimal(16,8),
	pop_std decimal(16,8),
	pop_density decimal(16,8),
	preg_per_sq_km decimal(16,8),
	create_date timestamp NOT NULL,
	creator_id varchar(24) NOT NULL,
	last_modifed_date timestamp NOT NULL,
	last_modified_by varchar(24) NOT NULL,
	source_id varchar(24) NOT NULL,
	current_ind varchar(1) NOT NULL,
	bigdata_txt varchar(1000),
	CONSTRAINT demographic_pk PRIMARY KEY (demo_district)

);
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.demo_district IS E'District name';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.region_name IS E'Region name';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.preg_min IS E'Minimum pregnancy';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.preg_max IS E'Maximum pregnancy';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.preg_range IS E'Pregnancy range';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.preg_median IS E'Pregnancy median';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.preg_mean IS E'Pregnancy mean';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.preg_count IS E'Pregnancy count';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.preg_sum IS E'Pregnancy sum';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.preg_std IS E'Pregnancy standard deviation';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umm_min IS E'Minimum Use Modern Method';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umm_max IS E'Maximum Use Modern Method';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umm_median IS E'Use Modern Method median';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umm_mean IS E'Use Modern Method mean';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umm_count IS E'Use Modern Method count';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umm_sum IS E'Use Modern Method sum';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umm_std IS E'Use Modern Method standard deviation';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.ds_min IS E'Minimum demand satisfied';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.ds_max IS E'Maximum demand satisfied';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.ds_range IS E'Demand satisfied range';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.ds_median IS E'Demand satisfied median';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.ds_mean IS E'Demand satisfied mean';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.ds_count IS E'Demand satisfied count';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.ds_sum IS E'Demand satisfied sum';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.ds_std IS E'Demand Satisfied standard deviation';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umn_min IS E'Minimum unmet need';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umn_max IS E'Maximum unmet need';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umn_range IS E'Unmet need range';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umn_median IS E'Unmet need median';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umn_mean IS E'Unmet need mean';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umn_count IS E'Unmet need count';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umn_sum IS E'Unmet need sum';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.umn_std IS E'Unmet need standard deviation';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.pop_min IS E'Minimum population';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.pop_max IS E'Maximum population';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.pop_range IS E'Population range';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.pop_median IS E'Population median';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.pop_mean IS E'Population mean';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.pop_count IS E'Population count';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.pop_sum IS E'Population sum';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.pop_std IS E'Population standard deviation';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.pop_density IS E'Population density';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.preg_per_sq_km IS E'Pregnancy per square kilometer';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.create_date IS E'Timestamp the record is created.';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.creator_id IS E'User or application ID who created the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.last_modifed_date IS E'Timestamp when the record was last modified.';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.last_modified_by IS E'User or application ID who modified the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.source_id IS E'ID of the source system (eLMIS, Worldpop, DHS, file, etc.)';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.current_ind IS E'A Boolean field used to indicate if the record is active or non-active (A/N).';
-- ddl-end --
COMMENT ON COLUMN bigdata.demographic.bigdata_txt IS E'Text field, a place holder for internal database comments.';
-- ddl-end --
ALTER TABLE bigdata.demographic OWNER TO dbadmin;
-- ddl-end --

-- object: bigdata.priority_input | type: TABLE --
-- DROP TABLE IF EXISTS bigdata.priority_input CASCADE;
CREATE TABLE bigdata.priority_input (
	id serial NOT NULL,
	preg_priority integer,
	preg_weight integer,
	preg_score varchar(24),
	preg_th_low_med decimal(5,2),
	preg_th_med_high decimal(5,2),
	umm_priority integer,
	umm_weight integer,
	umm_score varchar(24),
	umm_th_low_med decimal(5,2),
	umm_th_med_high decimal(5,2),
	ds_priority integer,
	ds_weight integer,
	ds_score varchar(24),
	ds_th_low_med decimal(5,2),
	ds_th_mid_high decimal(5,2),
	umn_priority integer,
	umn_weight integer,
	umn_score varchar(24),
	umn_th_low_mid decimal(5,2),
	umn_th_mid_high decimal(5,2),
	pop_priority integer,
	pop_weight integer,
	pop_score varchar(24),
	pop_th_low_med decimal(5,2),
	pop_th_med_high decimal(5,2),
	create_date timestamp NOT NULL,
	creator_id varchar(24) NOT NULL,
	last_modified_date timestamp NOT NULL,
	last_modified_by varchar(24) NOT NULL,
	source_id varchar(24) NOT NULL,
	current_ind char(1) NOT NULL,
	bigdata_txt varchar(1000),
	CONSTRAINT priority_input_pk PRIMARY KEY (id)

);
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.preg_priority IS E'Pregnancy priority';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.preg_weight IS E'Pregnancy weight';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.preg_score IS E'Pregnancy score';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.preg_th_low_med IS E'Pregnancy threshold medium low';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.preg_th_med_high IS E'Pregnancy threshold medium high';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umm_priority IS E'Use Modern Method priority';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umm_weight IS E'Use Modern Method weight';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umm_score IS E'Use Modern Method score';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umm_th_low_med IS E'Use Modern Method threshold medium low';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umm_th_med_high IS E'Use Modern Method threshold medium high';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.ds_priority IS E'Demand satisfied priority';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.ds_weight IS E'Demand satisfied weight';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.ds_score IS E'Demand satisfied score';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.ds_th_low_med IS E'Demand satisfied threshold medium low';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.ds_th_mid_high IS E'Demand satisfied threshold medium high';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umn_priority IS E'Unmet need priority';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umn_weight IS E'Unmet need weight';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umn_score IS E'Unmet need score';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umn_th_low_mid IS E'Unmet need threshold medium low';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.umn_th_mid_high IS E'Unmet need threshold medium high';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.pop_priority IS E'Population priority';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.pop_weight IS E'Population weight';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.pop_score IS E'Population score';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.pop_th_low_med IS E'Population threshold medium low';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.pop_th_med_high IS E'Population threshold medium high';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.create_date IS E'Timestamp the record is created.';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.creator_id IS E'User or application ID who created the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.last_modified_date IS E'Timestamp when the record was last modified.';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.last_modified_by IS E'User or application ID who modified the record.';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.source_id IS E'ID of the source system (eLMIS, Worldpop, DHS, file, etc.)';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.current_ind IS E'A Boolean field used to indicate if the record is active or non-active (A/N).';
-- ddl-end --
COMMENT ON COLUMN bigdata.priority_input.bigdata_txt IS E'Text field, a place holder for internal database comments.';
-- ddl-end --
ALTER TABLE bigdata.priority_input OWNER TO dbadmin;
-- ddl-end --

-- object: date_fk | type: CONSTRAINT --
-- ALTER TABLE bigdata.facility_status DROP CONSTRAINT IF EXISTS date_fk CASCADE;
ALTER TABLE bigdata.facility_status ADD CONSTRAINT date_fk FOREIGN KEY (month_number,calendar_year)
REFERENCES bigdata.date (month_number,calendar_year) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: demographic_fk | type: CONSTRAINT --
-- ALTER TABLE bigdata.facility DROP CONSTRAINT IF EXISTS demographic_fk CASCADE;
ALTER TABLE bigdata.facility ADD CONSTRAINT demographic_fk FOREIGN KEY (demo_district)
REFERENCES bigdata.demographic (demo_district) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: grant_1ec63cf85d | type: PERMISSION --
GRANT SELECT,INSERT,UPDATE,DELETE,TRUNCATE,REFERENCES,TRIGGER
   ON TABLE bigdata.demographic
   TO dbadmin;
-- ddl-end --

-- object: grant_91c6b7fa54 | type: PERMISSION --
GRANT SELECT,INSERT,UPDATE,DELETE,TRUNCATE
   ON TABLE bigdata.demographic
   TO dbrw;
-- ddl-end --

-- object: grant_f237a5ad82 | type: PERMISSION --
GRANT SELECT,INSERT,UPDATE,DELETE,TRUNCATE
   ON TABLE bigdata.priority_input
   TO dbrw;
-- ddl-end --

-- object: grant_5f90fbd4c8 | type: PERMISSION --
GRANT SELECT
   ON TABLE bigdata.priority_input
   TO dbro;
-- ddl-end --

-- object: grant_ff9ebe9516 | type: PERMISSION --
GRANT SELECT,INSERT,UPDATE,DELETE,TRUNCATE
   ON TABLE bigdata.product
   TO dbrw;
-- ddl-end --

-- object: grant_4f30fd4595 | type: PERMISSION --
GRANT SELECT
   ON TABLE bigdata.product
   TO dbro;
-- ddl-end --

-- object: grant_7980144eb7 | type: PERMISSION --
GRANT SELECT,INSERT,UPDATE,DELETE
   ON TABLE bigdata.date
   TO dbrw;
-- ddl-end --

-- object: grant_4595e8b168 | type: PERMISSION --
GRANT SELECT
   ON TABLE bigdata.date
   TO dbro;
-- ddl-end --

-- object: grant_a4fd3d84b2 | type: PERMISSION --
GRANT SELECT,INSERT,UPDATE,DELETE,TRUNCATE
   ON TABLE bigdata.stock_detail
   TO dbrw;
-- ddl-end --

-- object: grant_9c795cfd6e | type: PERMISSION --
GRANT SELECT
   ON TABLE bigdata.stock_detail
   TO dbro;
-- ddl-end --

-- object: grant_9b5a88c4c1 | type: PERMISSION --
GRANT SELECT,INSERT,UPDATE,DELETE,TRUNCATE
   ON TABLE bigdata.facility_status
   TO dbrw;
-- ddl-end --

-- object: grant_f62b822982 | type: PERMISSION --
GRANT SELECT
   ON TABLE bigdata.facility_status
   TO dbro;
-- ddl-end --

-- object: grant_95b6530e9f | type: PERMISSION --
GRANT SELECT,INSERT,UPDATE,DELETE,TRUNCATE
   ON TABLE bigdata.facility
   TO dbrw;
-- ddl-end --

-- object: grant_a16de7f9cb | type: PERMISSION --
GRANT SELECT
   ON TABLE bigdata.facility
   TO dbro;
-- ddl-end --


