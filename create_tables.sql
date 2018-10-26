CREATE TABLE IF NOT EXISTS site (
	site_id ,
	site_location GEOGRAPHY(POINT, 4326),
	site_name VARCHAR NULL,
	address VARCHAR NULL,
	zipcode VARCHAR NULL,
	state CHAR(2)
);

CREATE TABLE IF NOT EXISTS unit (
	unit_id PRIMARY KEY,
	program_id,
	site_id,
	unit_location GEOGRAPHY(POLYGON, 4326)
);

CREATE TABLE IF NOT EXISTS well (
	well_id PRIMARY KEY,
	well_location GEOGRAPHY(POINT, 4326),
	site_id ,
	unit_id
);	

CREATE TABLE IF NOT EXISTS parameters (
	param_id PRIMARY KEY,
	description,
	epa_equivalence,
	characteristic_name,
	measurement_code,
	sample_frac,
	stat_basis,
	time_basis,
	size_basis,
	CONSTRAINT param_id_check CHECK (param_id SIMILAR TO '[[:digit:]]{5}')
);

CREATE TABLE IF NOT EXISTS lab_analysis (
        lab_id VARCHAR,
        sample_id VARCHAR NOT NULL,
        sample_date DATE,
	media_matrix VARCHAR,
	prep_method VARCHAR,
	analysis_method VARCHAR,
        param_id VARCHAR(5) NOT NULL,
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
        analysis_comment VARCHAR,
	CONSTRAINT analysis_param_id_check CHECK (param_id SIMILAR TO '[[:digit:]]{5}')
);
