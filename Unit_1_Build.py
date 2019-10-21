import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = r'..\Unit_1_Build'
os.chdir(path)

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows',   100)
pd.set_option('display.width',      500)

# What I want:
#  - I want to gather death data on the US
#    - All states
#    - All possible years
#    - Sorted by year, state, county, age, cause of death
#  - Then I want to be able to see all the data in a clickable, sortable way
#  - All alive vs all dead, chunked groups of trauma vs medical, homicide vs suicide, etc.
#  - I also want it to be interactable
#  - Plot everythng along the US by state and county hallucinogens
#    - Heat maps
#    - Time slider, maybe allow a segment of time to view across?







# How to get there:
#  [-] Dataframe of the whole US
#      [X] California 1999 - 2014
#  [ ] Ask and answer a questions
#      [ ]
#  [ ] Make 3 different visualizations
#      [ ] Overall
#      [ ] Plot and Donut
#      [ ] California County Map


# ------------------------------ Data Cleaning ------------------------------ #
# Data pulled from the CDC website. Had to merge once for each year at minimum
# The data was very clean, though in working through the project I've had a few
# minor things to change still
df = pd.read_csv(r'dataframes\CDC Mortality Dataframe California 1999 - 2016.csv', low_memory = False)

df                              = df.drop(['Year Code'], axis = 1)

df                              = df.replace({'Population':                'Not Applicable'
                                             ,'Crude Rate':                'Not Applicable'
                                             ,'Crude Rate Standard Error': 'Not Applicable'}
                                             ,np.NaN)

df['Population']                = df['Population'].fillna(method = 'ffill', limit = 1).astype('int64')
df['Crude Rate']                = df['Crude Rate'].str.strip(' (Unreliable)').astype('float')
df['Crude Rate Standard Error'] = df['Crude Rate Standard Error'].astype('float')

# df.to_csv(r'dataframes\CDC Mortality Dataframe California 1999 - 2016 CLEANED.csv')

# print(df.head())
# print(df.dtypes)
# ------------------------------ Data Cleaning ------------------------------ #



# ----------------------------------- Work ----------------------------------- #
#  [] Create something that allows me to view the data correctly
# I need a way to filter based on arbitrary stats, e.g. County, Age Group, etc.
# I need a way of summing the number of deaths per type of death,
# or within any other category
#


# Use this to select subsets of data
filter = [['Year',           1999]
         ,['County',         'Alameda']
         ,['Age Group',      '< 1 year']
         ,['Cause of death', 'Extreme immaturity']
         ]
# The comparison creeates a True/False dataframe, which can then be used to
# filter for what we want to use

filtered_df = df

filtered_df = filtered_df[filtered_df[filter[0][0]] == filter[0][1]]
filtered_df = filtered_df[filtered_df[filter[1][0]] == filter[1][1]]
# filtered_df = filtered_df[filtered_df[filter[2][0]] == filter[2][1]]
# filtered_df = filtered_df[filtered_df[filter[3][0]] == filter[3][1]]

print(filtered_df.shape)
print(filtered_df.head())

#  [ ]
#  [ ]
# print(df['State'].unique())
# print(df['County'].unique())
# print(df['Age Group'].unique())
# print(df['Cause of death'].unique())
# ----------------------------------- Work ----------------------------------- #



# ---------------------------------- Output ---------------------------------- #
#  [ ] Present the data in an understandable way

# ----- Build this into something moddable ----- #
# # Make data: I have 3 groups and 7 subgroups
# group_names    = ['groupA', 'groupB', 'groupC']
# group_size     = [12,11,30]
# subgroup_names = ['A.1', 'A.2', 'A.3', 'B.1', 'B.2', 'C.1', 'C.2', 'C.3', 'C.4', 'C.5']
# subgroup_size  = [4,3,5,6,5,10,5,5,4,6]
#
# # Create colors
# a, b, c=[plt.cm.Blues, plt.cm.Reds, plt.cm.Greens]
#
# # First Ring (outside)
# fig, ax = plt.subplots()
# ax.axis('equal')
# mypie, _ = ax.pie(group_size, radius=1.3, labels=group_names, colors=[a(0.6), b(0.6), c(0.6)] )
# plt.setp( mypie, width=0.3, edgecolor='white')
#
# # Second Ring (Inside)
# mypie2, _ = ax.pie(subgroup_size, radius=1.3-0.3, labels=subgroup_names, labeldistance=0.7, colors=[a(0.5), a(0.4), a(0.3), b(0.5), b(0.4), c(0.6), c(0.5), c(0.4), c(0.3), c(0.2)])
# plt.setp( mypie2, width=0.4, edgecolor='white')
# plt.margins(0,0)
#
# plt.show()

# ----- Build this into something moddable ----- #


# ----- California County Map Plot ----- #

# ----- California County Map Plot ----- #
# ---------------------------------- Output ---------------------------------- #
