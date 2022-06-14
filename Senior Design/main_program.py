from helper_functions import *
from pprint import pprint
import csv
from model_district import *
from model_division import *
from model_area import *
#from model_difficulty import *


#### Test case library ############################################################
colorado_9 = [2501072,2500606,2501566,2501107,2501516,2501598,2501708,2500183,2501523]
colorado_10 = [2500521,2501072,2500606,2501566,2501107,2501516,2501598,2501708,2500183,2501523]
jacksonville_24 = [1250054,1250071,1250323,1250477,1250536,1250590,1250734,1251050,1251289,1251341,1251518,1251925,1251962,1252006,1252044,1252063,1252083,1252104,1252133,1252150,1252256,1252301,1252333,1252366]
houston_26 = [1010236,1010244,1010896,1010920,1010956,1010976,1010999,1011207,1011260,1011437,1011460,1011513,1011545,1011572,1011589,1011687,1012002,1012042,1012076,1012109,1012179,1012197,1012260,1012298,1012342,1012369]
pensacola_27 = [1011385,1010377,1011541,1011361,1011845,1011272,1011471,1011629,1011073,1011046,1010393,1011698,1012382,1011602,1011590,1012003,1010147,1010586,1011921,1010252,1010091,1011424,1010860,1012368,1011262,1011792,1010158]
east_n_carolina_32 = [1010024,1010359,1010360,1010711,1010736,1010871,1010934,1011021,1011112,1011153,1011307,1011433,1011456,1011536,1011549,1011624,1011639,1011651,1011665,1011774,1011810,1011955,1011957,1011974,1011976,1012031,1012085,1012118,1012184,1012263,1012286,1012354]
mississippi_50 = [1010124,1010672,1010832,1010891,1010927,1010969,1010983,1011176,1011355,1011377,1011396,1011459,1011506,1011517,1011573,1011647,1011668,1011748,1011802,1011807,1011822,1011827,1011847,1011864,1011874,1011880,1011910,1011928,1012004,1012045,1012123,1012139,1012170,1260235,1260478,1260665,1260682,1260759,1261140,1261328,1261888,1261927,1261952,1261960,1261965,1261980,1262089,1262136,1262228,1262268]
dallas_54 = [1010467,1011085,1011579,1010151,1011585,1012328,1011448,1011492,1012273,1011723,1011108,1010358,1011130,1011637,1011422,1011251,1011421,1011634,1011735,1010306,1012362,1010211,1011682,1010169,1011339,1010213,1010372,1010224,1012178,1012144,1010593,1010961,1010231,1010192,1010815,1010385,1012229,1011861,1012241,1012208,1010327,1011383,1011186,1012194,1012246,1010206,1011217,1010836,1011628,1011044,1010975,1011025,1011653,1011191]
south_florida_81 = [1250043,1250096,1250173,1250195,1250258,1250318,1250355,1250363,1250374,1250405,1250414,1250435,1250443,1250475,1250504,1250509,1250522,1250565,1250566,1250567,1250591,1250607,1250617,1250618,1250634,1250635,1250650,1250699,1250793,1250806,1250831,1250870,1250901,1250929,1250978,1251098,1251124,1251228,1251243,1251252,1251266,1251280,1251290,1251310,1251321,1251391,1251464,1251620,1251627,1251945,1251982,1252014,1252032,1252053,1252058,1252059,1252115,1252132,1252158,1252159,1252174,1252177,1252191,1252192,1252199,1252216,1252226,1252242,1252261,1252275,1252294,1252312,1252321,1252329,1252344,1252350,1252351,1252352,1252364,1252371,1252383]
atlanta_279 = [1010007,1010022,1010025,1010029,1010034,1010041,1010046,1010074,1010082,1010100,1010105,1010154,1010177,1010207,1010254,1010284,1010286,1010295,1010298,1010313,1010325,1010362,1010412,1010415,1010421,1010424,1010425,1010479,1010489,1010494,1010549,1010550,1010553,1010562,1010571,1010574,1010577,1010580,1010595,1010614,1010622,1010625,1010630,1010640,1010655,1010663,1010670,1010684,1010686,1010690,1010694,1010700,1010722,1010730,1010762,1010773,1010777,1010778,1010786,1010791,1010795,1010799,1010807,1010827,1010841,1010845,1010853,1010854,1010857,1010862,1010874,1010877,1010888,1010898,1010899,1010900,1010915,1010917,1010922,1010923,1010924,1010958,1010960,1010974,1010981,1010984,1010993,1010997,1011000,1011007,1011015,1011017,1011038,1011042,1011054,1011057,1011058,1011064,1011071,1011074,1011077,1011091,1011100,1011106,1011109,1011110,1011114,1011125,1011131,1011132,1011134,1011146,1011147,1011149,1011150,1011156,1011172,1011177,1011189,1011194,1011196,1011200,1011212,1011215,1011219,1011235,1011253,1011269,1011271,1011296,1011299,1011300,1011309,1011311,1011337,1011343,1011344,1011348,1011352,1011366,1011392,1011400,1011402,1011413,1011455,1011466,1011473,1011478,1011485,1011487,1011496,1011500,1011507,1011508,1011514,1011548,1011554,1011563,1011567,1011570,1011583,1011587,1011600,1011605,1011612,1011616,1011622,1011631,1011640,1011641,1011643,1011652,1011659,1011662,1011670,1011671,1011672,1011674,1011684,1011690,1011694,1011696,1011700,1011704,1011717,1011718,1011721,1011722,1011726,1011729,1011731,1011740,1011750,1011751,1011755,1011762,1011764,1011766,1011769,1011772,1011776,1011781,1011784,1011786,1011789,1011799,1011800,1011801,1011832,1011835,1011846,1011848,1011849,1011853,1011865,1011883,1011885,1011886,1011890,1011893,1011898,1011900,1011905,1011915,1011916,1011932,1011936,1011941,1011943,1011966,1011968,1011995,1011996,1011998,1012000,1012030,1012046,1012050,1012070,1012074,1012096,1012100,1012110,1012111,1012126,1012135,1012145,1012146,1012156,1012160,1012161,1012166,1012167,1012168,1012175,1012182,1012185,1012200,1012202,1012209,1012212,1012224,1012234,1012252,1012253,1012272,1012277,1012300,1012302,1012308,1012315,1012319,1012330,1012346,1012373,1012378,1012379,1012381,1012384]


###############################################################################################
###############################################################################################
#### Use these bools/constants to turn on/off cerain models ###################################
test_units = colorado_9                                                ###############
                                                                                ###############
run_district = True                                                             ###############
run_division = False                                                             ###############
run_area = False                                                                 ###############
                                                                                ###############
minimize = "distance" #"duration"                                               ###############
                                                                                ###############
use_difficulty_constraints = False                                              ###############
difficulty_bound = 0.9                                                          ###############
difficulty_type = 0 #0 if Operating DI, 1 if Crime DI                           ###############
###############################################################################################
###############################################################################################
###############################################################################################


##### GUI Inputs ###############################################################################


##### Baselines ################################################################################


##### Pull Google Data to Retrieve Distances/Durations #########################################


##### Clustering Algorithm? ####################################################################


##### Run Optimization Model ###################################################################
def optimize():
    if run_district:
        print("############################################# Running District Model #############################################")
        run_district_model(test_units, minimize, use_difficulty_constraints, difficulty_bound, difficulty_type)


def output():
##### Create Tableau Output ####################################################################
    print("\n\n############################################# Creating Tableau Output #############################################")
    my_dict = {}
    #Make dict of dicts
    for unit in test_units:
        my_dict[unit] = {"latitude": None,
        "longitude": None,
        "district": None,
        "division": None,
        "area": None}

    #Write district assignments
    if run_district:
        for line in open("district_assignments.csv", "r"):
            line = line.split(',')
            unit = int(line[0].strip())
            district = int(line[1].strip())
            my_dict[unit]['district'] = district

    #Write division assignments
    if run_division:
        for line in open("division_assignments.csv", "r"):
            line = line.split(',')
            unit = int(line[0].strip())
            division = int(line[1].strip())
            my_dict[unit]['division'] = division

    #Wriite area assignments
    if run_area:
        for line in open("area_assignments.csv", "r"):
            line = line.split(',')
            unit = int(line[0].strip())
            area = int(line[1].strip())
            my_dict[unit]['area'] = area

    #Write latitude and longitude
    count = 0
    for line in open("Data.txt", "r"):
        if count == 0:
            count += 1
            continue
        else:
            mylist = line.split("\t")
            unit = int(mylist[0])
            if unit not in test_units:
                continue
            else:
                lat = mylist[31].strip()
                lon = mylist[32].strip()

                try:
                    lat = float(lat)
                    lon = float(lon)
                except ValueError:
                    lat = None
                    lon = None

                my_dict[unit]["latitude"] = lat
                my_dict[unit]["longitude"] = lon
                count += 1

    #pprint(my_dict)
    df = pd.DataFrame(my_dict).transpose()
    df = df[['latitude', 'longitude', 'district', 'division', 'area']]
    df.index.name = "unit number"
    df = df.sort_values(by=["area","division","district"])
    df.to_csv(path_or_buf = "tableau_output.csv")

##### Compare Final & Baseline #################################################################
# Make dictionaries for district, division, and area with units as the values
def disctionaries_for_baseline():
    district_dict = {}
    division_dict = {}
    area_dict = {}
    count = 0

    for line in open("tableau_output.csv", 'r'):
        line = line.split(",")

        # Get rid of headers
        if count == 0:
            count += 1
            continue
        # Extract unit, division, and area from line in tableau_output.csv file

        unit = round(float(line[0]))
        if run_district:
            district = line[3]
            if district != "":
                district = round(float(line[3]))

            # If the district is not yet in the dictionary, add it with the unit as the first value
            if district not in district_dict.keys():
                district_dict[district] = [unit]
            # If the district is in the dictionary, add the unit to that district
            else:
                district_dict[district].append(unit)


        if run_division:
            division = line[4]
            if division != "":
                division = round(float(line[4]))

            if division not in division_dict.keys():
                division_dict[division] = [unit]
            else:
                division_dict[division].append(unit)


        if run_area:
            area = line[5]
            if area.strip() != "":
                area = round(float(line[5]))

            if area not in area_dict.keys():
                area_dict[area] = [unit]
            else:
                area_dict[area].append(unit)


def district_summary():
#District Summary
    avg_distance = 0
    print("---------------District---------------")

    distances = []
    table = convert_table_to_dict("unit_distances.csv")
    for district in district_dict:
        unit_list = district_dict[district]
        total = 0
        count = 0
        for num1 in range(len(unit_list)):
            for num2 in  range(num1 + 1,len(unit_list)):
                unit1 = unit_list[num1]
                unit2 = unit_list[num2]
                distance = table[unit1][unit2]
                total += distance
                count += 1
        avg = total / count
        distances.append(avg)

    min_distance = round(min(distances), 1)
    avg_distance = round(sum(distances) / len(distances), 1)
    max_distance = round(max(distances), 1)
    print("Number of Districts: {}".format(district_dict.keys()))
    print("Distances:")
    print("\tMin = {}\n\tAvg = {}\n\tMax = {}\n".format(min_distance, avg_distance, max_distance))



    difficulties = []
    for district in district_dict:
        total = 0
        count = 0
        for unit in district_dict[district]:
            difficulty = Get_Difficulty(unit,0)
            total += difficulty
            count += 1
        avg = total / count
        difficulties.append(avg)

    min_diff = round(min(difficulties), 1)
    avg_diff = round(sum(difficulties) / len(difficulties), 1)
    max_diff = round(max(difficulties), 1)
    print("Difficulty:")
    print("\tMin = {}\n\tAvg = {}\n\tMax = {}\n".format(min_diff, avg_diff, max_diff))

    durations = []
    table = convert_table_to_dict("unit_durations.csv")
    for district in district_dict:
        unit_list = district_dict[district]
        total = 0
        count = 0
        for num1 in range(len(unit_list)):
            for num2 in  range(num1 + 1,len(unit_list)):
                unit1 = unit_list[num1]
                unit2 = unit_list[num2]
                duration = table[unit1][unit2]
                total += duration
                count += 1
        avg = total / count
        durations.append(avg)

    min_duration = round(min(durations), 1)
    avg_duration = round(sum(durations) / len(durations), 1)
    max_duration = round(max(durations), 1)

    print("Durations:")
    print("\tMin = {}\n\tAvg = {}\n\tMax = {}\n".format(min_duration, avg_duration, max_duration))

def division_summary():
#Division Summary
    avg_distance = 0

    difficulties = []
    for division in division_dict:
        total = 0
        count = 0
        for unit in division_dict[division]:
            difficulty = Get_Difficulty(unit,0)
            total += difficulty
            count += 1
        avg = total / count
        difficulties.append(avg)

    min_diff = round(min(difficulties), 1)
    avg_diff = round(sum(difficulties) / len(difficulties), 1)
    max_diff = round(max(difficulties), 1)
    print("---------------Division---------------")
    print("Difficulty:")
    print("\tMin = {}\n\tAvg = {}\n\tMax = {}\n".format(min_diff, avg_diff, max_diff))

def area_summary():
#Area Summary
    avg_distance = 0

    difficulties = []
    for area in area_dict:
        total = 0
        count = 0
        for unit in area_dict[area]:
            difficulty = Get_Difficulty(unit,0)
            total += difficulty
            count += 1
        avg = total / count
        difficulties.append(avg)

    min_diff = round(min(difficulties), 1)
    avg_diff = round(sum(difficulties) / len(difficulties), 1)
    max_diff = round(max(difficulties), 1)
    print("-----------------Area-----------------")
    print("Difficulty:")
    print("\tMin = {}\n\tAvg = {}\n\tMax = {}".format(min_diff, avg_diff, max_diff))


##### GUI Outputs ##############################################################################
