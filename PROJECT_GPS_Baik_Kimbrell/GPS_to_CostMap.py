import sys
import pandas as pd
import csv
import math
from PROJECT_GPS_Baik_Kimbrell import GPS_to_KML as gpskml

def main():
    file = sys.argv[1]
    df = gpskml.get_df(file)
    print(df)

main()
