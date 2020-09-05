import pandas as pd
import numpy as np
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy import signal
import parseTraces as pt   
    
    
    
accTs, accData, gyroTs, gyroData, magnTs, magnData = pt.parseTrace(f'./walking_data/{subj[0]}')

acc_z = [item[2] for item in accData][list(subj_dict.items())[0][1][0]:list(subj_dict.items())[0][1][1]]
#gyro_x = [item[2] for item in gyroData][list(subj_dict.items())[0][1][0]:list(subj_dict.items())[0][1][1]]

acc_z = (acc_z - np.mean(acc_z)) / np.std(acc_z)
#gyro_x = (gyro_x - np.mean(gyro_x)) / np.std(gyro_x)

#HERE DEFINE 
#1)template consisting of numerical data points 
#2)stream consisting of numerical data points
template = step['acc']
stream = acc_z

#the threshold for the matching process has to be chosen by the user - yet in reality the choice of threshold is a non-trivial problem regarding the quality of the matching process
#Getting Epsilon from the user 

#epsilon = input("Please define epsilon: ")
#epsilon = float(epsilon)

epsilon = float('inf') #max distance threshold

#SPRING
#1.Requirements
n = len(template)
D_recent = [float("inf")]*(n)
D_now=[0]*(n)
S_recent=[0]*(n)
S_now=[0]*(n)
d_rep=float("inf")
J_s=float("inf")
J_e=float("inf")
check=0

#check/output
matches=[]

#calculation of accumulated distance for each incoming value
def accdist_calc (incoming_value, temp, Distance_new, Distance_recent):
    for i in range(len(temp)):
        if i == 0:
            #start point is corner
            ## need to square ??
            #Distance_new[i] = abs(incoming_value-temp[i])
            Distance_new[i] = (incoming_value-temp[i])**2
        else:
            #next point is previous value plus most efficient step
            ## need to square??
            #Distance_new[i] = abs(incoming_value-temp[i])+min(Distance_new[i-1], Distance_recent[i], Distance_recent[i-1])
            Distance_new[i] = ((incoming_value[0]-temp[i][0])**2) + ((incoming_value[1]-temp[i][1])**2) + min(Distance_new[i-1], Distance_recent[i], Distance_recent[i-1])
    return Distance_new

#deduce starting point for each incoming value
def startingpoint_calc (template_length, starting_point_recent, starting_point_new, Distance_new, Distance_recent):
    for i in range (template_length):
            if i == 0:
                #here j+1 instead of j, because of the programm counting from 0 instead of from 1
                starting_point_new[i] = j+1
            else:
                if Distance_new[i-1] == min(Distance_new[i-1], Distance_recent[i], Distance_recent[i-1]):
                    starting_point_new[i] = starting_point_new[i-1]                    
                elif Distance_recent[i] == min(Distance_new[i-1], Distance_recent[i], Distance_recent[i-1]):
                    starting_point_new[i] = starting_point_recent[i]                    
                elif Distance_recent[i-1] == min(Distance_new[i-1], Distance_recent[i], Distance_recent[i-1]):
                    starting_point_new[i] = starting_point_recent[i-1]                    
    return starting_point_new     

#2.Calculation for each incoming point x.t - simulated here by simply calculating along the given static list
for j in range (stream.shape[0]): # change to while loop?
    
    x = stream[j]
    accdist_calc (x,template,D_now,D_recent) # takes Distance_new as input and returns updated version
    startingpoint_calc (n, S_recent, S_now, D_now, D_recent) # takes S_now (starting_point_now) as input and returns updated version

    #Report any matching subsequence
    if D_now[n-1] <= epsilon: # last item in path list == distance, if less than thresh then: 
        if D_now[n-1] <= d_rep: # 
            d_rep = D_now[n-1] # most recent minimum distance
            J_s = S_now[n-1] # updated starting point         
            J_e = j+1 # ending point
            #print("REPORT: Distance "+str(d_rep)+" with a starting point of "+str(J_s)+" and ending at "+str(J_e))              

    #Identify optimal subsequence
    for i in range (n): # for i in length of template
        if D_now[i] >= d_rep or S_now[i] > J_e: # if accumulated distance at i position in template is greater than or equal to last position minimum distance
            check = check+1                     # OR deduced starting point for i position is greater than the ending point
    if check == n: # if check equals length of template, then add match
        #print("MATCH: Distance "+str(d_rep)+" with a starting point of "+str(J_s)+" and ending at "+str(J_e))
        matches.append(str(d_rep)+","+str(J_s)+","+str(J_e))
        d_rep = float("inf")
        J_s = float("inf")
        J_e = float("inf")
        check = 0 
    else:
        check = 0

    #define the recently calculated distance vector as "old" distance
    for i in range (n):
        D_recent[i] = D_now[i]
        S_recent[i] = S_now[i]
        
match_idx = []
for idx,match in enumerate(matches):
    for match2 in matches:
        list1 = [int(match.split(',')[1]), int(match.split(',')[2])]
        list2 = [int(match2.split(',')[1]), int(match2.split(',')[2])]
        if list1 != list2 and list1[0] >= list2[0] and list1[1] <= list2[1]:
            match_idx.append(idx)
            
matches = [match for idx,match in enumerate(matches) if idx not in match_idx]

fig, ax = plt.subplots()
ax.plot(acc_z)
for match in matches:
    ax.axvspan(int(match.split(',')[1]), int(match.split(',')[2]), alpha=0.5, color='red')

plt.xlim([2000,2500])
plt.show()
print(len(matches))

#fig, ax = plt.subplots()
#ax.plot(gyro_x)
#for match in matches:
    #ax.axvspan(int(match.split(',')[1]), int(match.split(',')[2]), alpha=0.4, color='green')

#plt.xlim([1500,2500])
#plt.show()
#print(len(matches))