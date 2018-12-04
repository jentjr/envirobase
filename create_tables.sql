CREATE TABLE IF NOT EXISTS site (
    site_id SERIAL PRIMARY KEY,
    site_name VARCHAR NOT NULL,
    address VARCHAR NULL,
    city VARCHAR NULL,
    state CHAR(2) NULL,
    zipcode VARCHAR NULL,
    site_geog GEOGRAPHY(POINT, 4326) NULL,
    constraint site_name_uniq unique(site_name)
);

CREATE TABLE IF NOT EXISTS unit (
    unit_id SERIAL PRIMARY KEY,
    site_name VARCHAR REFERENCES site(site_name),
    unit_name VARCHAR NOT NULL,
    unit_geog GEOGRAPHY(POLYGON, 4326) NULL,
    constraint unit_name_uniq unique (unit_name)
);

CREATE TABLE IF NOT EXISTS sample_location (
    location_id VARCHAR PRIMARY KEY,
    site_name VARCHAR REFERENCES site(site_name) ON DELETE RESTRICT ON UPDATE CASCADE,
    location_type VARCHAR NULL,
    location_geog GEOGRAPHY(POINT, 4326),
    UNIQUE(location_id, site_name)
);	

CREATE TABLE IF NOT EXISTS sample_parameters (
    param_cd CHAR(5) PRIMARY KEY,
    CONSTRAINT param_cd_check CHECK (param_cd SIMILAR TO '[[:digit:]]{5}'),
    group_name VARCHAR,
    description VARCHAR,
    epa_equivalence VARCHAR,
    statistical_basis VARCHAR,
    time_basis VARCHAR,
    weight_basis VARCHAR,
    particle_size_basis VARCHAR,
    sample_fraction VARCHAR,
    temperature_basis VARCHAR,
    casrn VARCHAR,
    srsname VARCHAR,
    parameter_unit VARCHAR
);

CREATE TABLE IF NOT EXISTS sample_results (
    sample_result_id SERIAL PRIMARY KEY,
    lab_id VARCHAR,
    site_name VARCHAR REFERENCES site(site_name),
    location_id VARCHAR NOT NULL REFERENCES sample_location(location_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    param_cd VARCHAR(5) NOT NULL REFERENCES sample_parameters(param_cd),
    sample_date DATE NOT NULL,
    media_matrix VARCHAR NULL,
    prep_method VARCHAR NULL,
    analysis_method VARCHAR NULL,
    analysis_flag CHAR(1),
    analysis_result REAL NULL,
    analysis_unit VARCHAR NOT NULL,
    detection_limit REAL,
    prac_quant_limit REAL,
    analysis_qualifier CHAR(1),
    disclaimer VARCHAR NULL,
    analysis_date DATE NULL,
    order_commment VARCHAR,
    analysis_comment VARCHAR,
    UNIQUE(lab_id, location_id, sample_date, param_cd, analysis_result)
);

\copy sample_parameters FROM 'param_codes.csv' WITH (FORMAT csv);

CREATE OR REPLACE FUNCTION check_units() 
  RETURNS trigger AS
$check_units$
DECLARE found_unit BIGINT;
DECLARE tmp_unit VARCHAR;
BEGIN
  SELECT COUNT(*) INTO found_unit FROM sample_parameters
    WHERE sample_parameters.param_cd = NEW.param_cd;
  IF found_unit > 0 THEN
    SELECT parameter_unit INTO tmp_unit FROM sample_parameters
      WHERE sample_parameters.param_cd = NEW.param_cd;	
          -- check that analysis_unit equals parameter_unit
	  IF NEW.analysis_unit != tmp_unit THEN
	    RAISE EXCEPTION 'Units not equal. Convert prior to inserting.';
	  END IF;
  END IF;
RETURN NEW;  
END;
$check_units$ 
LANGUAGE plpgsql;

CREATE TRIGGER check_insert_units
  BEFORE INSERT 
  ON sample_results
  FOR EACH ROW 
  EXECUTE PROCEDURE check_units();
