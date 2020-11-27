"""
GPS_to_KML.py reads GPS file and converts to KML file that can be viewed on Google Maps.
"""
import sys
import pandas as pd
import csv

def preprocess(gps_data):
    print(gps_data.head(10))
    gps_data.drop([0,1,2,3])
    print(gps_data.head(10))

def eliminate_unnecessary_data(gps_data):
    filtered_data = gps_data[gps_data[0] != "$GPGSA" and gps_data[0] != "$GPVTG"]
    print(filtered_data.head(10))

def main():
    gps_df = pd.DataFrame(columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', ' Longitude', 'E/W of Longitude', 'Speed in knots', 'Track', 'Date', '...', '...', 'Checksum'])
    with open(sys.argv[1], 'rt') as readhandle:     # read in the GPS file
        reader = csv.reader(readhandle)
        for row in reader:
            if len(row) > 0 and row[0] == '$GPRMC':
                print(row, type(row))
                gps_df.loc[len(gps_df)] = row
    print(gps_df.head())
    # preprocess(gps_df)
    # eliminate_unnecessary_data(gps_df)

main()