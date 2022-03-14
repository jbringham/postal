# STEPS TO CREATE DATABASE

1. Download the US Post Offices dataset from Harvard Dataverse from: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NUKCNA
    * make sure it is the Original Format ZIP file (464.9 MB)
2. Format all neccesary data into spreadsheets and save as csv file.
3. Run create.sql to create the tables for Postalrific database. 
4. Run copy.sql to copy the data from the spreadsheet csv file in order to import the data onto the server.
5. Run alter.sql to create PRIMARY and FOREIGN key constraints for the database after it has been imported on to the server. 
6. Run index.sql to create indexes for the columns that will be needed created. 
7. Run stats.sql to analyze the tables the and count the rows

```
psql < create.sql
./copy.sh
psql < alter.sql
psql < index.sql
psql < stats.sql
```