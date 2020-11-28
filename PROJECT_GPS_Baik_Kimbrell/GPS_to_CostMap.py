import sys
import pandas as pd
import csv
import math
from PROJECT_GPS_Baik_Kimbrell import GPS_to_KML as gpskml

def costmap_header():
    """
    initialize the kml file and emit header
    :return: initialized kml file handle
    """
    kml_file = open("KML_MapFile.kml", "w")
    kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    kml_file.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    kml_file.write("\t<Placemark>\n")
    kml_file.write("\t\t<description>Red PIN for a STOP.</description>\n")
    kml_file.write("\t\t<Style id=\"normalPlacemark\">\n")
    kml_file.write("\t\t\t<IconStyle>\n")
    kml_file.write("\t\t\t\t<color>ff0000ff</color>\n")   # red
    kml_file.write("\t\t\t\t<Icon>\n")
    kml_file.write("\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n")
    kml_file.write("\t\t\t\t</Icon>\n")
    kml_file.write("\t\t\t</IconStyle>\n")
    kml_file.write("\t\t</Style>\n")
    kml_file.write("\t\t<Point>\n")
    kml_file.write("\t\t\t<coordinates>\n")
    return kml_file

def end_kml(filehandle):
    filehandle.write("</kml>")
    filehandle.close()

def end_placemark(filehandle):
    filehandle.write("\t\t\t</coordinates>\n")
    filehandle.write("\t\t</Point>\n")
    filehandle.write("\t</Placemark>\n")

def detect_stop(filehandle, gps_df):
    prev_gps = None
    curr_gps = None
    for index in range(gps_df):
        coordinate = ""
        curr_gps = gps_df.iloc[index]
        if prev_gps == None:
            prev_gps = curr_gps
        else:
            # if it's slowing down
            if prev_gps["Speed in knots"] > curr_gps["Speed in knots"]:
                if curr_gps["E/W of Longitude"] == 'W':
                    coordinate += "-"
                longitude = float(curr_gps["Longitude"]) / 100
                degree = math.floor(longitude)
                frac_changes = (longitude - degree) * 100 / 60
                dg_frac = degree + frac_changes
                coordinate += str(dg_frac)
                coordinate += ","

                if curr_gps["N/S of Longitude"] == 'S':
                    coordinate += "-"
                latitude = float(curr_gps["Latitude"]) / 100
                degree = math.floor(latitude)
                frac_changes = (latitude - degree) * 100 / 60
                dg_frac = degree + frac_changes
                coordinate += str(dg_frac)
                coordinate += ",0.0"

                filehandle.write("\t\t\t\t")
                filehandle.write(coordinate + "\n")
    end_placemark(filehandle)

def detect_left(filehandle, gps_df):
    filehandle.write("\t<Placemark>\n")
    filehandle.write("\t\t<description>Yellow PIN for a LEFT TURN.</description>\n")
    filehandle.write("\t\t<Style id=\"normalPlacemark\">\n")
    filehandle.write("\t\t\t<IconStyle>\n")
    filehandle.write("\t\t\t\t<color>ff00ffff</color>\n")   # yellow?
    filehandle.write("\t\t\t\t<Icon>\n")
    filehandle.write("\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n")
    filehandle.write("\t\t\t\t</Icon>\n")
    filehandle.write("\t\t\t</IconStyle>\n")
    filehandle.write("\t\t</Style>\n")
    filehandle.write("\t\t<Point>\n")
    filehandle.write("\t\t\t<coordinates>\n")
    prev_gps = None
    curr_gps = None
    for index in range(gps_df):
        coordinate = ""
        curr_gps = gps_df.iloc[index]
        if prev_gps == None:
            prev_gps = curr_gps
        else:
            # TODO if it's slowing down and the angle is
            if prev_gps["Speed in knots"] > curr_gps["Speed in knots"] and \
                prev_gps["Track"] > curr_gps["Track"]:
                if curr_gps["E/W of Longitude"] == 'W':
                    coordinate += "-"
                longitude = float(curr_gps["Longitude"]) / 100
                degree = math.floor(longitude)
                frac_changes = (longitude - degree) * 100 / 60
                dg_frac = degree + frac_changes
                coordinate += str(dg_frac)
                coordinate += ","

                if curr_gps["N/S of Longitude"] == 'S':
                    coordinate += "-"
                latitude = float(curr_gps["Latitude"]) / 100
                degree = math.floor(latitude)
                frac_changes = (latitude - degree) * 100 / 60
                dg_frac = degree + frac_changes
                coordinate += str(dg_frac)
                coordinate += ",0.0"

                filehandle.write("\t\t\t\t")
                filehandle.write(coordinate + "\n")
    end_placemark(filehandle)

def detect_right(filehandle, gps_df):
    filehandle.write("\t<Placemark>\n")
    filehandle.write("\t\t<description>Cyan PIN for a RIGHT TURN.</description>\n")
    filehandle.write("\t\t<Style id=\"normalPlacemark\">\n")
    filehandle.write("\t\t\t<IconStyle>\n")
    filehandle.write("\t\t\t\t<color>ff00ffff</color>\n")   # yellow?
    filehandle.write("\t\t\t\t<Icon>\n")
    filehandle.write("\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n")
    filehandle.write("\t\t\t\t</Icon>\n")
    filehandle.write("\t\t\t</IconStyle>\n")
    filehandle.write("\t\t</Style>\n")
    filehandle.write("\t\t<Point>\n")
    filehandle.write("\t\t\t<coordinates>\n")
    prev_gps = None
    curr_gps = None
    for index in range(gps_df):
        coordinate = ""
        curr_gps = gps_df.iloc[index]
        if prev_gps == None:
            prev_gps = curr_gps
        else:
            # TODO if it's slowing down and the angle is
            if prev_gps["Speed in knots"] > curr_gps["Speed in knots"] and \
                prev_gps["Track"] > curr_gps["Track"]:
                if curr_gps["E/W of Longitude"] == 'W':
                    coordinate += "-"
                longitude = float(curr_gps["Longitude"]) / 100
                degree = math.floor(longitude)
                frac_changes = (longitude - degree) * 100 / 60
                dg_frac = degree + frac_changes
                coordinate += str(dg_frac)
                coordinate += ","

                if curr_gps["N/S of Longitude"] == 'S':
                    coordinate += "-"
                latitude = float(curr_gps["Latitude"]) / 100
                degree = math.floor(latitude)
                frac_changes = (latitude - degree) * 100 / 60
                dg_frac = degree + frac_changes
                coordinate += str(dg_frac)
                coordinate += ",0.0"

                filehandle.write("\t\t\t\t")
                filehandle.write(coordinate + "\n")
    end_placemark(filehandle)

def main():
    file = sys.argv[1]
    df = gpskml.get_df(file)
    df = df.drop(columns=['...1', '...2'])      # drop unnecessary columns
    df = df.iloc[::5, :]        # get every 5 rows
    print(df)
    # kml_handle = costmap_header()
    # detect_stop(kml_handle, df)
    # detect_left(kml_handle, df)
    # detect_right(kml_handle, df)
    # end_kml(kml_handle)

main()
