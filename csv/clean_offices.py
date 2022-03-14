"""
This script cleans up offices.csv by performing the following:

    1. Removing the post offices that aren't in virginia.
    2. Remove the AltName OrigName columns
    3. Remove the County2, County3, OrigCounty columns
    4. Remove the StampIndex column
    5. Remove the GNIS Columns

Author: Jacob Bringham
Version: 10/5/2021
"""

import csv
import time


def main():
    
    with open("offices.csv") as fp:
        print("Reading in offices.csv...")
        reader = csv.reader(fp)
        data = list(reader)
        
        total_offices = len(data)

        # Filter out post offices not in VA
        stateCol = data[0].index("State")

        print("Removing post offices that are not in VA...")
        start = time.time()

        for row in data[1:]:
            if row[stateCol] != "VA":
                data.remove(row)

        elapsed = time.time() - start
        print(f"Took {elapsed : 2f} seconds")
        print(f"Removed {total_offices - len(data)} offices from offices.csv")
        print(f"{len(data)} offices remaining")

        print("Fixing known typos...")
        # Fix known typos in county names
        typos = {}
        typos["KING AND QUEENEN"] = "KING AND QUEEN"
        typos["NORTHUMBERLANDND"] = "NORTHUMBERLAND"
        typos["CULPEPPER"] = "CULPEPER"
        typos["CULPERER?"] = "CULPEPER"
        typos["PRINCESS ANNEE"] = "PRINCESS ANNE"
        typos["NULL"] = ""
        for row in data[1:]:
            office_county_name = row[4]
            if office_county_name in typos:
                row[4] = typos[office_county_name]


        # Remove bad counties
        print("Removing counties that no longer have income data...")
        bad_counties = {}
        bad_counties["MONONGALIA?"] = True
        bad_counties[""] = True
        bad_counties[" "] = True
        bad_counties["?"] = True
        bad_counties["WOOD?"] = True
        bad_counties["LEWIS?"] = True
        bad_counties["WOODFORD"] = True
        bad_counties["WARWICK"] = True
        bad_counties["PRINCESS ANNE"] = True
        bad_counties["PRINCESS ANNEE"] = True
        bad_counties["UNKNOWN"] = True
        for row in data[1:]:
            office_county_name = row[4]
            if office_county_name in bad_counties:
                data.remove(row)

        
        # Add office ID's to each row
        data[0].insert(0, "id")
        for i, row in enumerate(data[1:]):
            row.insert(0, i)
            
        # Create a hashmap of county name -> database entry
        print("Creating hashmap of county names to county entries...")
        counties = {}
        with open("county.csv") as county_fp:
            csvreader = csv.reader(county_fp)
            county_data = list(csvreader)
            for row in county_data:
                name = row[1].upper()
                counties[name] = row 

        print("Performing a county lookup for each post office in VA")
        data[0].insert(1, "county_id")
        missing_counties = {}
        print()
        print(f"{data[0]}")
        print()
        for i, row in enumerate(data[1:]):
            office_county = row[5]
            gnis_orig_county = row[data[0].index("GNIS.OrigCounty") - 1]

            # Check for GNIS.OrigCounty to see if it's a city
            name = ""
            if gnis_orig_county != "":
                if gnis_orig_county.upper().find("(CITY)") != -1: 
                    # If it contains city, fix it
                    name = gnis_orig_county.upper().replace("(CITY)", "CITY")
                else:
                    name = office_county.upper() + " COUNTY"
            else:
                name = office_county.upper() + " COUNTY"

            cityname = office_county.upper() + " CITY"
            if name in counties:
                row.insert(1, counties[name][0])
            elif cityname in counties:
                row.insert(1, counties[cityname][0])
            else:
                missing_counties[name] = True
                missing_counties[cityname] = True
                row.insert(1, "NULL")

        print("Couldn't find these counties in county.csv:")
        for key in missing_counties.keys():
            print(f"    '{key}'")
            




        # Write out data as a csv file
        print("Writing out va_offices.csv")
        with open("va_offices.csv", "w") as out:
            csvwriter = csv.writer(out) 
            csvwriter.writerows(data)

        return 0
    return -1


if __name__ == "__main__":
    exit(main())
