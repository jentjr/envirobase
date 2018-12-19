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
    site_id INT REFERENCES site(site_id),
    unit_name VARCHAR NOT NULL,
    unit_geog GEOGRAPHY(POLYGON, 4326) NULL,
    constraint unit_name_uniq unique (unit_name)
);

CREATE TABLE IF NOT EXISTS sample_location (
    location_id VARCHAR PRIMARY KEY,
    site_id INT REFERENCES site(site_id) ON DELETE CASCADE ON UPDATE CASCADE,
    location_type VARCHAR NULL,
    location_geog GEOGRAPHY(POINT, 4326),
    UNIQUE(location_id, site_id)
);	

CREATE TABLE IF NOT EXISTS sample_parameter (
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

CREATE TABLE IF NOT EXISTS medium_code (
    medium_cd VARCHAR(3) PRIMARY KEY,
    medium_name VARCHAR(64),
    medium_description VARCHAR,
    legacy_cd CHAR(1)
);

CREATE TABLE IF NOT EXISTS sample_result (
    id SERIAL PRIMARY KEY,
    site_id INT NOT NULL REFERENCES site(site_id),
    lab_id VARCHAR,
    location_id VARCHAR NOT NULL REFERENCES sample_location(location_id),
    param_cd VARCHAR(5) NOT NULL REFERENCES sample_parameter(param_cd),
    sample_date DATE NOT NULL,
    sample_time TIME NULL,
    medium_cd VARCHAR(3) REFERENCES medium_code(medium_cd),
    prep_method VARCHAR NULL,
    analysis_method VARCHAR NULL,
    analysis_flag CHAR(1) NULL,
    analysis_result REAL NULL,
    analysis_unit VARCHAR NOT NULL,
    detection_limit REAL NULL,
    reporting_limit REAL NULL,
    analysis_qualifier CHAR(1) NULL,
    disclaimer VARCHAR NULL,
    analysis_date TIMESTAMP NULL,
    order_comment VARCHAR NULL,
    analysis_comment VARCHAR NULL,
    UNIQUE(lab_id, location_id, sample_date, param_cd, analysis_result)
);

CREATE TABLE IF NOT EXISTS boring (
    boring_id INTEGER PRIMARY KEY,
    start_date DATE,
    end_date DATE
);

CREATE TABLE IF NOT EXISTS well (
    well_id VARCHAR NOT NULL REFERENCES sample_location(location_id),
    boring_id INTEGER REFERENCES boring(boring_id),
    install_date DATE,
    top_riser REAL,
    top_bent_seal REAL,
    top_gravel_pack REAL,
    top_screen REAL,
    bottom_screen REAL,
    bottom_well REAL,
    bottom_gravel_pack REAL,
    bottom_boring REAL,
    grout_seal_desc VARCHAR,
    bent_seal_desc VARCHAR,
    screen_type VARCHAR,
    gravel_pack_desc VARCHAR,
    riser_pipe_desc VARCHAR,
    spacer_depths VARCHAR,
    notes VARCHAR
);
 
-- load in the USGS parameter and medium codes
\copy sample_parameter FROM 'data/param_codes.csv' WITH (FORMAT csv);
\copy medium_code FROM 'data/medium_codes.csv' WITH (FORMAT csv); 
