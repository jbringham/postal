--
-- Identifying the composite index for each 
-- county in relation to population and
-- per_capita (ordered from greatest to least).
-- Included number of offices per county and population.
--

CREATE VIEW compind_county AS
    
SELECT AVG(o.latitude), AVG(o.longitude), c.name AS county_name, COUNT(o.id) AS num_of_offices, c.population, 
    CAST(COUNT(o.id) as real) / (CAST(c.population AS real) / 100000) AS per_capita, c.compind AS comp_index
FROM office AS o
    JOIN county AS c ON o.county_id = c.id
WHERE o.discontinued IS NULL
GROUP BY c.id, c.name, c.population;

ALTER VIEW compind_county OWNER TO postal;