#!/bin/sh
#
# NOTE: \copy imports from a local file
#       COPY imports from another database


echo \copy office FROM csv
psql -c "\copy office FROM ../csv/va_offices.csv WITH CSV HEADER" postal

echo \copy county FROM csv
psql -c "\copy county FROM ../csv/county.csv WITH CSV HEADER" postal


