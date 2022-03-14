"""
Author: Jacob Bringham
Version: 10/16/2021

Merges census.csv, incomedata.csv and size.csv to create county.csv

TODO: Add the distinction of city vs county as a column

Schema overview:
    ID   - Primary Key
    Name - Name of the county
    PropertyValue - Sum of all properties value within the county
    AGI - Adjust Gross Income of the county
    RetailValue - TODO
    CompIndex - TODO
    Population - Overall population of the county
    WhitePop - Number of white people in county
    AfricanAmericanPop - Number of African American People in county
    AsianPop - Number of Asian People in county
    OtherPop - Number of other races not mentioned in county
    
"""

import csv



def main():

    # Read in the size data
    size_data = {}
    with open("sizes.csv", encoding="windows-1252") as fp:
        reader = csv.reader(fp)
        data = list(reader)

        # First row does not contain data
        for row in data[1:]:
            # This file has some non unicode characters in it
            row[1] = row[1].replace("\xa0", " ")
            name = row[0].upper().strip()
            if not name.endswith("COUNTY"):
                name += " CITY"
            size_data[name] = float(row[1].split(" ")[0])


    # Read in the census data
    census_data = None
    with open("census.csv") as fp:
        reader = csv.reader(fp)
        census_data = list(reader)
        # First 4 rows do not contain data
        census_data = census_data[4:]

        # Delete 3 rows after title
        for row in census_data[:]:
            if row[0] == "":
                census_data.remove(row)

        # Delete columns that do not have a title
        for i, title in enumerate(census_data[0]):
            if title == "":
                for row in census_data:
                    del row[i]
       


    # Read in the income data
    income_data = None
    with open("incomedata.csv") as fp:
        reader = csv.reader(fp)
        income_data = list(reader)

        # Delete rows that aren't 2010-2012 (these looked the best)
        for row in income_data[:]:
            if row[0] != "2012-2014" and row[0] != "comp_year":
                income_data.remove(row)
        

    # Assert that both were read correctly
    if census_data == None or income_data == None:
        print("Failed to read census.csv or incomedata.csv")

    # Schema of new csv
    schema = ["id", "name", "property_value", "agi",  "retail_value", "comp_index", "population", 
    "white_population", "african_american_population", "asian_population", "other_population", "sq_mi"]
    
    county_data = []

    in_income_not_in_census = {}
    for income_entry in income_data[1:]:
        county_entry = [len(county_data)]
        
        # Lookup the county in census.csv
        found = False
        for census_entry in census_data[1:]:
            census_name = census_entry[1].upper().strip() #.replace(" COUNTY", "")
            income_name = income_entry[2].upper().strip() #.replace(" COUNTY", "")
            
            # Jurisdiction == div_name
            if income_name == census_name or income_name + " CITY" == census_name or income_name + " COUNTY" == census_name:
                if not census_name in size_data.keys():
                    print(f"{census_name} is not in the size data")
                county_entry.append(census_entry[1].title()) # Name = Jurisdiction (from census because it includes city/county)
                county_entry.append(income_entry[3].replace("$", "").replace(",", "")) # PropertyValue = property
                county_entry.append(income_entry[4].replace("$", "").replace(",", "")) # AGI_incl = agi_incl
                county_entry.append(income_entry[6].replace("$", "").replace(",", "")) # RetailValue = retail
                county_entry.append(income_entry[11].replace(",", "")) # comp_ind

                county_entry.append(census_entry[2].replace(",", "")) # Total Pop
                county_entry.append(census_entry[3].replace(",", "")) # White pop
                county_entry.append(census_entry[4].replace(",", "")) # African American Pop
                county_entry.append(census_entry[5].replace(",", "")) # Asian Pop
                county_entry.append(str(int(census_entry[6].replace(",", "")) \
                                     + int(census_entry[7].replace(",", "")))) # Other pop
                county_entry.append(size_data[census_name]) # square mileage
                county_data.append(county_entry)
                found = True
                break
        
        if not found:
            in_income_not_in_census[income_entry[2]] = True
    
    print("Entries in incomedata.csv that are not in census.csv and are therefore dropped")
    for key in in_income_not_in_census.keys():
        print(f"    '{key}'")


    with open("county.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(schema)
        writer.writerows(county_data)




if __name__ == "__main__":
    exit(main())
