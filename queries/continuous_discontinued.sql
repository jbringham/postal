-- Identifying the first 500 post offices  
-- that are still continous and the ones that are 
-- discontined with duration in years. Included
-- with office name, county name, and ordered 
-- in descending order in terms of the year established.
--
CREATE VIEW continuous_discontinued AS
    
SELECT o.latitude AS lat, o.longitude AS long, o.name AS office_name, c.name AS county_name, COALESCE(o.Established, 0), COALESCE(o.Discontinued, 0), COALESCE(o.Duration, 0)
FROM office AS o
    JOIN county AS c ON o.county_id = c.id
WHERE o.latitude IS NOT NULL
	AND o.longitude IS NOT NULL
GROUP BY o.Discontinued, o.Established, c.name, c.population, o.name, o.Duration, o.latitude, o.longitude;

ALTER VIEW continuous_discontinued OWNER TO postal;