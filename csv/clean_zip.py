"""
This script cleans up zipcodedata.csv by removing the zip codes
that are not in Virginia. It also aggregates the pacific islander
and native american counts with the "other" category.

Author: Jacob Bringham
Date:   10/5/2021
"""

import csv
import time

MIN_VA_ZIP = 20101
MAX_VA_ZIP = 24658

def main():
    with open("zipcodedata.csv") as fp:
        print("Reading in zipcodedata.csv...")
        reader = csv.reader(fp)
        data = list(reader)


        print("Removing zip codes not in VA...")
        oldRows = len(data)
        start = time.time()

        # Keep zip codes between 20101 and 24658
        # Add a new column containing just the zip code
        zipCol = data[0].index("NAME")
        data[0].append("zip")
        for row in data[2:]: # Skips first 2 rows
            spl = row[zipCol].split(" ")
            if len(spl) == 2 and spl[1].isdigit():
                zipcode = int(spl[1])
                row.append(str(zipcode))
                if zipcode < MIN_VA_ZIP or zipcode > MAX_VA_ZIP:
                    data.remove(row)
            else:
                print(row[zipCol])
                data.remove(row)
        elapsed = time.time() - start
        print(f"Took {elapsed : .2f} seconds")
        print(f"Removed {oldRows - len(data)} zip codes from zipcodedata.csv")
        print(f"{len(data)} zip codes remaining")

        headers = ["zip", "total", "total_error", \
                  "white_total", "white_error", \
                  "african_american_total", "african_american_error", \
                  "asian_total", "asian_error", \
                  "other_race_total", "other_race_error", \
                  "multiracial_total", "multiracial_error" \
                  ]

        transform = []
        for row in data[2:]:
            newRow = []
            newRow.append(row[-1]) # zip
            newRow.append(row[2])  # total
            newRow.append(row[3])  # total_error
            newRow.append(row[4])  # white_total
            newRow.append(row[5])  # white_error
            newRow.append(row[6])  # african_american_total
            newRow.append(row[7])  # african_american_error
            newRow.append(row[9]) # asian_total
            newRow.append(row[10]) # asian_error

            # other_race_total = islander + native american + other
            newRow.append(str( int(row[8]) + int(row[12]) + int(row[14]))) 

            # other_race_error 
            newRow.append(str( int(row[9]) + int(row[13]) + int(row[15]))) 

            # multiracial_total
            newRow.append(str( int(row[16]) + int(row[18]) + int(row[20]) ))

            # multiracial_total
            newRow.append(str( int(row[17]) + int(row[19]) + int(row[21]) ))

            transform.append(newRow)

        # Write out the transformed data as a csv
        with open("va_zipcodes.csv", "w") as out:
            csvwriter = csv.writer(out)
            csvwriter.writerow(headers)
            csvwriter.writerows(transform)
  
        print("Wrote out transformed data...")
        return 0
    return -1




if __name__ == "__main__":
    exit(main())

