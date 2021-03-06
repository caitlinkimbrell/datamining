"""
GPS_to_KML.py reads GPS file and converts to KML file that can be viewed on Google Maps.
"""
import sys
import pandas as pd
import csv
import math

def emit_header(filename):
    """
    initialize the kml file and emit header
    :return: initialized kml file handle
    """
    kml_file = open(filename, "w")
    kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    kml_file.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    kml_file.write("\t<Document>\n")
    kml_file.write("\t\t<Style id=\"cyanPoly\">\n")
    kml_file.write("\t\t\t<LineStyle>\n")
    kml_file.write("\t\t\t\t<color>ffffff00</color>\n")
    kml_file.write("\t\t\t\t<width>6</width>\n")
    kml_file.write("\t\t\t</LineStyle>\n")
    kml_file.write("\t\t\t<PolyStyle>\n")
    kml_file.write("\t\t\t\t<color>7ffff00</color>\n")
    kml_file.write("\t\t\t</PolyStyle>\n")
    kml_file.write("\t\t</Style>\n")
    kml_file.write("\t\t<Placemark><styleUrl>#cyanPoly</styleUrl>\n")
    kml_file.write("\t\t\t<LineString>\n")
    kml_file.write("\t\t\t\t<Description>Speed in MPH, not altitude.</Description>\n")
    kml_file.write("\t\t\t\t<extrude>1</extrude>\n")
    kml_file.write("\t\t\t\t<tesselate>1</tesselate>\n")
    kml_file.write("\t\t\t\t<altitudeMode>absolute</altitudeMode>\n")
    kml_file.write("\t\t\t\t<coordinates>\n")
    return kml_file

def emit_epilog(filehandle):
    filehandle.write("\t\t\t\t</coordinates>\n")
    filehandle.write("\t\t\t</LineString>\n")
    filehandle.write("\t\t</Placemark>\n")
    filehandle.write("\t</Document>\n")
    filehandle.write("</kml>\n")
    filehandle.close()

def emit_body(filehandle, gps_df):
    previous_coord = ""
    for index in range(gps_df.shape[0]):
        coordinate = ""
        if gps_df["E/W of Longitude"].iloc[index] == 'W':
            coordinate += "-"
        longitude = float(gps_df["Longitude"].iloc[index]) / 100
        degree = math.floor(longitude)
        frac_changes = (longitude - degree) * 100 / 60
        dg_frac = degree + frac_changes
        coordinate += str(dg_frac)
        coordinate += ","

        if gps_df["N/S of Longitude"].iloc[index] == 'S':
            coordinate += "-"
        latitude = float(gps_df["Latitude"].iloc[index]) / 100
        degree = math.floor(latitude)
        frac_changes = (latitude - degree) * 100 / 60
        dg_frac = degree + frac_changes
        coordinate += str(dg_frac)
        coordinate += ","

        speed = gps_df["Speed in knots"].iloc[index]
        coordinate += str(speed)

        # if it's duplicate/same record, no need to put it in
        if coordinate == previous_coord:
            continue
        filehandle.write("\t\t\t\t\t")
        filehandle.write(coordinate + "\n")
        previous_coord = coordinate
    return filehandle

def filter_df(df):
    new_df = pd.DataFrame(columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude', 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
    prev = None
    counter = 0
    for row in range(df.shape[0]):
        if prev is None:
            prev = df.iloc[row]
            new_df.loc[counter] = prev
            counter += 1
        else:
            curr = df.iloc[row]
            if curr["Latitude"] == prev["Latitude"] and curr["Longitude"] == prev["Longitude"] and curr["Speed in knots"] == prev["Speed in knots"]:
                continue
            else:
                prev = curr
                new_df.loc[counter] = prev
                counter += 1
    return new_df


def get_df(file):
    gps_df = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
    counter = 0     # counter for getting every n-th data
    skipping_n = 2
    with open(file, 'rt') as readhandle:  # read in the GPS file
        reader = csv.reader(readhandle)
        for row in reader:
            # only using GPRMC data
            if len(row) == gps_df.shape[1] and row[0] == '$GPRMC':
                if counter % skipping_n == 0:
                    gps_df.loc[len(gps_df)] = row
                counter += 1
    gps_df = filter_df(gps_df)
    return gps_df


def main():
    gps_df = get_df(sys.argv[1])
    kml_handle = emit_header(sys.argv[2])
    kml_handle = emit_body(kml_handle, gps_df)
    emit_epilog(kml_handle)

main()