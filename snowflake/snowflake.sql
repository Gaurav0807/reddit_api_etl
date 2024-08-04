

create database snowflake_integration;

create schema ingestion_layer;

create or replace STORAGE INTEGRATION aws_s3_integration
type=external_stage
storage_provider='s3'
enabled=true
storage_aws_role_arn='' -- pull this from aws_role_arn
storage_allowed_locations=('s3://snowflake-integration-bucket-data/');

show integrations;

desc integration aws_s3_integration;

grant usage on integration aws_s3_integration to role accountadmin;


create or replace file format s3_bucket
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
NULL_IF = ('')
EMPTY_FIELD_AS_NULL = TRUE;

show file formats;

desc file format s3_bucket;

create or replace stage s3_external_stage
storage_integration=aws_s3_integration
file_format=s3_bucket
url='s3://snowflake-integration-bucket-data/raw/';


list @s3_external_stage;

remove @s3_external_stage/reddit_20240803.csv;



CREATE OR REPLACE EXTERNAL TABLE snowflake_integration.ingestion_layer.reddit_data(
  id VARCHAR(1000) AS (VALUE:"c1"::VARCHAR(1000)) NULL,
  title VARCHAR(1000) AS (VALUE:"c2"::VARCHAR(1000)) NULL,
  Topic VARCHAR(1000) AS (VALUE:"c3"::VARCHAR(1000)) NULL,
  score INTEGER AS (VALUE:"c4"::INTEGER) NULL,
  num_comments VARCHAR(1000) AS (VALUE:"c5"::VARCHAR(1000)) NULL,
  author VARCHAR(1000) AS (VALUE:"c6"::VARCHAR(1000)) NULL,
  created_utc TIMESTAMP AS (VALUE:"c7"::TIMESTAMP) NULL,
  url VARCHAR(1000) AS (VALUE:"c8"::VARCHAR(1000)) NULL,
  Self_Text_Description VARCHAR(1000) AS (VALUE:"c9"::VARCHAR(1000)) NULL,
  upvote_ratio NUMERIC AS (VALUE:"c10"::NUMERIC) NULL,
  over_18 BOOLEAN AS (VALUE:"c11"::BOOLEAN) NULL,
  edited BOOLEAN AS (VALUE:"c12"::BOOLEAN) NULL,
  spoiler BOOLEAN AS (VALUE:"c13"::BOOLEAN) NULL,
  stickied BOOLEAN AS (VALUE:"c14"::BOOLEAN) NULL
)
LOCATION = @s3_external_stage
FILE_FORMAT = (FORMAT_NAME = s3_bucket);



select * from snowflake_integration.ingestion_layer.reddit_data





