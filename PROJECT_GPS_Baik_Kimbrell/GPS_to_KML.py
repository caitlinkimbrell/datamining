"""
GPS_to_KML.py reads GPS file and converts to KML file that can be viewed on Google Maps.
"""
import sys
import pandas as pd

def preprocess(gps_data):
    print(gps_data.head(10))
    gps_data.drop([0,1,2,3])
    print(gps_data.head(10))

def eliminate_unnecessary_data(gps_data):
    filtered_data = gps_data[gps_data[0] != "$GPGSA" and gps_data[0] != "$GPVTG"]
    print(filtered_data.head(10))

def main():
    print(sys.argv[1])
    gps_df = pd.read_csv(sys.argv[1])    # read in the GPS file
    preprocess(gps_df)
    eliminate_unnecessary_data(gps_df)

main()