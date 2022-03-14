DROP TABLE IF EXISTS office;

CREATE TABLE office (
    id integer NOT NULL,
    county_id integer NOT NULL,
    name text NOT NULL,
    altName text,
    origName text,
    state text NOT NULL,
    County1 text NOT NULL,
    County2 text,
    County3 text,
    OrigCounty text,
    Established integer,
    Discontinued integer,
    Continuous boolean NOT NULL,
    StampIndex text,
    GNIS_ID integer,
    Coordinates boolean NOT NULL,
    Duration integer,
    GNIS_Match boolean,
    GNIS_Name text,
    GNIS_County text,
    GNIS_State text,
    GNIS_FEATURE_ID integer,
    GNIS_Feature_Class text,
    GNIS_OrigName text,
    GNIS_OrigCounty text,
    GNIS_Latitude real,
    GNIS_Longitude real,
    GNIS_ELEV_IN_M integer,
    GNIS_Dist real,
    Latitude real,
    Longitude real   
    
);

--ALTER TABLE office OWNER TO absent;
ALTER TABLE office OWNER TO postal;

COMMENT ON TABLE office IS 'post offices in virginia';


DROP TABLE IF EXISTS county;

CREATE TABLE county (
    id integer NOT NULL,
    name text NOT NULL,
    property_Value real NOT NULL,
    agi real NOT NULL,
    retail_value real,
    compind real NOT NULL,
    population integer NOT NULL,
    white_population integer NOT NULL,
    african_american_population integer NOT NULL,
    asian_population integer NOT NULL,
    other_population integer NOT NULL,
    sq_mile real NOT NULL

);

-- CREATE FUNCTION counties_with_agi_lt(real)
-- RETURNS TABLE (
--                 lat double precision,
--                 long double precision,
--                 name text,
--                 agi real,
--                 population int
-- )
-- language plpgsql as $$
-- begin
--     RETURN query 
--         SELECT AVG(o.latitude), AVG(o.longitude), c.name AS county, c.agi, c.population
--         FROM office AS o
--             JOIN county AS c ON o.county_id = c.id
--         WHERE (c.agi / c.population) < $1
--         GROUP BY c.name, c.agi, c.population;
-- end;$$

-- CREATE FUNCTION counties_with_compind_lt(double precision)
-- RETURNS TABLE (
--                 lat double precision,
--                 long double precision,
--                 name text,
--                 compind real
-- )
-- language plpgsql as $$
-- begin
--     RETURN query 
--         SELECT AVG(o.latitude), AVG(o.longitude), c.name AS county_name, c.compind AS comp_index
--     FROM office AS o
--         JOIN county AS c ON o.county_id = c.id
--     WHERE o.discontinued IS NULL
--         AND c.compind < $1
--     GROUP BY c.id, c.name, c.population;
-- end;$$


-- CREATE FUNCTION counties_with_population_capita(double precision)
-- RETURNS TABLE (
--                 lat double precision,
--                 long double precision,
--                 name text,
--                 per_capita double precision
-- )
-- language plpgsql as $$
-- begin
--     RETURN query 
--         SELECT AVG(o.latitude), AVG(o.longitude), c.name AS county_name, CAST(COUNT(o.id) as real) / 
--                     (CAST(c.population AS real) / 100000) AS per_capita  
--             FROM office AS o
--                 JOIN county AS c ON o.county_id = c.id
--             WHERE o.discontinued IS NULL
--             GROUP BY c.name, c.population
--             HAVING CAST(COUNT(o.id) as real) / 
--                     (CAST(c.population AS real) / 100000) < $1;
-- end;$$

-- CREATE FUNCTION counties_with_established_offices(INT)
-- RETURNS TABLE (
--                 lat real,
--                 long real,
--                 name text,
--                 Established int
-- )
-- language plpgsql as $$
-- begin
--     RETURN query 
--         SELECT o.latitude AS lat, o.longitude AS long, c.name AS county_name, COALESCE(o.Established, 0) AS Established 
--             FROM office AS o
--                 JOIN county AS c ON o.county_id = c.id
--             WHERE o.latitude IS NOT NULL
--                 AND o.longitude IS NOT NULL
--             GROUP BY o.Discontinued, o.Established, c.name, c.population, o.name, o.Duration, o.latitude, o.longitude
--             HAVING COALESCE(o.Established, 0) < $1;
-- end;$$

-- CREATE FUNCTION counties_with_races_capita(real)
-- RETURNS TABLE (
--                 name text,
--                 num_of_offices int,
--                 population int,
--                 per_capita real,
--                 white_percent real,
--                 african_american_percent real,
--                 asian_percent real,
--                 other_percent real
-- )
-- language plpgsql as $$
-- begin
--     RETURN query 
--         SELECT c.name AS county_name, COUNT(o.id) AS num_of_offices, c.population, 
--             CAST(COUNT(o.id) as real) / (CAST(c.population AS real) / 100000) AS per_capita, 
--             CAST(c.white_population AS real) / c.population AS white_percent,
--             CAST(c.african_american_population AS real) / c.population AS african_american_percent,
--             CAST(c.asian_population AS real) / c.population AS asian_percent,
--             CAST(c.other_population AS real) / c.population AS other_percent
--         FROM office AS o
--             JOIN county AS c ON o.county_id = c.id
--         WHERE o.discontinued IS NULL
--             AND c.population < $1
--         GROUP BY c.id;
-- end;$$

--ALTER TABLE county OWNER TO absent;
ALTER TABLE county OWNER TO postal;

COMMENT ON TABLE county IS 'all counties in Virginia';



