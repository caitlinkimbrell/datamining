import sys
import pandas as pd
import csv
import math

right_turns_df = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
left_turns_df = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
stops_df = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
file_dfs = []

def costmap_header():
    """
    initialize the kml file and emit header
    :return: initialized kml file handle
    """
    kml_file = open("KML_MapFile.kml", "w")
    kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    kml_file.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    kml_file.write("\t<Document>\n")
    kml_file.write("\t\t<Placemark>\n")
    kml_file.write("\t\t\t<description>Red PIN for a STOP.</description>\n")
    kml_file.write("\t\t\t<Style id=\"normalPlacemark\">\n")
    kml_file.write("\t\t\t\t<IconStyle>\n")
    kml_file.write("\t\t\t\t\t<color>ff0000ff</color>\n")   # red
    kml_file.write("\t\t\t\t\t<Icon>\n")
    kml_file.write("\t\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n")
    kml_file.write("\t\t\t\t\t</Icon>\n")
    kml_file.write("\t\t\t\t</IconStyle>\n")
    kml_file.write("\t\t\t</Style>\n")
    kml_file.write("\t\t\t<Point>\n")
    kml_file.write("\t\t\t\t<coordinates>\n")
    return kml_file


def end_kml(filehandle):
    filehandle.write("\t</Document>\n")
    filehandle.write("</kml>")
    filehandle.close()


def end_placemark(filehandle):
    filehandle.write("\t\t\t\t</coordinates>\n")
    filehandle.write("\t\t\t</Point>\n")
    filehandle.write("\t\t</Placemark>\n")


def detect_stop(filehandle, gps_df):
    prev_gps = None
    curr_gps = None
    for index in range(gps_df.shape[0]):
        coordinate = ""
        curr_gps = gps_df.iloc[index]
        if prev_gps is None:
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
    filehandle.write("\t\t<Placemark>\n")
    filehandle.write("\t\t\t<description>Yellow PIN for a LEFT TURN.</description>\n")
    filehandle.write("\t\t\t<Style id=\"normalPlacemark\">\n")
    filehandle.write("\t\t\t\t<IconStyle>\n")
    filehandle.write("\t\t\t\t\t<color>ff00ffff</color>\n")   # yellow?
    filehandle.write("\t\t\t\t\t<Icon>\n")
    filehandle.write("\t\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n")
    filehandle.write("\t\t\t\t\t</Icon>\n")
    filehandle.write("\t\t\t\t</IconStyle>\n")
    filehandle.write("\t\t\t</Style>\n")
    filehandle.write("\t\t\t<Point>\n")
    filehandle.write("\t\t\t\t<coordinates>\n")
    prev_gps = None
    curr_gps = None
    for index in range(gps_df.shape[0]):
        coordinate = ""
        curr_gps = gps_df.iloc[index]
        if prev_gps is None:
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
    filehandle.write("\t\t<Placemark>\n")
    filehandle.write("\t\t\t<description>Cyan PIN for a RIGHT TURN.</description>\n")
    filehandle.write("\t\t\t<Style id=\"normalPlacemark\">\n")
    filehandle.write("\t\t\t\t<IconStyle>\n")
    filehandle.write("\t\t\t\t\t<color>ff00ffff</color>\n")   # yellow?
    filehandle.write("\t\t\t\t\t<Icon>\n")
    filehandle.write("\t\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n")
    filehandle.write("\t\t\t\t\t</Icon>\n")
    filehandle.write("\t\t\t\t</IconStyle>\n")
    filehandle.write("\t\t\t</Style>\n")
    filehandle.write("\t\t\t<Point>\n")
    filehandle.write("\t\t\t\t<coordinates>\n")
    prev_gps = None
    curr_gps = None
    for index in range(gps_df.shape[0]):
        coordinate = ""
        curr_gps = gps_df.iloc[index]
        if prev_gps is None:
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


def get_df(file):
    gps_df = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
    with open(file, 'rt') as readhandle:  # read in the GPS file
        reader = csv.reader(readhandle)
        for row in reader:
            # only using GPRMC data
            if len(row) == gps_df.shape[1] and row[0] == '$GPRMC':
                gps_df.loc[len(gps_df)] = row
    gps_df = filter_df(gps_df)
    return gps_df


def get_coordinate(curr_gps):
    coordinate = "\t\t\t\t"
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
    coordinate += "\n"
    return coordinate

def is_right_turn(prev_gps, curr_gps):
    flag = False
    if prev_gps["Speed in knots"] > curr_gps["Speed in knots"] and \
            prev_gps["Speed in knots"] >= 0.10:
        if float(prev_gps["Track"]) > float(curr_gps["Track"]) and \
                float(prev_gps["Track"]) - float(curr_gps["Track"]) - 180 >= 65 or \
                float(prev_gps["Track"]) - float(curr_gps["Track"]) - 180 < 100:
            # if the starting track angle is higher than the finishing angle and
            # the smaller difference between the two is greater than or equal to 65 or less than 100 degrees,
            # it is right turn
            flag = True
        elif float(prev_gps["Track"]) < float(curr_gps["Track"]) and \
                float(prev_gps["Track"]) - float(curr_gps["Track"]) <= -65 or \
                float(prev_gps["Track"]) - float(curr_gps["Track"]) > -100:
            # if the starting track angle is lower than the finishing angle and
            # the smaller difference between the two is greater than or equal to 65 or less than 100 degrees,
            # it is right turn
            flag = True
    return flag

def is_left_turn(prev_gps, curr_gps):
    flag = False
    if prev_gps["Speed in knots"] < curr_gps["Speed in knots"] and \
            prev_gps["Speed in knots"] >= 0.10:
        if float(prev_gps["Track"]) < float(curr_gps["Track"]) and \
                float(prev_gps["Track"]) - float(curr_gps["Track"]) + 180 <= -65 or \
                float(prev_gps["Track"]) - float(curr_gps["Track"]) + 180 > -100:
            # if the starting track angle is less than the finishing angle and
            # the smaller difference between the two is greater than or equal to 65 or less than 100 degrees,
            # it is left turn
            flag = True
        elif float(prev_gps["Track"]) > float(curr_gps["Track"]) and \
                float(prev_gps["Track"]) - float(curr_gps["Track"]) >= 65 or \
                float(prev_gps["Track"]) - float(curr_gps["Track"]) < 100:
            # if the starting track angle is lower than the finishing angle and
            # the smaller difference between the two is greater than or equal to 65 or less than 100 degrees,
            # it is right turn
            flag = True
    return flag

def is_stop(prev_gps, curr_gps):
    return float(curr_gps["Speed in knots"]) < 4.00


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
    df = df.drop(columns=['...1', '...2'])      # drop unnecessary columns
    df = df.iloc[::5, :]        # get every 5 rows
    return new_df


def main():
    # TODO takes in several GPS files and output one kml file with all the placemarks.
    for i in range(len(sys.argv)):
        if i == 0:
            continue
        file = sys.argv[i]
        df = filter_df(get_df(file))
        #print(df)
        file_dfs.append(df)
    for i in range(len(file_dfs)):
        df = file_dfs[i]
        prev = None
        for row in range(df.shape[0]):
            curr = df.iloc[row]
            if prev is None:
                prev = curr
                continue
            else:
                if is_left_turn(prev, curr):
                    global left_turns_df
                    left_turns_df = left_turns_df.append(curr)
                elif is_right_turn(prev, curr):
                    global right_turns_df
                    right_turns_df = right_turns_df.append(curr)
                elif is_stop(prev, curr):
                    global stops_df
                    stops_df = stops_df.append(curr)
    global left_turns_df
    left_turns_df = filter_df(left_turns_df)
    global right_turns_df
    right_turns_df = filter_df(right_turns_df)
    global stops_df
    stops_df = filter_df(stops_df)

    print(left_turns_df)
    print(right_turns_df)
    print(stops_df)

    kml_handle = costmap_header()
    detect_stop(kml_handle, df)
    detect_left(kml_handle, df)
    detect_right(kml_handle, df)
    end_kml(kml_handle)


main()
