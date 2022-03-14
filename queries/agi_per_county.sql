--
-- Identifying the adjusted gross income
-- for each county in terms with population.
-- Ordered by population per county from least 
-- to greatest.
--

CREATE VIEW agi_per_county AS
    
SELECT AVG(o.latitude), AVG(o.longitude), c.name AS county, c.agi, c.population
FROM office AS o
    JOIN county AS c ON o.county_id = c.id
WHERE (c.agi / c.population) < 76456
GROUP BY c.name, c.agi, c.population;


ALTER VIEW agi_per_county OWNER TO postal;