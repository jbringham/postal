--
-- Identifying the per capita of each county from least to 
-- greatest with popualtion and number of post offices in 
-- each county. Ordered per capita from least to greatest.
--

CREATE VIEW offices_per_capita AS

SELECT c.name AS county_name, COUNT(o.id) AS num_of_offices, c.population, 
	CAST(COUNT(o.id) as real) / (CAST(c.population AS real) / 100000) AS per_capita, 
	CAST(c.white_population AS real) / c.population AS white_percent,
	CAST(c.african_american_population AS real) / c.population AS african_american_percent,
	CAST(c.asian_population AS real) / c.population AS asian_percent,
	CAST(c.other_population AS real) / c.population AS other_percent
FROM office AS o
	JOIN county AS c ON o.county_id = c.id
WHERE o.discontinued IS NULL
GROUP BY c.id;

ALTER VIEW offices_per_capita OWNER TO postal;