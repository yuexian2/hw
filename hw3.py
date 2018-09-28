## Team member: Yingyi Lai & Yue Xian

## We worked together all the question and code.

# global parameters

from pygeodesy import ellipsoidalVincenty as ev

Dict = {}
Property_list = []
StormID = 'c'
Direction = ['NE','SE','SW','NW']
count = 0
CountTrue = 0

# read the first dataset

with open('1.txt','r') as f:
    for line in f:
        values_on_line =line.split(',')
        if values_on_line[0][0].isalpha():
            Dict[StormID] = Property_list
            Property_list = []
            knotmax = 0
            StormID = values_on_line[0]
            name = values_on_line[1].strip()
            recdlen=int(values_on_line[2])
            if name == 'UNNAMED':
                 name = ' '
            Property_list.append(name)

            for i in range(recdlen):
                line = next(f)
                time=[]
                maxdate = line[0]
                values_on_line = line.split(',')
                Date = values_on_line[0]
                radius = []
                Quadrant = [ ]
                ind = []

                # print(Quadrant)
                if i==0:
                    StDate = Date
                    Property_list.append(StDate)
                    t=[]
                    Coordinate_X = []
                    Coordinate_Y = []
                    Time = []
                # collect the x,y coordinates in a list
                Coordinate_X.append(values_on_line[4].strip())
                Coordinate_Y.append(values_on_line[5].strip())
                if i >= 1:
                    # in order to clear '999'data
                    if ' -999' not in values_on_line[8:]:

                        for k in range(3):
                            radius.append([])

                            for radii in range(4):
                                radius[k].append(int(values_on_line[8 + radii + k * 4]))  # 输出一个包含三种type风的半径的list
                            # print(radius)
                        a = ev.LatLon(Coordinate_X[i - 1], Coordinate_Y[i - 1])
                        b = ev.LatLon(Coordinate_X[i], Coordinate_Y[i])
                        radius.reverse()
                        # print(radius)
                        if a != b:
                            for types in radius:
                                # print(max(types))
                                if max(types) != 0:  # 进入第一种风
                                    maxr = max(types)
                                    # print("max",maxr)
                                    ind = [i for i, j in enumerate(types) if j == maxr]
                                    # print(ind)
                                    for order in range(len(ind)):
                                        Quadrant.append(Direction[ind[order]])
                                    # print(Quadrant)
                                    Bearing = a.bearingTo(b)
                                    Bearing = Bearing + 110
                                    if Bearing > 360:
                                        Bearing = Bearing-360
                                    count = count+1 # 统计总的record的数量
                                    for quad in Quadrant:
                                        if quad == 'NE' and Bearing >=0 and Bearing<=90:
                                            CountTrue = CountTrue+1
                                        if quad == 'SE' and Bearing >=90 and Bearing<=180:
                                            CountTrue = CountTrue+1
                                        if quad == 'SW' and Bearing >=180 and Bearing<=270:
                                            CountTrue = CountTrue+1
                                        if quad == 'NW' and Bearing >=270 and Bearing<=360:
                                            CountTrue = CountTrue+1
                                    break

                if values_on_line[1].strip()[0] == '0':
                    time.append(values_on_line[1].strip()[1])
                    time.append(values_on_line[1].strip()[2:4])
                    time.append(Date[-2:])
                else:
                    time.append(values_on_line[1].strip()[0:2])
                    time.append(values_on_line[1].strip()[2:4])
                    time.append(Date[-2:])

                Time.append(time)

                t.append(values_on_line[2].strip())
                knot = int(values_on_line[6])
                if knot > knotmax:
                    knotmax = knot
                    maxdate = Date
                if i ==(recdlen - 1):
                    Enday = Date
                    Property_list.append(Enday)

            Property_list.append(knotmax)
            Property_list.append(maxdate)
            Property_list.append(t.count('L'))
            travel_time = []
            if len(Time)==1:
                travel_time = 'N/A'
            else:
                for i in range(len(Coordinate_X)-1):
                    if Time[i+1][2] == Time[i][2]:
                        travel_time.append(int(Time[i+1][0])-int(Time[i][0])+int(Time[i+1][1])/60-int(Time[i][1])/60)
                    else:
                        travel_time.append(int(Time[i+1][0]) + 24 - int(Time[i][0])+int(Time[i+1][1])/60-int(Time[i][1])/60)
            # print(travel_time)
            total_distance = 0
            max_speed = 'N/A'
            ave_speed = 'N/A'
            if len(Coordinate_X) == 1:
                total_distance = 'N/A'
                ave_speed = 'N/A'
                max_speed = 'N/A'
            else:
                travel_speed = []
                BearingList = []
                for j in range(len(Coordinate_X)-1):
                    a = ev.LatLon(Coordinate_X[j], Coordinate_Y[j])
                    b = ev.LatLon(Coordinate_X[j+1], Coordinate_Y[j+1])

                    if a != b :
                        total_distance = total_distance + a.distanceTo3(b)[0]/1852.0
                        travel_speed.append(float(a.distanceTo3(b)[0])/float(travel_time[j])/1852.0)
                        # in order to exclude the useless data



                if travel_speed:
                    max_speed = max(travel_speed)

            if total_distance != 'N/A'and travel_time != 'N/A':
                ave_speed = float(total_distance)/(sum(travel_time))
            if total_distance == 0:
                total_distance = 'N/A'
                ave_speed = 'N/A'
            Property_list.append(total_distance)
            Property_list.append(max_speed)
            Property_list.append(ave_speed)


            # print(BearingList)
            print(Property_list)

# read the second dataset





del Dict['c']
Dict[StormID] = Property_list
print(CountTrue,count)





# print(Dict)

# print(Dict)

# Year={}
# Agg=[]
#
# for ID in Dict.keys():
#     allvar = Dict[ID]
#     print(allvar)
#     year=int(allvar[1][:4])
#     Year[ID] = year
#     if int(allvar[3]) >= 64:
#         ans='Hurricane!'
#     else:
#         ans='Not Hurricane'
#     Agg.append([ID,year, ans])
# print(Agg)
# # # define Count function : it first flipped the dictionary and then count the number of values, and print out
#
# def Count (Dict):
#     flipped = {}
#     new=[]
#     for k in Dict.keys():
#         v = Dict[k]
#         if v not in flipped:
#             flipped[v] = [k]
#         else:
#             flipped[v].append(k)
#     # print(flipped)
#     for x in flipped.keys():
#          new.append([x, len(flipped[x])])
#     return new
#
# Year1=Count(Year)
#
# # Count the number of Hurricane per year
#
# Hurr={}
# for info in Agg:
#     if info[2]=='Hurricane!':
#         Hurr[info[0]]=info[1]
# # print(Hurr)
# Year2=Count(Hurr)  # print the number of Hurricane each year
#
#
# # ouput
# file = open('Result.txt', 'w')
#
# #
# file.write("Output Data: \n")
# for ID in Dict.keys():
#     file.write('StormID : {:10}'.format(str(ID)) + '\tStorm Name : {:15}'.format(str(Dict[ID][0]))+ '\tDate range is : {} - {} \t'.format(str(Dict[ID][1]), str(Dict[ID][2])) +
#             'Highest Maximum Knots are : {:4}'.format(str(Dict[ID][3])) + '\tDate :{:10}'.format(str(Dict[ID][4])) +'\tTime of Landfall are :{:3}'.format(str(Dict[ID][5])) + '\n')
#
# file.write("\nTotal number of Storm each year :\n")
# for i in range(len(Year1)):
#      file.write('Year : {:6}\t Total number of Storm : {}\n'.format(str(Year1[i][0]),str(Year1[i][1])))
#
# file.write("\nTotal Number of Hurricane each year:\n")
# for i in range(len(Year2)):
#      file.write('Year : {:6}\t Total number of hurricane : {}\n'.format(str(Year2[i][0]),str(Year2[i][1])))


# file.close
