from math import sin
from math import cos
from math import tan
from math import asin
from math import acos
from math import atan
from math import pi
from pprint import pprint
import pandas as pd
import numpy as np
import re
import math

#########################################################################################################################################################################
#### GENERAL HELPER FUNCTIONS ###########################################################################################################################################
#########################################################################################################################################################################
"""Calculates as-the-crow-flies distances between two locations."""
def calcDistance(lat1, long1, lat2, long2):
    if lat1 == lat2 and long1 == long2:
        return(0)
    try:
        dist_in_naut_miles = acos((sin(lat1 * pi / 180) * sin(lat2 * pi / 180) + cos(lat1 * pi / 180) * cos(
            lat2 * pi / 180) * cos(long2 * pi / 180 - long1 * pi / 180))) * 3443.8985
    except ValueError:
        print('ERROR CALCULATING DISTANCE: unit 1: ({}, {}), unit2: ({}, {})'.format(lat1, long1, lat2, long2))
        exit()
    dist = dist_in_naut_miles * 1.151
    return round(dist, 3)

"""Pulls the coordinates for each unit ID and stores them in a dictionary."""
def pullCoordinates(myfile):
    mydict = {}

    count = 0
    for line in open(myfile, "r"):
        if count == 0:
            count += 1
            continue
        mylist = line.split("\t")
        key = int(mylist[0])
        lat = mylist[31].strip()
        lon = mylist[32].strip()

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            continue

        mydict[key] = (lat, lon)
        count += 1

    return mydict

"""Converts a csv table into a dictionary of dictionaries."""
def convert_table_to_dict(filename):
    mydict = {}
    index_dict = {}
    line_count = 0
    for line in open(filename):
        if line_count == 0:
            headers = line.split(",")[1:]

            #making indices
            for num in range(len(headers)):
                index_dict[num] = int(headers[num])

            #make the empty dictionary
            for column in headers:
                mydict[int(column)] = {}
                for row in headers:
                    mydict[int(column)][int(row)] = None
            line_count +=1

        else:
            myline = line.split(",")

            for num in range(len(myline)):
                if num == 0:
                    continue
                else:
                    row_name = int(myline[0])
                    col_name = index_dict[num-1]
                    try:
                        value = float(myline[num])
                        mydict[row_name][col_name] = value
                        mydict[col_name][row_name] = value
                    except:
                        continue

    return mydict

"""Returns a dictionary where the key is a unit #, and corresponding value is a list of the 30 closest units to the unit in question."""
def find_closest_units():
    # key is business unit, values are (latitude, longitude) tuples
    coordinates = pullCoordinates()

    # key is business unit, values are lists of 30 closest restaurant to unit in question
    closest_units = {}
    goal = 50

    # loop through all business units to make list of closest units
    for unit1 in coordinates:
        lat1 = coordinates[unit1][0]
        long1 = coordinates[unit1][1]

        this_units_list = []

        for unit2 in coordinates:
            lat2 = coordinates[unit2][0]
            long2 = coordinates[unit2][1]

            # if comparing unit with itself, continue to next unit
            if unit1 == unit2:
                continue
            # calculate distance
            distance = calcDistance(lat1, long1, lat2, long2)

            # print (str(unit1) + " to " + str(unit2) + ": " + str(distance))

            if len(this_units_list) < goal:
                this_units_list.append((unit2, distance))
                this_units_list = sorted(this_units_list, key=lambda x: x[1])
            elif distance < this_units_list[-1][1]:
                this_units_list = this_units_list[:-1]  # removes furthest away unit to make room for this closer unit
                this_units_list.append((unit2, distance))  # appends closer unit to list
                this_units_list = sorted(this_units_list, key=lambda x: x[1])  # sorts list of units by distance

        closest_units[unit1] = [unit_tup[0] for unit_tup in this_units_list]

    return closest_units

"""Reads the input file and finds the distance/duration at indicated location."""
def read_matrix(loc1, loc2, input_file):
    loc2 = int(loc2)
    data = pd.read_csv(input_file, index_col=0, low_memory=False)
    return data[loc1][loc2]

"""Creates  a dictionary with keys for each district, and values are a list of units in that district"""
def Get_District_Dict():
    df2 = pd.read_csv('Data.csv', low_memory=False)

    District_Dict = {}

    # Create Dictionary Keys for every District pointing to a an empty list
    for index, row in df2.iterrows():
        District_Key = row['District Manager (Units)']
        District_Dict[District_Key] = []

    # Appends to the list the Business Unit ID's within that Division
    for index, row in df2.iterrows():
        # print(index,row)
        District_Key = row['District Manager (Units)']
        Business_Unit = row['Business Unit']
        District_Dict[District_Key].append(Business_Unit)

    # empty list - will be used to store calculated distances
    return District_Dict

"""Creates  a dictionary with keys for each division, and values are a list of units in that district"""
def Get_Division_Dict():
    df2 = pd.read_csv('Data.csv', low_memory=False)

    Division_Dict = {}

    # Create Dictionary Keys for every District pointing to a an empty list
    for index, row in df2.iterrows():
        Division_Key = row['Division Manager (Units)']
        Division_Dict[Division_Key] = []

    # Appends to the list the Business Unit ID's within that Division
    for index, row in df2.iterrows():
        # print(index,row)
        Division_Key = row['Division Manager (Units)']
        Business_Unit = row['Business Unit']
        Division_Dict[Division_Key].append(Business_Unit)

    # empty list - will be used to store calculated distances
    return Division_Dict

"""Creates  a dictionary with keys for each area, and values are a list of units in that district"""
def Get_Area_Dict():
    df2 = pd.read_csv('Data.csv', low_memory=False)

    Area_Dict = {}

    # Create Dictionary Keys for every District pointing to a an empty list
    for index, row in df2.iterrows():
        Area_Key = row['Area Manager (Units)']
        Area_Dict[Area_Key] = []

    # Appends to the list the Business Unit ID's within that Division
    for index, row in df2.iterrows():
        # print(index,row)
        Area_Key = row['Area Manager (Units)']
        Business_Unit = row['Business Unit']
        Area_Dict[Area_Key].append(Business_Unit)

    # empty list - will be used to store calculated distances
    return Area_Dict

"""Pulls data from a csv file and outputs it as a dictionary of dictionaries."""
def create_tuple_dict_districts_divisions(dist_file):
    tuple_dict = {}

    dict_of_dicts = convert_table_to_dict(dist_file)

    for row in dict_of_dicts:
        for col in dict_of_dicts[row]:
            distance = dict_of_dicts[row][col]
            if distance == None or row == col:
                continue
            else:
                small_unit = min(row, col)
                large_unit = max(row,col)
                my_tuple = (small_unit, large_unit)

            if my_tuple not in tuple_dict.keys():
                tuple_dict[my_tuple] = distance
    return tuple_dict
#########################################################################################################################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################




#########################################################################################################################################################################
#### BASELINE HELPER FUNCTIONS ##########################################################################################################################################
#########################################################################################################################################################################
"""Calculates district difficulty baseline."""
def District_Difficulty_Baseline():
    districts = Get_District_Dict()
    mydict = {}
    for district in districts:
        if len(districts[district]) == 0 or districts[district] == None:
            continue
        unit_list = districts[district]
        difficulty_list = []
        for unit in unit_list:
            if Get_Difficulty(unit) != None:
                difficulty_list.append(Get_Difficulty(unit))
        try:
            avg = round(sum(difficulty_list) / len(difficulty_list),2)
            stdv = round(np.std(difficulty_list),2)
            mydict[district] = avg
        except:
            mydict[district] = None
    return mydict

"""Calculates Division difficulty baseline."""
def Division_Difficulty_Baseline():
    divisions = Get_Division_Dict()
    mydict = {}
    for division in divisions:
        if len(divisions[division]) == 0 or divisions[division] == None:
            continue
        unit_list = divisions[division]
        difficulty_list = []
        for unit in unit_list:
            if Get_Difficulty(unit) != None:
                difficulty_list.append(Get_Difficulty(unit))
        try:
            avg = round(sum(difficulty_list) / len(difficulty_list),2)
            stdv = round(np.std(difficulty_list),2)
            mydict[division] = avg
        except:
            mydict[division] = None
    return mydict

"""Calculates Area Difficulty Baseline."""
def Area_Difficulty_Baseline():
        areas = Get_Area_Dict()
        mydict = {}
        for area in areas:
            if len(areas[area]) == 0 or areas[area] == None:
                continue
            unit_list = areas[area]
            difficulty_list = []
            for unit in unit_list:
                if Get_Difficulty(unit) != None:
                    difficulty_list.append(Get_Difficulty(unit))
            try:
                avg = round(sum(difficulty_list) / len(difficulty_list),2)
                stdv = round(np.std(difficulty_list),2)
                mydict[area] = avg
            except:
                mydict[area] = None
        return mydict
#########################################################################################################################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################




#########################################################################################################################################################################
#### MIDPOINT HELPER FUNCTIONS ##########################################################################################################################################
#########################################################################################################################################################################
"""
Finds midpoint of each district and returns a dictionary where the keys are the district names,
and values are the lat/long of the midpoint.
"""
def District_Midpoint(district_dict, myfile):
    #district_dict = Get_District_Dict()
    coordinates = pullCoordinates(myfile)
    latlong_dict = {}

    for key,value in district_dict.items():
        Division_Key = key
        if Division_Key in latlong_dict.keys():
            continue
        else:
            latlong_dict[Division_Key] = []
            for unit in value:
                latlong_dict[Division_Key].append(coordinates[unit])

    #STEP 1 Convert lat and long from degrees to radians
    radian_dict = {}
    for district,coords in latlong_dict.items():
        Division_Key = district
        if Division_Key in radian_dict.keys():
            continue
        else:
            lat_sum = 0
            long_sum = 0
            radian_dict[Division_Key] = []
            for latlong in coords:
                newlat = latlong[0]*pi/180
                newlong = latlong[1]*pi/180
                tup = (newlat,newlong)
                radian_dict[Division_Key].append(tup)

    #STEP 2 Convert lat/long to Cartesian coordinates
    Cart_dict = {}
    for district,coords in radian_dict.items():
        Division_Key = district
        if Division_Key in Cart_dict.keys():
            continue
        else:
            lat_sum = 0
            long_sum = 0
            Cart_dict[Division_Key] = []
            for latlong in coords:
                #latlong[0] is lat latlong[1] is long
                x = math.cos(latlong[0])*math.cos(latlong[1])
                y = math.cos(latlong[0])*math.sin(latlong[1])
                z = math.sin(latlong[0])
                tup = (x,y,z)
                Cart_dict[Division_Key].append(tup)

    #Step 3 Compute averages of x,y,z coordinates
    Weighted_Dict = {}
    for district,coords in Cart_dict.items():
        Division_Key = district
        if Division_Key in Weighted_Dict.keys():
            continue
        else:
            Weighted_Dict[Division_Key] = []
            x_sum = 0
            y_sum = 0
            z_sum = 0
            for xyz in coords:
                x_sum += xyz[0]
                y_sum += xyz[1]
                z_sum += xyz[2]
            tup = (x_sum/len(coords),y_sum/len(coords),z_sum/len(coords))
            Weighted_Dict[Division_Key].append(tup)

    #Step 4 Convert average x,y,z coordinates to latitude and longitude
    Averaged_Dict = {}
    for district,coords in Weighted_Dict.items():
        Division_Key = district
        if Division_Key in Averaged_Dict.keys():
            continue
        else:
            for xyz in coords:
                Averaged_Dict[Division_Key] = []
                lon = math.atan2(xyz[1],xyz[0])
                hyp = math.sqrt(xyz[0]*xyz[0]+xyz[1]*xyz[1])
                lat = math.atan2(xyz[2],hyp)
                #Convert Lat/lon to degrees
                lat = lat*180/pi
                lon = lon*180/pi
                tup = (lat,lon)
                Averaged_Dict[Division_Key].append(tup)
    return Averaged_Dict

"""
Finds midpoint of each division and returns a dictionary where the keys are the division names,
and values are the lat/long of the midpoint.
"""
def Division_Midpoint(division_dict, myfile):
    #division_dict = Get_Division_Dict()

    coordinates = pullCoordinates(myfile)

    latlong_dict = {}

    for key, value in division_dict.items():
        Division_Key = key
        if Division_Key in latlong_dict.keys():
            continue
        else:
            latlong_dict[Division_Key] = []
            for unit in value:
                latlong_dict[Division_Key].append(coordinates[unit])

    # STEP 1 Convert lat and long from degrees to radians
    radian_dict = {}
    for district, coords in latlong_dict.items():
        Division_Key = district
        if Division_Key in radian_dict.keys():
            continue
        else:
            lat_sum = 0
            long_sum = 0
            radian_dict[Division_Key] = []
            for latlong in coords:
                newlat = latlong[0] * pi / 180
                newlong = latlong[1] * pi / 180
                tup = (newlat, newlong)
                radian_dict[Division_Key].append(tup)

    # STEP 2 Convert lat/long to Cartesian coordinates
    Cart_dict = {}
    for district, coords in radian_dict.items():
        Division_Key = district
        if Division_Key in Cart_dict.keys():
            continue
        else:
            lat_sum = 0
            long_sum = 0
            Cart_dict[Division_Key] = []
            for latlong in coords:
                # latlong[0] is lat latlong[1] is long
                x = math.cos(latlong[0]) * math.cos(latlong[1])
                y = math.cos(latlong[0]) * math.sin(latlong[1])
                z = math.sin(latlong[0])
                tup = (x, y, z)
                Cart_dict[Division_Key].append(tup)

    # Step 3 Compute averages of x,y,z coordinates
    Weighted_Dict = {}
    for district, coords in Cart_dict.items():
        Division_Key = district
        if Division_Key in Weighted_Dict.keys():
            continue
        else:
            Weighted_Dict[Division_Key] = []
            x_sum = 0
            y_sum = 0
            z_sum = 0
            for xyz in coords:
                x_sum += xyz[0]
                y_sum += xyz[1]
                z_sum += xyz[2]
            tup = (x_sum / len(coords), y_sum / len(coords), z_sum / len(coords))
            Weighted_Dict[Division_Key].append(tup)

    # Step 4 Convert average x,y,z coordinates to latitude and longitude

    Averaged_Dict = {}
    for district, coords in Weighted_Dict.items():
        Division_Key = district
        if Division_Key in Averaged_Dict.keys():
            continue
        else:
            for xyz in coords:
                Averaged_Dict[Division_Key] = []
                lon = math.atan2(xyz[1], xyz[0])
                hyp = math.sqrt(xyz[0] * xyz[0] + xyz[1] * xyz[1])
                lat = math.atan2(xyz[2], hyp)
                # Convert Lat/lon to degrees
                lat = lat * 180 / pi
                lon = lon * 180 / pi
                tup = (lat, lon)
                Averaged_Dict[Division_Key].append(tup)
    return Averaged_Dict
#########################################################################################################################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################




#########################################################################################################################################################################
#### MODEL HELPER FUNCTIONS #############################################################################################################################################
#########################################################################################################################################################################
"""
Creates dictionaries where keys are tuples and values are the distances/durations
between the two units in question. Makes two dictionaries, one for distances, one for durations.
"""
def create_tuple_dict_units(dist_file, dur_file):
    tuple_dict_distances = {}
    tuple_dict_durations = {}

    dict_of_dicts_distances = convert_table_to_dict(dist_file)
    dict_of_dicts_durations = convert_table_to_dict(dur_file)

    for row in dict_of_dicts_distances:
        for col in dict_of_dicts_distances[row]:
            distance = dict_of_dicts_distances[row][col]
            #if distance == None:
            if distance == None or distance > 60.0:
                continue
            small_unit = min(row, col)
            large_unit = max(row, col)
            my_tuple = (small_unit, large_unit)

            if my_tuple not in tuple_dict_distances.keys():
                tuple_dict_distances[my_tuple] = dict_of_dicts_distances[row][col]
                tuple_dict_durations[my_tuple] = dict_of_dicts_durations[row][col]

    return (tuple_dict_distances, tuple_dict_durations)

"""
Formats the Gurobi solution into readable format.
Also makes an output file called district_assignments.csv.
"""
def format_district_solution(list_of_tups):
    district_count = 0

    district_assignments = {}
    for pair in list_of_tups:
        unit1 = pair[0]
        unit2 = pair[1]
        if unit1 in district_assignments.keys() and unit2 in district_assignments.keys():
            continue
        else:
            if unit1 in district_assignments.keys():
                district_assignments[unit2] = district_assignments[unit1]
            elif unit2 in district_assignments.keys():
                district_assignments[unit1] = district_assignments[unit2]
            else:
                district_assignments[unit1] = district_count
                district_assignments[unit2] = district_count
                district_count += 1

    output_dict = {}
    for district_num in range(district_count):
        key = district_num + 1000000
        output_dict[key] = []
        for unit in district_assignments:
            if district_assignments[unit] == district_num and unit > 1000000:
                output_dict[key].append(unit)

    f = open("district_assignments.csv", "w")
    for key in district_assignments.keys():
        #latitude = pullLatLong(key)[0]
        #longitude = pullLatLong(key)[1]
        mystring = "{}, {} \n".format(key,district_assignments[key] + 1000000)
        f.write(mystring)
    f.close()
    #return (district_assignments)
    return (output_dict)

"""Returns a list of all the units in given district."""
def pull_units_in_district(district_num):
    mydict = {}
    for line in open("district_assignments.csv", 'r'):
        line = line.split(',')
        unit = int(line[0].strip())
        district = int(line[1].strip())
        if district not in mydict.keys():
            mydict[district] = [unit]
        else:
            mydict[district].append(unit)
    return(mydict[district_num])

"""
Formats the Gurobi solution into readable format.
Also makes an output file called division_assignments.csv.
"""
def format_division_solution(list_of_tups):
    division_count = 2000000

    division_assignments = {}
    for pair in list_of_tups:
        district1 = pair[0]
        district2 = pair[1]
        if district1 in division_assignments.keys() and district2 in division_assignments.keys():
            continue
        else:
            if district1 in division_assignments.keys():
                division_assignments[district2] = division_assignments[district1]
            elif district2 in division_assignments.keys():
                division_assignments[district1] = division_assignments[district2]
            else:
                division_assignments[district1] = division_count
                division_assignments[district2] = division_count
                division_count += 1

    division_to_unit_dict = {}
    for district in division_assignments:
        units = pull_units_in_district(district)
        division = division_assignments[district]
        if division not in division_to_unit_dict.keys():
            division_to_unit_dict[division] = []
        for unit in units:
            division_to_unit_dict[division].append(unit)

    f = open("division_assignments.csv", "w")
    for division in division_to_unit_dict.keys():
        for unit in division_to_unit_dict[division]:
            #latitude = pullLatLong(key)[0]
            #longitude = pullLatLong(key)[1]
            mystring = "{}, {} \n".format(unit, division)
            f.write(mystring)
    f.close()

    return(division_to_unit_dict)

"""Returns a list of all the units in given division."""
def pull_units_in_division(division_num):
    mydict = {}
    for line in open("division_assignments.csv", 'r'):
        line = line.split(',')
        unit = int(line[0].strip())
        division = int(line[1].strip())
        if division not in mydict.keys():
            mydict[division] = [unit]
        else:
            mydict[division].append(unit)
    return(mydict[division_num])

"""
Formats the Gurobi solution into readable format.
Also makes an output file called area_assignments.csv.
"""
def format_area_solution(list_of_tups):
    area_count = 3000000

    area_assignments = {}
    for pair in list_of_tups:
        division1 = pair[0]
        division2 = pair[1]
        if division1 in area_assignments.keys() and division2 in area_assignments.keys():
            continue
        else:
            if division1 in area_assignments.keys():
                area_assignments[division2] = area_assignments[division1]
            elif division2 in area_assignments.keys():
                area_assignments[division1] = area_assignments[division2]
            else:
                area_assignments[division1] = area_count
                area_assignments[division2] = area_count
                area_count += 1

    area_to_unit_dict = {}
    for division in area_assignments:
        units = pull_units_in_division(division)
        area = area_assignments[division]
        if area not in area_to_unit_dict.keys():
            area_to_unit_dict[area] = []
        for unit in units:
            area_to_unit_dict[area].append(unit)

    f = open("area_assignments.csv", "w")
    for area in area_to_unit_dict.keys():
        for unit in area_to_unit_dict[area]:
            #latitude = pullLatLong(key)[0]
            #longitude = pullLatLong(key)[1]
            mystring = "{}, {} \n".format(unit, area)
            f.write(mystring)
    f.close()

    return(area_to_unit_dict)
#########################################################################################################################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################




#########################################################################################################################################################################
#### DIFFICULTY INDEX HELPER FUNCTIONS ##################################################################################################################################
#########################################################################################################################################################################
"""Creates a dictionary where the key is the unit number, and the value is it's difficulty value."""
def pullDifficultyDict(tsv_file):
    mydict = {}
    count = 0
    for line in open(tsv_file,"r"):
        if count == 0:
            count += 1
            continue
        else:
            count += 1
            mylist = line.split('\t')
            key = int(mylist[0])
            try:
                difficulty = float(mylist[46].strip())
            except:
                continue
            mydict[key] = difficulty
    return mydict

"""Reads difficulty index for a given unit and returns the difficulty as an int."""
def Get_Difficulty(unit):
    count = 0
    for line in open("Data.txt", "r"):
        if count == 0:
            count += 1
            continue
        mylist = line.split("\t")
        key = int(mylist[0])
        if key != unit:
            continue
        else:
            try:
                difficulty = float(mylist[46].strip())
            except:
                difficulty = None

            return difficulty
        count += 1

"""
Creates a dictionary where the keys are tuples of all combinations of units, and values are the sum of their difficulty.
No combinations of units that are greater than 60 miles apart are included.
"""
def create_difficulty_dict(tsv_file):
    distances = convert_table_to_dict("district_distances.csv")
    #pprint(distances)
    difficulties = pullDifficultyDict(tsv_file)
    combinations_dict = {}
    for unit1 in difficulties:
        for unit2 in difficulties:
            if unit1 == unit2 or distances[unit1][unit2] == None or distances[unit1][unit2] > 60:
            #if unit1 == unit2:
                continue
            else:
                my_tup = (unit1, unit2)
                combinations_dict[my_tup] = difficulties[unit1] + difficulties[unit2]
    return combinations_dict
#########################################################################################################################################################################
#########################################################################################################################################################################
#########################################################################################################################################################################
