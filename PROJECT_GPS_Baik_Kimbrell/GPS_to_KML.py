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

def emit_header():
    """
    initialize the kml file and emit header
    :return: initialized kml file handle
    """
    kml_file = open("GPS_to_KML_result.kml", "w")
    kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    kml_file.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    kml_file.write("\t<Document>\n")
    kml_file.write("\t\t<Style id=\"yellowPoly\"\n")
    kml_file.write("\t\t\t<LineStyle>\n")
    kml_file.write("\t\t\t\t<color>Af00ffff</color>\n")
    kml_file.write("\t\t\t\t<width>6</width>\n")
    kml_file.write("\t\t\t</LineStyle>\n")
    kml_file.write("\t\t\t<PolyStyle>\n")
    kml_file.write("\t\t\t\t<color>7f00ff00</color>\n")
    kml_file.write("\t\t\t</PolyStyle>\n")
    kml_file.write("\t\t</Style>\n")
    kml_file.write("\t\t<Placemark><styleUrl>#yellowPoly</styleUrl>\n")
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

def main():
    gps_df = pd.DataFrame(columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', ' Longitude', 'E/W of Longitude', 'Speed in knots', 'Track', 'Date', '...', '...', 'Checksum'])
    with open(sys.argv[1], 'rt') as readhandle:     # read in the GPS file
        reader = csv.reader(readhandle)
        for row in reader:
            if len(row) > 0 and row[0] == '$GPRMC':
                print(row, type(row))
                gps_df.loc[len(gps_df)] = row
    print(gps_df.head())
    print(gps_df.size)
    kml_handle = emit_header()
    emit_epilog(kml_handle)

main()