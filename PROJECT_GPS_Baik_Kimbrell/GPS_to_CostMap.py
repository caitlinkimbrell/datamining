import sys
import pandas as pd
import csv
import math


# contians all gps points that are right turns
right_turns_df = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
# contains all gps points that are left turns
left_turns_df = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
# contains all gps points that are stops
stops_df = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
# contains all gps points
master_dfs = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
# color mapping to placemark type
color_dict = {"stop" : "ff00ffff", "right turn" : "00ffffff", "left turn" : "ffff00ff" }
# small delta for filtering duplicates
delta_small = .002
# big delta for filtering duplicates
delta_big = .1


# writes out the header of the kml file
def costmap_header(filename):
    """
    initialize the kml file and emit header
    :return: initialized kml file handle
    """
    kml_file = open(filename, "w")
    kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    kml_file.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    kml_file.write("\t<Document>\n")
    return kml_file


# writes out the ending of the kml file
def end_kml(filehandle):
    filehandle.write("\t</Document>\n")
    filehandle.write("</kml>")
    filehandle.close()


# gets the data frame from the given file
def get_df(file):
    gps_df = pd.DataFrame(
        columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude',
                 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
    counter = 0     # counter for getting every n-th data
    skipping_n = 5
    with open(file, 'rt') as readhandle:  # read in the GPS file
        reader = csv.reader(readhandle)
        for row in reader:
            # only using GPRMC data
            if len(row) == gps_df.shape[1] and row[0] == '$GPRMC':
                if counter % skipping_n == 0:
                    gps_df.loc[len(gps_df)] = row
                counter += 1
    return gps_df


# writes a place mark in KML to the given file handle, plac emark is off the given gps point
def write_placemark(filehandle, curr_gps, type):
    filehandle.write("\t\t<Placemark>\n")
    filehandle.write("\t\t\t<description>"+type+"</description>\n")
    filehandle.write("\t\t\t<Style id=\""+type+"\">\n")
    filehandle.write("\t\t\t\t<IconStyle>\n")
    filehandle.write("\t\t\t\t\t<color>"+color_dict.get(type)+"</color>\n")  # yellow?
    filehandle.write("\t\t\t\t\t<Icon>\n")
    filehandle.write("\t\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n")
    filehandle.write("\t\t\t\t\t</Icon>\n")
    filehandle.write("\t\t\t\t</IconStyle>\n")
    filehandle.write("\t\t\t</Style>\n")
    filehandle.write("\t\t\t<Point>\n")
    filehandle.write("\t\t\t\t<coordinates>\n")
    filehandle.write(get_coordinate(curr_gps))
    filehandle.write("\t\t\t\t</coordinates>\n")
    filehandle.write("\t\t\t</Point>\n")
    filehandle.write("\t\t</Placemark>\n")


# returns the coordinate string og the given gps point
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

# determines if the curr_gps is a right turn or not
def is_right_turn(prev_gps, curr_gps):
    flag = False
    if float(curr_gps["Speed in knots"]) <= 13:
        # going less than 15 mph
        if float(prev_gps["Track"]) > float(curr_gps["Track"]):
            if 360 - float(prev_gps["Track"]) - float(curr_gps["Track"]) >= 80 or \
                360 - float(prev_gps["Track"]) - float(curr_gps["Track"]) < 100:
                # if the starting track angle is higher than the finishing angle and
                # the smaller difference between the two is greater than or equal to 80 or less than 100 degrees,
                # it is right turn
                flag = True
        elif float(prev_gps["Track"]) < float(curr_gps["Track"]):
            if float(curr_gps["Track"]) - float(prev_gps["Track"]) >= 80 or \
                float(curr_gps["Track"]) - float(prev_gps["Track"]) < 100:
                # if the starting track angle is lower than the finishing angle for cases passing North
                # the smaller difference between the two is greater than or equal to 80 or less than 100 degrees,
                # it is right turn
                flag = True
    return flag


# determines if the curr_gps is  aleft turn or not
def is_left_turn(prev_gps, curr_gps):
    flag = False
    if float(curr_gps["Speed in knots"]) <= 17:
        # going less than 20 mph
        if float(prev_gps["Track"]) < float(curr_gps["Track"]):
            if 360 - float(curr_gps["Track"]) - float(prev_gps["Track"]) + 180 >= 80 or \
                360 - float(curr_gps["Track"]) - float(prev_gps["Track"]) + 180 < 100:
                # if the starting track angle is less than the finishing angle and
                # the smaller difference between the two is greater than or equal to 80 or less than 100 degrees,
                # it is left turn
                flag = True
        elif float(prev_gps["Track"]) > float(curr_gps["Track"]):
            if float(prev_gps["Track"]) - float(curr_gps["Track"]) >= 80 or \
                float(prev_gps["Track"]) - float(curr_gps["Track"]) < 100:
                # if the starting track angle is bigger than the finishing angle for cases passing North
                # the smaller difference between the two is greater than or equal to 80 or less than 100 degrees,
                # it is left turn
                flag = True
    return flag


# returns whether the curr_gps is a stop or not
def is_stop(prev_gps, curr_gps):
    # if its slower than 4 knots it is a stop
    return float(curr_gps["Speed in knots"]) < 4.00


# determines if two gps poitns are the same within a given delta
def is_same(prev, curr, delta):
    if float(prev["Latitude"]) - delta <= float(curr["Latitude"]) <= float(prev["Latitude"]) + delta:
        if float(prev["Longitude"]) - delta <= float(curr["Longitude"]) <= float(prev["Longitude"]) + delta:
            return True
    return False


# filters the given data frame using the delta to determine duplicates
def filter_df(df, delta):
    new_df = pd.DataFrame(columns=['Type', 'UTC', 'Status', 'Latitude', 'N/S of Longitude', 'Longitude', 'E/W of Longitude', 'Speed in knots', 'Track', 'Date', '...1', '...2', 'Checksum'])
    prev = None
    for row in range(df.shape[0]):
        if prev is None:
            prev = df.iloc[row]
            new_df = new_df.append(prev)
        else:
            curr = df.iloc[row]
            if is_same(prev, curr, delta):
                continue
            else:
                prev = curr
                new_df = new_df.append(prev)
    df = df.drop(columns=['...1', '...2'])      # drop unnecessary columns
    #df = df.iloc[::5, :]        # get every 5 rows
    return new_df


def main():
    # takes in seceral gps files and appends to master dataframe, last file name is the name of file to write to
    for i in range(len(sys.argv) - 1):
        if i == 0:
            continue
        file = sys.argv[i]
        df = get_df(file)
        global master_dfs
        master_dfs = master_dfs.append(df)
    prev = None
    print(master_dfs[["Longitude", "Latitude", "Speed in knots"]])
    # filter close duplicates
    master_dfs = filter_df(master_dfs, delta_small)
    print(master_dfs[["Longitude", "Latitude", "Speed in knots"]])
    # go through master dfs and split gps points into right turn, left turn, or stop
    for row in range(master_dfs.shape[0]):
        curr = master_dfs.iloc[row]
        if prev is None:
            prev = curr
            if is_stop(prev, curr):
                global stops_df
                stops_df = stops_df.append(curr)
            continue
        else:
            if is_left_turn(prev, curr):
                global left_turns_df
                left_turns_df = left_turns_df.append(curr)
            elif is_right_turn(prev, curr):
                global right_turns_df
                right_turns_df = right_turns_df.append(curr)
            elif is_stop(prev, curr):
                stops_df = stops_df.append(curr)
        prev = curr
    # filter three new dfs using the big interval
    left_turns_df = filter_df(left_turns_df, delta_big)
    right_turns_df = filter_df(right_turns_df, delta_big)
    stops_df = filter_df(stops_df, delta_big)

    print("lefts: " + str(len(left_turns_df.index)))
    print("rights: " + str(len(right_turns_df.index)))
    print("stops: " + str(len(stops_df.index)))
    # write the kml
    kml_handle = costmap_header(sys.argv[len(sys.argv) - 1])
    for points in range(len(stops_df)):
        write_placemark(kml_handle, stops_df.iloc[points], "stop")
    for points in range(len(right_turns_df)):
        write_placemark(kml_handle, right_turns_df.iloc[points], "right turn")
    for points in range(len(left_turns_df)):
        write_placemark(kml_handle, left_turns_df.iloc[points], "left turn")
    end_kml(kml_handle)


main()
