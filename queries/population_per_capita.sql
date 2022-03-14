--
-- Identifying the per capita of each county from least to 
-- greatest with popualtion and number of post offices in 
-- each county. Ordered per capita from least to greatest.
--

CREATE VIEW population_per_capita AS

SELECT AVG(o.latitude), AVG(o.longitude), c.name AS county_name, CAST(COUNT(o.id) as real) / (CAST(c.population AS real) / 100000) AS per_capita,
		c.population, COUNT(o.id) AS num_of_offices   
FROM office AS o
    JOIN county AS c ON o.county_id = c.id
WHERE o.discontinued IS NULL
GROUP BY c.name, c.population;

ALTER VIEW population_per_capita OWNER TO postal;