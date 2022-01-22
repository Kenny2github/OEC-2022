import numpy as np
import os
import math
import scipy


#each waste has closest local facility
def distance(pt1, pt2):
    (x1,y1) = pt1
    (x2,y2) = pt2
    return math.sqrt((x1-x2)**2+(y1-y2)**2)



def LocalSortPair(local_sort, waste_pts):
    local_to_waste = {}
    sort_waste = []

    closest_dist = 1000000
    for sort_facility in local_sort:
        x = float(sort_facility[1])
        y = float(sort_facility[2])
        local_to_waste[(x,y)] = 0
        dist = 100000000 #big value to be replaced
        closest_waste = []
        for waste in waste_pts:
            waste_x = float(waste[1])
            waste_y = float(waste[2])
            if distance((x,y), (waste_x, waste_y)) <= dist:
                closest_waste = waste
                dist = distance((x,y), (waste_x, waste_y))
        local_to_waste[(x,y)] = closest_waste
        if distance((x,y), (float(local_to_waste[(x,y)][1]), float(local_to_waste[(x,y)][2]))) <= closest_dist:
            sort_waste = [sort_facility, local_to_waste[(x,y)]]
            closest_dist = distance((x,y), (float(local_to_waste[(x,y)][1]), float(local_to_waste[(x,y)][2])))
    return local_to_waste, sort_waste

def RegionalSortPair(regional_sort, waste_pts): # need to remove from waste_pts
    regional_to_waste = {}
    sort_waste = []
    closest_dist = 1000000
    for sort_facility in regional_sort:
        x = float(sort_facility[1])
        y = float(sort_facility[2])
        regional_to_waste[(x,y)] = 0
        dist = 100000000 #big value to be replaced
        closest_waste = []
        for waste in waste_pts:
            waste_x = float(waste[1])
            waste_y = float(waste[2])
            if distance((x,y), (waste_x, waste_y)) <= dist:
                closest_waste = waste
                dist = distance((x,y), (waste_x, waste_y))
        regional_to_waste[(x,y)] = closest_waste
        if distance((x,y), (float(regional_to_waste[(x,y)][1]), float(regional_to_waste[(x,y)][2]))) <= closest_dist:
            sort_waste = [sort_facility, regional_to_waste[(x,y)]]
            closest_dist = distance((x,y), (float(regional_to_waste[(x,y)][1]), float(regional_to_waste[(x,y)][2])))
    return regional_to_waste, sort_waste

def RecyclingSortPair(regional_sort, waste_pts): # need to remove from waste_pts
    regional_to_waste = {}
    sort_waste = []

    closest_dist = 1000000
    for sort_facility in regional_sort:
        x = float(sort_facility[1])
        y = float(sort_facility[2])
        regional_to_waste[(x,y)] = 0
        dist = 100000000 #big value to be replaced
        closest_waste = []
        for waste in waste_pts:
            waste_x = float(waste[1])
            waste_y = float(waste[2])
            if distance((x,y), (waste_x, waste_y)) <= dist:
                closest_waste = waste
                dist = distance((x,y), (waste_x, waste_y))
        regional_to_waste[(x,y)] = closest_waste
        if distance((x,y), (float(regional_to_waste[(x,y)][1]), float(regional_to_waste[(x,y)][2]))) <= closest_dist:
            sort_waste = [sort_facility, regional_to_waste[(x,y)]]
            closest_dist = distance((x,y), (float(regional_to_waste[(x,y)][1]), float(regional_to_waste[(x,y)][2])))
    return regional_to_waste, sort_waste

class Truck():
    def __init__(self):
        self.waste = 0
        self.localsorted = 0
        self.regionalsorted = 0
        self.recycled = 0

data = np.loadtxt("c:\\users\\roryg\\desktop\\oec2022\\oec-2022\\test cases\\small\\test_100_equal.csv", dtype=str, delimiter=',')

GarbageTruck = Truck()

waste_pts =[]
local_sort = []
regional_sort = []
regional_recycle = []



for row in data:
    if row[3] == "waste":
        waste_pts.append(row)
    if row[3] == "local_sorting_facility":
        local_sort.append(row)
    if row[3] == "regional_sorting_facility":
        regional_sort.append(row)
    if row[3] == "regional_recycling_facility":
        regional_recycle.append(row)

start_pos = [float(waste_pts[0][1]), float(waste_pts[0][2])]
end_condition = 0
for waste in waste_pts:
    end_condition += float(waste[4]) #end condition is total amount of garbage




copy_waste_pts = waste_pts[:] #deep copy for identifying pairs


local_waste_dict, local_waste_pair = LocalSortPair(local_sort, copy_waste_pts) #identify closest garbage to local sort

i = 0
for waste in copy_waste_pts:
    if waste[0] == local_waste_pair[1][0]:
        copy_waste_pts.pop(i)
        break
        ##print(i)
    i+=1

regional_waste_dict, regional_waste_pair = RegionalSortPair(regional_sort, copy_waste_pts) #identify closest garbage to regional sort

i = 0
for waste in copy_waste_pts:
    if waste[0] == regional_waste_pair[1][0]:
        copy_waste_pts.pop(i)
        break
        ##print(i)
    i+=1

recycling_waste_dict, recycling_waste_pair = RecyclingSortPair(regional_recycle, copy_waste_pts) #identify closest garbage to recycling

#use greedy algorithm to travel to all points,
cur_pos = start_pos
moves = []

##print(copy_waste_pts)
while GarbageTruck.recycled != end_condition:
    dist = 10000000.0 #large number
    ##print(len(copy_waste_pts))
    for waste in copy_waste_pts: # first identify closest waste
        waste_x = float(waste[1])
        waste_y = float(waste[2])
        if distance(cur_pos, (waste_x, waste_y)) <= dist:
            #cur_pos = (waste_x, waste_y) #we go pick this up
            target_waste = waste
            dist = distance(cur_pos, (waste_x, waste_y))
            ##print(cur_pos, waste[0], distance(cur_pos, (waste_x, waste_y)))
        ##print(cur_pos, (waste_x, waste_y))
        #print(distance(cur_pos, (waste_x, waste_y)))
    i = 0
    for waste1 in copy_waste_pts:
        ##print("tgt", target_waste[0])
        if waste1[0] == target_waste[0]:
            ##print("i",i)
            ##print("waste1",waste1)
            copy_waste_pts.pop(i)
            break
            ##print(copy_waste_pts)
        i+=1
    ##print(cur_pos)
    ##print(copy_waste_pts)
    cur_pos = [float(target_waste[1]),float(target_waste[2])]
    #print("chosen",cur_pos) #update position
    moves.append(target_waste)#update move
    print(target_waste)
    if len(copy_waste_pts)==0:
        GarbageTruck.recycled = end_condition

    #Now that we moved to all garbage points, move to garbage point pair
moves.append(local_waste_pair[1])
moves.append(local_waste_pair[0]) # move to local sort facility
moves.append(regional_waste_pair[1])
moves.append(regional_waste_pair[0])
moves.append(recycling_waste_pair[1])
moves.append(recycling_waste_pair[0])
#print(moves)
#we have to deal with the leftover garbage


copy_local_pts = local_sort[:] # hard copy because we need to delete
dist = 1000000
for local in local_sort: # first identify closest waste
    local_x = float(local[1])
    local_y = float(local[2])
    if distance(cur_pos, (local_x, local_y)) <= dist:
        #cur_pos = (local_x, local_y) #we go pick this up
        target_local = local
        dist = distance(cur_pos, (local_x, local_y))
        ##print(cur_pos, local[0], distance(cur_pos, (local_x, local_y)))
    ##print(cur_pos, (local_x, local_y))
    ##print(distance(cur_pos, (local_x, local_y)))
i = 0
for local1 in copy_local_pts:
    ##print("tgt", target_local[0])
    if local1[0] == target_local[0]:
        ##print("i",i)
        ##print("local1",local1)
        copy_local_pts.pop(i)
        break
        ##print(copy_local_pts)
    i+=1
##print(cur_pos)
##print(copy_local_pts)
cur_pos = [float(target_local[1]),float(target_local[2])]
##print("chosen",cur_pos) #update position
moves.append(target_local)#update move
#First identify closely linked local sort and local nodes


copy_regional_pts = regional_sort[:] # hard copy because we need to delete
dist = 1000000
for regional in regional_sort: # first identify closest waste
    regional_x = float(regional[1])
    regional_y = float(regional[2])
    if distance(cur_pos, (regional_x, regional_y)) <= dist:
        #cur_pos = (regional_x, regional_y) #we go pick this up
        target_regional = regional
        dist = distance(cur_pos, (regional_x, regional_y))
        ##print(cur_pos, regional[0], distance(cur_pos, (regional_x, regional_y)))
    ##print(cur_pos, (regional_x, regional_y))
    ##print(distance(cur_pos, (regional_x, regional_y)))
i = 0
for regional1 in copy_regional_pts:
    ##print("tgt", target_regional[0])
    if regional1[0] == target_regional[0]:
        ##print("i",i)
        ##print("regional1",regional1)
        copy_regional_pts.pop(i)
        break
        ##print(copy_regional_pts)
    i+=1
##print(cur_pos)
##print(copy_regional_pts)
cur_pos = [float(target_regional[1]),float(target_regional[2])]
##print("chosen",cur_pos) #update position
moves.append(target_regional)#update move
#First identify closely linked regional sort and regional nodes

#print(moves)

copy_recycle_pts = regional_recycle[:] # hard copy because we need to delete
dist = 1000000
for recycle in regional_recycle: # first identify closest waste
    recycle_x = float(recycle[1])
    recycle_y = float(recycle[2])
    if distance(cur_pos, (recycle_x, recycle_y)) <= dist:
        #cur_pos = (recycle_x, recycle_y) #we go pick this up
        target_recycle = recycle
        dist = distance(cur_pos, (recycle_x, recycle_y))
        ##print(cur_pos, recycle[0], distance(cur_pos, (recycle_x, recycle_y)))
    ##print(cur_pos, (recycle_x, recycle_y))
    ##print(distance(cur_pos, (recycle_x, recycle_y)))
i = 0
for recycle1 in copy_recycle_pts:
    ##print("tgt", target_recycle[0])
    if recycle1[0] == target_recycle[0]:
        ##print("i",i)
        ##print("recycle1",recycle1)
        copy_recycle_pts.pop(i)
        break
        ##print(copy_recycle_pts)
    i+=1
##print(cur_pos)
##print(copy_recycle_pts)
cur_pos = [float(target_recycle[1]),float(target_recycle[2])]
##print("chosen",cur_pos) #update position
moves.append(target_recycle)#update move
#First identify closely linked regional sort and regional nodes


#now convert np array back to list
#moves= np.array(moves)
np.savetxt("test.csv", moves, delimiter=",", fmt='%s')