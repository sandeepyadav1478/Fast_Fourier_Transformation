from math import dist
from json import load, dump
import operator

def cordsort(file_path = "coordinate.txt", # location of file
             file_path_bck = "cords_bck.txt", #backup file
             perc = 90,       # save only % of data
             sort = ">",       # sorting format '>' means minimum distance, '<' means longest distance
             loss_level =10,    # every 10th place cord will be removed from list
             format = "Remove"     # 'Keep' will save % of current cords,'Remove' will remove % of current cords
            ):

    exist = 1
    #loading cords
    try:
        file = open(file_path,"r")
    except:
        exist = 0
        return "Need input"
    if exist:
        cors = load(file)
        file.close()
        #
        #creating backup
        file=open(file_path_bck,"w")
        dump(cors,file)
        file.close()
        #
        # assigning sort string to operator work
        ops = { "<": operator.lt, ">": operator.gt, "=": operator.eq }
        #
        #removing repeated values
        cords = []
        for i in cors:
            if i not in cords:
                cords.append(i)
        print("Removed repeated cords :",len(cors)-len(cords))
        #
        #sorting with math distance function
        min_dist=0.0
        min_dist_cords = []
        tmp_len = len(cords)-1
        init = 0
        new_cors = []
        new_cors.append(cords[0])
        cords.remove(cords[0])
        while init < tmp_len :
            for i in cords:
                if i != new_cors[-1]:
                    tmp_dist = dist(new_cors[-1],i)
                    if min_dist == 0.0 or ops[sort](min_dist,tmp_dist):
                        min_dist = tmp_dist
                        min_dist_cords = i
            new_cors.append(min_dist_cords)
            cords.remove(min_dist_cords)
            init+=1
            min_dist = 0.0

        #loss compression data / removing 10th cord from list till number of nodes drop by percentile
        num_cords = len(new_cors)
        if format == "Keep":
            temp = (len(new_cors)* perc)/100
        if format == "Remove":
            temp = (len(new_cors)* (100-perc))/100
        while len(new_cors) > temp:
            if temp <= loss_level:
                break
            del new_cors[1::loss_level]
        if format == "Remove":
            print("Removed",perc,"%, ",num_cords-len(new_cors)," cords are removed.")
        if format == "Keep":
            print("Kept",perc,"%, ",num_cords-len(new_cors)," cords are removed.")
        #
        print(len(new_cors),"cords are saved.")
        file=open(file_path,"w")
        dump(new_cors,file)
        file.close()
        if len(new_cors) > 0:
            return 'Compressed: '+str(len(new_cors))+' cords/points left now.'
        else:
            return "Can't find any pixel"

def undo(file_path = "coordinate.txt", # location of file
        file_path_bck = "cords_bck.txt" #backup file
        ):
    #loading cords
    file = open( file_path_bck, "r")
    cors = load(file)
    file.close()
    #
    if len(cors) > 0:
        file = open( file_path, "r")
        cors_bck = load(file)
        file.close()
        if cors_bck == cors:
            return "All cords are same."
        else:
            #loading cords
            file = open( file_path, "w")
            dump(cors,file)
            file.close()
            #
            return str(len(cors))+" cords are restored."
    else:
        return "No cords available in backup file!"


# cordsort(perc = 100)