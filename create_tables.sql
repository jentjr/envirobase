CREATE TABLE IF NOT EXISTS site (
	site_id SERIAL PRIMARY KEY,
	site_geog GEOGRAPHY(POINT, 4326),
	site_name VARCHAR NULL,
	address VARCHAR NULL,
	zipcode VARCHAR NULL,
	state CHAR(2)
);

CREATE TABLE IF NOT EXISTS unit (
	unit_id SERIAL PRIMARY KEY,
	unit_geog GEOGRAPHY(POLYGON, 4326),
	site_id INTEGER REFERENCES site(site_id)
);

CREATE TABLE IF NOT EXISTS location (
	location_id VARCHAR PRIMARY KEY,
	location_geog GEOGRAPHY(POINT, 4326),
	site_id INTEGER REFERENCES site(site_id),
	unit_id INTEGER REFERENCES unit(unit_id)
);	

CREATE TABLE IF NOT EXISTS parameters (
	param_cd CHAR(5) PRIMARY KEY,
	CONSTRAINT param_cd_check CHECK (param_cd SIMILAR TO '[[:digit:]]{5}'),
	description VARCHAR,
	epa_equivalence VARCHAR,
	characteristicname VARCHAR,
	measureunitcode VARCHAR,
	resultsamplefraction VARCHAR,
	resulttemperaturebasis VARCHAR,
	resultstatisticalbasis VARCHAR,
	resulttimebasis VARCHAR,
	resultweightbasis VARCHAR,
	resultparticlesizebasis VARCHAR
);

CREATE TABLE IF NOT EXISTS sample_results (
        lab_id VARCHAR,
        location_id VARCHAR NOT NULL REFERENCES location(location_id),
	param_cd VARCHAR(5) NOT NULL REFERENCES parameters(param_cd),
        sample_date DATE NOT NULL,
	media_matrix VARCHAR,
	prep_method VARCHAR,
	analysis_method VARCHAR,
	analysis_flag CHAR(1),
        analysis_result REAL NULL,
        analysis_unit VARCHAR NOT NULL,
        detection_limit REAL,
        prac_quant_limit REAL,
	min_detect_activity REAL,
	comb_stand_unc REAL,
	analysis_qualifier CHAR(1),
	disclaimer VARCHAR,
	analysis_date DATE NULL,
	order_commment VARCHAR,
        analysis_comment VARCHAR
);

COPY param_codes FROM 'param_codes.csv' WITH (FORMAT csv);
