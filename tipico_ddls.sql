--------------------------------------------------CREATE STAGING TABLES--------------------------------------------------
drop table if exists timothy_chan.stg_event;
CREATE TABLE IF NOT EXISTS timothy_chan.stg_event
(
	root_id integer encode lzo
	,start_time TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,message_time TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,match_state VARCHAR(255)   ENCODE lzo
	,sport_type VARCHAR(255)   ENCODE lzo
	,status VARCHAR(255)   ENCODE lzo
	,market_count integer encode lzo
	,name VARCHAR(255)   ENCODE lzo
	,"type" VARCHAR(255)   ENCODE lzo
	,last_modified_time TIMESTAMP encode lzo
)
DISTSTYLE AUTO
;

drop table if exists timothy_chan.stg_market;
CREATE TABLE IF NOT EXISTS stg_market
(
	root_id integer encode lzo
	,market_id VARCHAR(36)   ENCODE lzo
	,name VARCHAR(255)   ENCODE lzo
	,"type" VARCHAR(255)   ENCODE lzo
	,"parameters" VARCHAR(255)   ENCODE lzo
	,status VARCHAR(255)   ENCODE lzo
	,most_balanced_line BOOLEAN   ENCODE RAW
	,is_sgp_eligable BOOLEAN   ENCODE RAW
)
DISTSTYLE AUTO
;

drop table if exists timothy_chan.stg_outcome;
CREATE TABLE IF NOT exists stg_outcome
(
	root_id integer encode lzo
	,market_id varchar(255) encode lzo
	,outcome_id VARCHAR(255)   ENCODE lzo
	,name VARCHAR(255)   ENCODE lzo
	,traded_ind bool   
	,true_odds DECIMAL(10,2)   ENCODE az64
	,format_decimal DECIMAL(10,2)   ENCODE az64
	,format_american DECIMAL(10,2)   ENCODE az64
	,status VARCHAR(7)   ENCODE lzo
)
DISTSTYLE AUTO
;

drop table if exists timothy_chan.stg_event_dtls;
CREATE TABLE IF NOT EXISTS stg_event_dtls
(	
	root_id INTEGER  encode lzo
	,block_cashout BOOLEAN   ENCODE RAW
	,long_term_event_type VARCHAR(255)   ENCODE lzo
	,outright_type VARCHAR(255)   ENCODE lzo
	,sub_group_name_key VARCHAR(255)   ENCODE lzo
	,sub_group_id_key INTEGER   ENCODE az64
	,tie_break VARCHAR(255)   ENCODE lzo
	,best_of_sets VARCHAR(255)   ENCODE lzo
)
DISTSTYLE AUTO
;


root_id,
start_time,
message_time,
match_state,
sport_type,
status,
market_count,
"name",
"type",
last_modified_time

drop table if exists timothy_chan.stg_participant;
CREATE TABLE IF NOT EXISTS stg_participant
(
	root_id integer encode lzo
	,participant_id INTEGER   ENCODE az64
	,name VARCHAR(255)   ENCODE lzo
	,"position" VARCHAR(25)   ENCODE lzo
	,abbreviation VARCHAR(25)   ENCODE lzo
)
DISTSTYLE AUTO
;

drop table if exists timothy_chan.stg_specifier;
CREATE TABLE IF NOT EXISTS timothy_chan.stg_specifier
(
	"key" VARCHAR(255)   ENCODE lzo
	,value VARCHAR(255)   ENCODE lzo
	,"type" VARCHAR(255)   ENCODE lzo
)
DISTSTYLE AUTO
;
--------------------------------------------------END OF CREATE STAGING TABLES--------------------------------------------------


--------------------------------------------------CREATE DIM TABLES--------------------------------------------------
drop table if exists timothy_chan.dim_event;
CREATE TABLE IF NOT EXISTS timothy_chan.dim_event
(
	root_id integer encode lzo
	,start_time TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,message_time TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,match_state VARCHAR(255)   ENCODE lzo
	,sport_type VARCHAR(255)   ENCODE lzo
	,status VARCHAR(255)   ENCODE lzo
	,market_count integer encode lzo
	,name VARCHAR(255)   ENCODE lzo
	,"type" VARCHAR(255)   ENCODE lzo
	,last_modified_time TIMESTAMP encode lzo
)
DISTSTYLE AUTO
;

drop table if exists timothy_chan.dim_market;
CREATE TABLE IF NOT EXISTS timothy_chan.dim_market
(
	root_id integer encode lzo
	,market_id VARCHAR(36)   ENCODE lzo
	,name VARCHAR(255)   ENCODE lzo
	,"type" VARCHAR(255)   ENCODE lzo
	,"parameters" VARCHAR(255)   ENCODE lzo
	,status VARCHAR(255)   ENCODE lzo
	,most_balanced_line BOOLEAN   ENCODE RAW
	,is_sgp_eligable BOOLEAN   ENCODE RAW
)
DISTSTYLE AUTO
;

drop table if exists timothy_chan.dim_outcome;
CREATE TABLE IF NOT EXISTS timothy_chan.dim_outcome
(
	root_id integer encode lzo
	,market_id varchar(255) encode lzo
	,outcome_id VARCHAR(255)   ENCODE lzo
	,name VARCHAR(255)   ENCODE lzo
	,traded_ind bool   
	,true_odds DECIMAL(10,2)   ENCODE az64
	,format_decimal DECIMAL(10,2)   ENCODE az64
	,format_american DECIMAL(10,2)   ENCODE az64
	,status VARCHAR(7)   ENCODE lzo
)
DISTSTYLE AUTO
;

drop table if exists timothy_chan.dim_event_dtls;
CREATE TABLE IF NOT EXISTS timothy_chan.dim_event_dtls
(	
	root_id INTEGER  encode lzo
	,block_cashout BOOLEAN   ENCODE RAW
	,long_term_event_type VARCHAR(255)   ENCODE lzo
	,outright_type VARCHAR(255)   ENCODE lzo
	,sub_group_name_key VARCHAR(255)   ENCODE lzo
	,sub_group_id_key INTEGER   ENCODE az64
	,tie_break VARCHAR(255)   ENCODE lzo
	,best_of_sets VARCHAR(255)   ENCODE lzo
)
DISTSTYLE AUTO
;

drop table if exists timothy_chan.dim_participant;
CREATE TABLE IF NOT EXISTS timothy_chan.dim_participant
(
	root_id integer encode lzo
	,participant_id INTEGER   ENCODE az64
	,name VARCHAR(255)   ENCODE lzo
	,"position" VARCHAR(25)   ENCODE lzo
	,abbreviation VARCHAR(25)   ENCODE lzo
)
DISTSTYLE AUTO
;

drop table if exists timothy_chan.dim_specifier;
CREATE TABLE IF NOT EXISTS timothy_chan.dim_specifier
(
	"key" VARCHAR(255)   ENCODE lzo
	,value VARCHAR(255)   ENCODE lzo
	,"type" VARCHAR(255)   ENCODE lzo
)
DISTSTYLE AUTO
;