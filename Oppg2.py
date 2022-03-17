#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:05:54 2022

@author: hedda
"""

import numpy as np
import pandas as pd 
import seaborn as sns

# Non-shiftable appliances
heat = (6400+6900)/2 #Wh
fridge = float(1320) #Wh
stove = float(3900) #Wh
TV = int((150+600)/2) #Wh for 5 hours a day
computer = float(600) #Wh
lighting = 1500/10 #Wh from 10:00 to 20:00
coffee_maker = 260 #Wh
cell_phone_charger = 50 #Wh

#Shiftable appliances
dishwasher = 1440 #Wh
laudry = 1940 #Wh
dryer = 2500 #Wh
EV = 9900 #Wh

# Additional shiftable appliances
vacuum = 230 #Wh

"""
Electricity from non-shiftable appliances
Assuming they all run at a constant rate throughout the day
"""
constant = (heat + fridge)/24
TV_per_hour =  (TV/5)


"Real-Time Pricing scheme"
hours = np.linspace(1, 24, num = 24)
prices = []
for hour in hours:
    if 16 <= hour <= 20 or 7 <= hour <= 10:
        price = np.random.randint(75, 150)/10000
    if 11 <= hour <= 17:
        price = np.random.randint(50, 125)/10000
    else: 
        price = np.random.randint(25, 75)/10000
    prices.append(price)
    
df = pd.DataFrame(zip(hours, prices), columns=['Hour','Price'])


#Adding the heating and fridge
for index in df.index:
    df.loc[index, 'energy_consumption'] = constant
    
#Adding the lighting from 10:00 to 20:00   
for index in range(9, 19):
    df.energy_consumption[index] += lighting
    
#Adding the computer for seven hours from 8:00 to 15:00
for index in range(7, 14):
    df.energy_consumption[index] += computer

#Adding TVs for five hours from 15:00 to 21:00
for index in range(14, 20):
    df.energy_consumption[index] += TV_per_hour
    
#Adding the stove for an hour from 17:00 to 18:00
df.energy_consumption[16] += stove

lowest_price = df.loc[0, "Price"]
lowest_dayprice = df.loc[8, "Price"] 
for index in df.index:
    if 8 < index < 22:
        if df.loc[index, "Price"] < lowest_dayprice:
            lowest_dayprice = df.loc[index, "Price"]
    if df.loc[index, "Price"] < lowest_price:
        lowest_price = df.loc[index, "Price"]

#Adding the shiftable appliances which can go by night to this time
laundry=0
cleaning=0
for index in df.index:
    if df.loc[index, "Price"] == lowest_price and laundry == 0:
        df.energy_consumption[index] += laudry + dryer + EV + cell_phone_charger
        print('charinging EV, washing and drying clothes')
        laundry = 1
    if df.loc[index, "Price"] == lowest_dayprice and cleaning == 0:
        df.energy_consumption[index] += vacuum
        print('vacuum cleaning')
        cleaning = 1

    
for index in df.index:
    df.loc[index, 'hourly_cost'] = df.Price[index]*df.energy_consumption[index]
        
Total_cost = sum(df.hourly_cost)
print(df)
print(Total_cost)

sns.lineplot(x='Hour', y='Price', data=df)
sns.lineplot(x='Hour', y='energy_consumption', data=df)
sns.lineplot(x='Hour', y='hourly_cost', data=df)