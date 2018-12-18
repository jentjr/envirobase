-- Create trigger to make sure the inserted sample results unit matches
-- the USGS parameter code unit. This is a quick check instead of 
-- trying to do unit conversions.
CREATE OR REPLACE FUNCTION check_unit() 
  RETURNS trigger AS
$check_unit$
DECLARE found_unit BIGINT;
DECLARE tmp_unit VARCHAR;
BEGIN
  SELECT COUNT(*) INTO found_unit FROM sample_parameter
    WHERE sample_parameter.param_cd = NEW.param_cd;
  IF found_unit > 0 THEN
    SELECT parameter_unit INTO tmp_unit FROM sample_parameter
      WHERE sample_parameter.param_cd = NEW.param_cd;	
          -- check that analysis_unit equals parameter_unit
	  IF NEW.analysis_unit != tmp_unit THEN
	    RAISE EXCEPTION 'Units not equal. Convert prior to inserting.';
	  END IF;
  END IF;
RETURN NEW;  
END;
$check_unit$ 
LANGUAGE plpgsql;

CREATE TRIGGER check_insert_unit
  BEFORE INSERT 
  ON sample_result
  FOR EACH ROW 
  EXECUTE PROCEDURE check_unit();