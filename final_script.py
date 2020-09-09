# usage: python final_script.py (int)time-to-run
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
import platform
import sys
import pandas as pd
import numpy as np
from scipy import signal as sig
import pyfiglet

z_list = []
walk_list = [False,False]
step = pd.read_csv('./step_template.csv')
j = 0
template = step['acc']

epsilon = float(42)
n = len(template)
D_recent = [float("inf")]*(n)
D_now=[0]*(n)
S_recent=[0]*(n)
S_now=[0]*(n)
d_rep=float("inf")
J_s=float("inf")
J_e=float("inf")
check=0
len_matches_previous = 0

matches=[]

total_steps = 0

class State:
    def __init__(self, device):
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.algo)

    def algo(self, ctx, data):
        global j,template,epsilon,n,D_recent,D_now,S_recent,S_now,d_rep,J_s,J_e,check,matches,total_steps, len_matches_previous
        self.samples+= 1
        dataz = parse_value(data).y
        
        if len(z_list) < 250:
            z_list.append(dataz)
        else:
            z_list.pop(0)
            z_list.append(dataz)

        if self.samples >= 250 and self.samples % 50 == 0:
            f, psd = sig.welch(z_list,fs=100,window='hanning',nperseg=250,detrend='constant')
            if np.mean(psd[2:6])>np.mean(psd[:2]) and np.mean(psd[2:6])>0.002:
                walk_list.append(True)
                if walk_list[-2:] == [False,True]:
                    print(pyfiglet.figlet_format('walking'))
                    #total_steps+=1
                    #print(pyfiglet.figlet_format(f'{total_steps} steps'))
                    #total_steps+=1
                    #print(pyfiglet.figlet_format(f'{total_steps} steps'))
                    
            else:
                walk_list.append(False)
                D_recent = [float("inf")]*(n)
                D_now=[0]*(n)
                S_recent=[0]*(n)
                S_now=[0]*(n)
                d_rep=float("inf")
                J_s=float("inf")
                J_e=float("inf")
                check=0
                j = 0
                matches=[]
                if walk_list[-2:] == [True,False]:
                    print(pyfiglet.figlet_format('not walking'))

        acc_z = (int(dataz) - np.mean(z_list)) / np.std(z_list) + 0.00001


        #calculation of accumulated distance for each incoming value
        def accdist_calc (incoming_value, temp, Distance_new, Distance_recent):
            for i in range(len(temp)):
                if i == 0:
                    #start point is corner
                    Distance_new[i] = (incoming_value-temp[i])**2
                else:
                    #next point is previous value plus most efficient step
                    Distance_new[i] = ((incoming_value-temp[i])**2) + min(Distance_new[i-1], Distance_recent[i], Distance_recent[i-1])
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
        
        if self.samples >= 250 and walk_list[-1]:   
            x = acc_z
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
                matches.append(str(d_rep)+","+str(J_s)+","+str(J_e))
                #total_steps += 1
                #print(total_steps)
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

            j+=1
     
            match_idx = []
            for idx,match in enumerate(matches):
                for match2 in matches:
                    list1 = [int(match.split(',')[1]), int(match.split(',')[2])]
                    list2 = [int(match2.split(',')[1]), int(match2.split(',')[2])]
                    if list1 != list2 and list1[0] >= list2[0] and list1[1] <= list2[1]:
                        match_idx.append(idx)
                        
            matches = [match for idx,match in enumerate(matches) if idx not in match_idx]

            if len(matches) > len_matches_previous:
                total_steps += len(matches) - len_matches_previous
                print(pyfiglet.figlet_format(f'{total_steps} steps'))

            len_matches_previous = len(matches)
            
            
states = []

d = MetaWear("FC:A3:80:92:67:06")
d.connect()
print("Connected to " + d.address)
states.append(State(d))

print("Configuring device")
libmetawear.mbl_mw_settings_set_connection_parameters(states[0].device.board, 7.5, 7.5, 0, 6000)
sleep(1.5)

libmetawear.mbl_mw_acc_set_odr(states[0].device.board, 100.0)
libmetawear.mbl_mw_acc_set_range(states[0].device.board, 16.0)
libmetawear.mbl_mw_acc_write_acceleration_config(states[0].device.board)

signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(states[0].device.board)
libmetawear.mbl_mw_datasignal_subscribe(signal, None, states[0].callback)

libmetawear.mbl_mw_acc_enable_acceleration_sampling(states[0].device.board)
libmetawear.mbl_mw_acc_start(states[0].device.board)

sleep(int(sys.argv[1]))

libmetawear.mbl_mw_acc_stop(states[0].device.board)
libmetawear.mbl_mw_acc_disable_acceleration_sampling(states[0].device.board)

signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(states[0].device.board)
libmetawear.mbl_mw_datasignal_unsubscribe(signal)
libmetawear.mbl_mw_debug_disconnect(states[0].device.board)

print("%s -> %d" % (states[0].device.address, states[0].samples))
