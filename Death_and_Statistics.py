import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as geo
import re
from textwrap import fill


# path = r'..\Unit_1_Build'
# os.chdir(path)

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
#  [ ] Ask and answer a question
#      [ ] I know that medical deaths are far more common than those by crime,
#          cardiac arrest alone is 800k per year iirc while all firearm deaths
#          combined, even including suicides is barely 25k. Without suicides
#          it's a third of that. I want to visualize this
#  [ ] Make 3 different visualizations
#      [ ] Overall
#      [ ] Plot and Donut
#      [ ] California County Map
# [ ] Connect this project to github.io
#
# train_features.profile_report() # Need to look at this later


# ------------------------------ Data Cleaning ------------------------------ #
# Data pulled from the CDC website. Had to merge once for each year at minimum
# The data was very clean, though in working through the project I've had a few
# minor things to change still


df = pd.read_csv(r'data\CDC Mortality Dataframe California 1999 - 2016.csv', low_memory = False)

df                              = df.drop(['Year Code'], axis = 1)

df                              = df.replace({'Population':                'Not Applicable'
                                             ,'Crude Rate':                'Not Applicable'
                                             ,'Crude Rate Standard Error': 'Not Applicable'}
                                             ,np.NaN)

df['Population']                = df['Population'].fillna(method = 'ffill', limit = 1).astype('int64')
df['Crude Rate']                = df['Crude Rate'].str.strip(' (Unreliable)').astype('float')
df['Crude Rate Standard Error'] = df['Crude Rate Standard Error'].astype('float')
df = df.rename(columns = {'Cause of death':      'Cause of Death'
                         ,'Cause of death Code': 'Cause of Death Code'})


df['Age Group'] = df['Age Group'].replace({'1-4 years':   '1 - 4 years'
                                          ,'5-9 years':   '5 - 9 years'
                                          ,'10-14 years': '10 - 14 years'
                                          ,'15-19 years': '15 - 19 years'
                                          ,'20-24 years': '20 - 24 years'
                                          ,'25-34 years': '25 - 34 years'
                                          ,'35-44 years': '35 - 44 years'
                                          ,'45-54 years': '45 - 54 years'
                                          ,'55-64 years': '55 - 64 years'
                                          ,'65-74 years': '65 - 74 years'
                                          ,'75-84 years': '75 - 84 years'
                                          })

# df.to_csv(r'data\CDC Mortality Dataframe California 1999 - 2016 CLEANED.csv')

# ------------------------------ Data Cleaning ------------------------------ #




# ----------------------------------- Work ----------------------------------- #
# I need a way to filter based on arbitrary stats, e.g. County, Age Group, etc.

# The default values for ALL RESULTS
years           = range(1999, 2017, 1)
states          = range(   1,   51, 1)
counties        = range(6001, 6116, 1)
age_group_codes = ['1'
                  ,'1-4'
                  ,'5-9'
                  ,'10-14'
                  ,'15-19'
                  ,'20-24'
                  ,'25-34'
                  ,'35-44'
                  ,'45-54'
                  ,'55-64'
                  ,'65-74'
                  ,'75-84'
                  ,'85'
                  ,'NS'
                  ]
age_groups      = ['< 1 year'
                   ,'1 - 4 years'
                   ,'5 - 9 years'
                   ,'10 - 14 years'
                   ,'15 - 19 years'
                   ,'20 - 24 years'
                   ,'25 - 34 years'
                   ,'35 - 44 years'
                   ,'45 - 54 years'
                   ,'55 - 64 years'
                   ,'65 - 74 years'
                   ,'75 - 84 years'
                   ,'85+ years'
                   ,'Not Stated'
               ]
causes          = df['Cause of Death'].unique().tolist()
causes_codes    = df['Cause of Death Code'].unique().tolist()

default         = [years
                  ,states
                  ,counties
                  ,age_group_codes
                  ,causes_codes]



# Dictionaries that allow me to replace the compact codes with their values
cause_code_dict  = dict(df[['Cause of Death Code', 'Cause of Death']].values.tolist())
county_code_dict = dict(df[['County Code', 'County']].values.tolist())
county_dict      = dict(df[['County', 'County Code']].values.tolist())
age_code_dict    = dict(zip(age_group_codes, age_groups))


# --------------- Giant lists of Death Codes -------------------- #

# --------------- Medical --------------- #


# ---------- Cancer ---------- #
Oral_Cancer       = ['C02.9'
                    ,'C06.9'
                    ,'C07'
                    ,'C09.9'
                    ,'C11.9'
                    ,'C14.0'
                    ,'C15.9'
                    ]

GI_Cancer         = ['C16.9'
                    ,'C17.0'
                    ,'C18.2'
                    ,'C18.7'
                    ,'C18.9'
                    ,'C19'
                    ,'C20'
                    ,'C22.0'
                    ,'C22.1'
                    ,'C22.9'
                    ,'C23'
                    ,'C24.0'
                    ,'C24.9'
                    ,'C25.9'
                    ,'C26.0'
                    ,'C26.9'
                    ]

Pulmonary_Cancer  = ['C32.9'
                    ,'C34.1'
                    ,'C34.3'
                    ,'C34.9'
                    ]

Renal_Cancer      = ['C64'
                    ,'C67.9'
                    ,'C76.2'
                    ,'C78.6'
                    ,'C78.7'
                    ,'C79.8'
                    ]

Skeletal_Cancer   = ['C41.9']

Skin_Cancer       = ['C43.5'
                    ,'C43.7'
                    ,'C43.9'
                    ,'C44.4'
                    ,'C44.9'
                    ,'C45.9'
                    ,'C48.2'
                    ,'C76.0'
                    ,'C76.2'
                    ]

Brain_Cancer      = ['C71.9'
                    ,'D43.2'
                    ]

Thyroid_Cancer    = ['C73']


Lymphatic_Cancer  = ['C81.9'
                    ,'C83.1'
                    ,'C83.3'
                    ,'C85.1'
                    ,'C85.9'
                    ]

Blood_Cancer      = ['C90.0'
                    ,'C91.0'
                    ,'C91.1'
                    ,'C92.0'
                    ,'C92.1'
                    ,'C95.0'
                    ,'C95.9'
                    ,'D46.9'
                    ,'D47.1'
                    ]

Female_Cancer     = ['C50.9'
                    ,'C51.9'
                    ,'C53.9'
                    ,'C54.1'
                    ,'C55'
                    ,'C56'
                    ]

Male_Cancer       = ['C61']

Misc_Cancer       = ['C80'
                    ,'C97'
                    ]
# ---------- Cancer ---------- #


# -------- Heart -------- #
Valve        = ['I05.0'
               ,'I05.9'
               ,'I34.0'
               ,'I35.0'
               ,'I35.9'
               ,'I38'
               ]

Hypertension = ['I10'
               ,'I11.0'
               ,'I11.9'
               ,'I12.0'
               ,'I13.1'
               ,'I13.2'
               ,'I27.0'
               ,'I27.2'
               ]

MI          = ['I20.9'
              ,'I21.4'
              ,'I21.9'
              ,'I24.9'
              ,'I25.0'
              ,'I25.1'
              ,'I25.5'
              ,'I25.8'
              ,'I25.9'
              ,'I26.9'
              ,'I27.9'
              ,'I33.0'
              ,'I42.0'
              ,'I42.2'
              ,'I42.9'
              ,'I46.9'
              ]

MI_Specific = ['I48'
              ,'I49.9'
              ,'I50.0'
              ,'I50.9'
              ,'I51.6'
              ,'I51.7'
              ,'I51.9'
              ]

Haemorrhage = ['I60.7'
              ,'I60.9'
              ,'I61.5'
              ,'I61.9'
              ,'I62.0'
              ,'I62.9'
              ]

Circulatory = ['I70.0'
              ,'I70.9'
              ,'I71.0'
              ,'I71.1'
              ,'I71.2'
              ,'I71.3'
              ,'I71.4'
              ,'I71.8'
              ,'I71.9'
              ,'I73.9'
              ,'I80.2'
              ,'I99'
              ]
# -------- Heart -------- #


# ----- Brain ----- #
Stroke = ['I63.3'
         ,'I63.4'
         ,'I63.5'
         ,'I63.9'
         ,'I64'
         ,'I67.2'
         ,'I67.8'
         ,'I67.9'
         ,'I69.3'
         ,'I69.4'
         ,'I69.8'
         ]
# ----- Brain ----- #


# ---- Infections ---- #
Flu        = ['J10.0'
             ,'J10.1'
             ,'J11.0'
             ]

Pneumonia  = ['J12.9'
             ,'J15.2'
             ,'J15.9'
             ,'J18.0'
             ,'J18.1'
             ,'J18.9'
             ]

Bronchitis = ['J40'
             ,'J42'
             ,'J47'
             ]
# ---- Infections ---- #


# -------- Disease -------- #
Gastro          = ['A04.7'
                  ,'A09.0'
                  ,'A09.9'
                  ,'A16.2'
                  ,'A41.9'
                  ]

Hepatitis       = ['B16.9'
                  ,'B17.1'
                  ,'B18.2'
                  ,'B94.2']

HIV             = ['B20.1'
                  ,'B20.3'
                  ,'B20.6'
                  ,'B20.7'
                  ,'B20.8'
                  ,'B21.2'
                  ,'B22.2'
                  ,'B21.2'
                  ,'B22.2'
                  ,'B23.8'
                  ,'B24'
                  ]

Motor_Disease   = ['G12.2'
                  ,'G20'
                  ,'G23.1'
                  ]

Immune_Disease  = ['G35'
                  ,'G40.9'
                  ,'G70.0'
                  ,'G80.9'
                  ,'M32.1'
                  ,
                  ]

Blood_And_Fluid = ['D64.9'
                  ,'E78.0'
                  ,'E78.5'
                  ,'E86'
                  ]

Diabetes        = ['E10.2'
                  ,'E10.9'
                  ,'E11.2'
                  ,'E11.5'
                  ,'E11.7'
                  ,'E11.9'
                  ,'E14.0'
                  ,'E14.1'
                  ,'E14.2'
                  ,'E14.5'
                  ,'E14.7'
                  ,'E14.9'
                  ]

Obesity         = ['E66.8'
                  ,'E66.9'
                  ]

Protein         = ['E43'
                  ,'E46'
                  ]

Thyroid         = ['E03.9']

COPD            = ['J43.9'
                  ,'J44.0'
                  ,'J44.1'
                  ,'J44.8'
                  ,'J44.9'
                  ,'J45.9'
                  ]

Pulmonary       = ['J69.0'
                  ,'J84.1'
                  ,'J84.9'
                  ,'J98.4'
                  ]
# -------- Disease -------- #


# --------- GI --------- #
GI          = ['K25.4'
              ,'K26.4'
              ,'K26.5'
              ,'K27.4'
              ,'K52.9'
              ,'K55.0'
              ,'K55.9'
              ,'K56.6'
              ,'K57.8'
              ,'K57.9'
              ,'K63.1'
              ,'K92.2'
              ]

Hepatic     = ['K76.0'
              ,'K76.9'
              ]

Gallbladder = ['K80.2'
              ,'K81.0'
              ,'K81.9'
              ,'K83.0'
              ]

Pancreas    = ['K85'
              ,'K85.9'
              ]

Renal       = ['N03.9'
              ,'N12'
              ,'N17.9'
              ,'N18.0'
              ,'N18.4'
              ,'N18.5'
              ,'N18.9'
              ,'N19'
              ,'N39.0'
              ]
# --------- GI --------- #


# ---- Joints ---- #
Joints = ['M06.9'
         ,'M19.9'
         ]

Osteo  = ['M80.9'
         ,'M81.9'
         ,'M86.9'
         ]

Skin   = ['M34.8']
# ---- Joints ---- #


# ---------- Age ---------- #
Prebirth        = ['Q00.0'
                  ,'Q04.2'
                  ,'Q23.4'
                  ,'Q24.9'
                  ,'Q33.6'
                  ,'Q79.0'
                  ,'Q89.7'
                  ,'Q90.9'
                  ,'Q91.3'
                  ,'Q91.7'
                  ]

Neonate_Disease = ['P01.0'
                  ,'P01.1'
                  ,'P01.5'
                  ,'P02.1'
                  ,'P02.7'
                  ,'P07.2'
                  ,'P07.3'
                  ,'P21.9'
                  ,'P22.0'
                  ,'P27.1'
                  ,'P28.0'
                  ,'P29.0'
                  ,'P29.1'
                  ,'P36.9'
                  ,'P52.3'
                  ,'P77'
                  ,'R95'
                  ,'R99'
                  ]

Seniority       = ['G30.1'
                  ,'G30.9'
                  ,'G31.1'
                  ,'G31.8'
                  ,'G31.9'
                  ,'R54'
                  ,'R62.8'
                  ,'R63.6'
                  ,'R63.8'
                  ]

Dementia        = ['F01.1'
                  ,'F01.9'
                  ,'F03'
                  ]


# Mental
Mental_Disorder = ['F06.9'
                  ,'F10.0'
                  ,'F10.1'
                  ,'F10.2'
                  ,'F11.9'
                  ,'F14.9'
                  ,'F15.1'
                  ,'F19.1'
                  ,'F19.9'
                  ,'F50.8'
                  ,'F79'
                  ]

Cerebral        = ['G80.9'
                  ,'G93.4'
                  ,'G93.9'
                  ]
# ---------- Age ---------- #


# -- Gender Specific -- #
Mens_Disease = ['N40']

Child_birth  = ['O96']
# -- Gender Specific -- #


# Self-Inflicted Disease
Alcoholism = ['K70.0'
             ,'K70.1'
             ,'K70.3'
             ,'K70.4'
             ,'K70.9'
             ,'K74.6'
             ]
# Self-Inflicted Disease


# --------------- Medical --------------- #

# --------------- Trauma --------------- #

# Motor-Vehicle Collision
Pedestrian = ['V03.1'
             ,'V09.2'
             ,'V87.7'
             ,'V89.2'
             ]

Motorcycle = ['V23.4'
             ,'V27.4'
             ]

Car        = ['V43.5'
             ,'V43.6'
             ,'V47.5'
             ,'V47.6'
             ,'V48.5'
             ,'Y85.0'
             ]

# Misc.
Fall = ['W01'
       ,'W06'
       ,'W10'
       ,'W18'
       ]


# Firearms
Firarms            = ['W34']

Airway_Obstruction = ['W67'
                     ,'W79'
                     ]

Imolation          = ['X00']

Poisoning          = ['X41'
                     ,'X42'
                     ,'X44'
                     ,'X45'
                     ,'X59'
                     ,'X59.9'
                     ]


# Suicide
Self_Harm        = ['X64'
                   ,'X67'
                   ,'X70'
                   ,'X80'
                   ]



Self_Firearm     = ['X72'
                   ,'X73'
                   ,'X74'
                   ]


# Homicide

Homicide_Firearm = ['X93'
                   ,'X94'
                   ,'X95'
                   ,'Y35.0'
                   ]

Homicide_Object  = ['X99'
                   ,'Y09'
                   ]

# Accidental
Misc             = ['Y14']

# --------------- Trauma --------------- #

# --------------- Giant lists of Death Codes -------------------- #


# This prevents errors in the other functions for not passing a list
# Just makes it simpler for me
def error_prev(some_list):

    # Converts any none lists into lists for use
    # Also ignores ranges which function identically for my purposes
    iterator = -1
    for choice in some_list:
        iterator += 1

        if type(choice) != list and type(choice) != range:
            some_list[iterator] = [some_list[iterator]]


    # If there's blank values, replaces them with the default
    iterator = -1
    for choice in some_list:
        iterator += 1

        if choice[0] == '':
            some_list[iterator] = default[iterator]


    return some_list



# This function is specifically for making a graph that projects data across
# the years
def df_graphing(choices):

    choices            = error_prev(choices)
    death_sums_by_year = []

    # For each year we sum the deaths and put them to a list. This prevents the
    # graph from having dozens of lines that zig-zag everywhere
    for year in choices[0]:
        choice  = [year
                  ,choices[1]
                  ,choices[2]
                  ,choices[3]
                  ,choices[4]
                  ]
        death_sums_by_year.append(df_filter(choice)['Deaths'].sum())

    plotting_df = np.array([choices[0],     death_sums_by_year]).T
    plotting_df = pd.DataFrame(plotting_df, columns = ['Year', 'Deaths'])

    return plotting_df



# This is for telling the pct values in the donut chart how to present
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d} ({p:.2f}%)'.format(p = pct
                                         ,v = val)
    return my_autopct



def df_filter(choices):

    choices = error_prev(choices)

    # Any choices must be put in lists, else .isin() can't function
    filterer = [['Year',                choices[0]]
               ,['State Code',          choices[1]]
               ,['County Code',         choices[2]]
               ,['Age Group Code',      choices[3]]
               ,['Cause of Death Code', choices[4]]
               ]

    # From right to left
    # This checks our specified filters against what's in the dataframe, then
    # for each part of the filter, top to bottom, it weeds out the False values.
    # Any value which includes a list of all possible values will pass through
    # that entire chunk of the dataframe.

    # Can't think of a less chunky version of this. It needs to save over prior
    # data to make the dataframe correctly.
    filtered_df = df
    filtered_df = filtered_df[filtered_df[filterer[0][0]].isin(filterer[0][1])]
    filtered_df = filtered_df[filtered_df[filterer[1][0]].isin(filterer[1][1])]
    filtered_df = filtered_df[filtered_df[filterer[2][0]].isin(filterer[2][1])]
    filtered_df = filtered_df[filtered_df[filterer[3][0]].isin(filterer[3][1])]
    filtered_df = filtered_df[filtered_df[filterer[4][0]].isin(filterer[4][1])]

    return filtered_df



# ----------------------------------- Work ----------------------------------- #



# ---------------------------------- Output ---------------------------------- #

# ----- Graph of Age Group Summed Deaths ----- #
# For each year, add up the deaths by Age Group Code

choice      = [''
              ,6
              ,6073
              ,['1'
               ,'1-4'
               ,'5-9'
               ,'10-14'
               ,'15-19'
               ,'15-19'
               ,'20-24']
              ,''
              ]

choice = error_prev(choice)

fig, ax     = plt.subplots()
target      = 'Deaths'
features    = 'Year'

# Let's say I want to look at a bunch of graphs filtered by age group

for layer in choice[3]:

    choice[3]     = layer
    plotting_df   = df_graphing(choice)
    ax.plot(plotting_df[features]
           ,plotting_df[target]
           ,label = age_code_dict[layer])




plt.xticks(rotation = 45)
plt.xlim(choice[0][0]
        ,choice[0][-1])
plt.ylim(-0.5)
# Limited the y-axis to prevent the data from being all over the place


plt.title(str(county_code_dict[choice[2][0]])
    ,fontsize = 12
    )

ax.legend(bbox_to_anchor = (1, 1))


plt.show()
# ----- Graph of Age Group Summed Deaths ----- #


# ----- Graph of All Types of Deaths ----- #
# For each year, add up the deaths by Cause of Death Code

lists       = [Homicide_Firearm, Self_Firearm]
chosen_list = []

for listy in lists:
    for thing in listy:
        chosen_list.append(thing)


choice      = [''
              ,6
              ,6073
              ,''
              ,chosen_list
              ]


choice = error_prev(choice)

fig, ax     = plt.subplots()
target      = 'Deaths'
features    = 'Year'


for layer in choice[4]:

    choice[4]     = layer
    plotting_df   = df_graphing(choice)
    ax.plot(plotting_df[features]
           ,plotting_df[target]
           ,label = cause_code_dict[layer])


plt.xticks(rotation = 45)
plt.xlim(choice[0][0]
        ,choice[0][-1])
plt.ylim(-0.5)
# Limited the y-axis to prevent the data from being all over the place


plt.title(str(county_code_dict[choice[2][0]])
    ,fontsize = 12
    )

ax.legend(bbox_to_anchor = (1, 1))


plt.show()
# ----- Graph of All Types of Deaths ----- #


# ---------- Donut Plot ---------- #
# ---------- Donut Plot ---------- #

choice      = [2016
              ,6
              ,6073
              ,'20-24'
              ,''
              ]

choice = error_prev(choice)

# ----- Pre-work ----- #
filtered_df = df_filter(choice)

# Total dead of a given age group vs total population of a given age group
# This gives us the total left living, for a given age group
total_pop = filtered_df['Population'].iloc[0]
alive     = filtered_df['Population'].iloc[0] - filtered_df['Deaths'].sum()
dead      = filtered_df['Deaths'].sum()


# This is the outer ring of the donut chart showing the living vs the dead for
# a given subset of the dataframe
group_names    = ['Alive', 'Deceased']
group_size     = [alive, dead]


# This is the inner ring showing the 4 most common causes with a misc 5th cause
# that includes all the others that were missed. Then it makes the list of the
# 5 groups going into the donut chart
subgroup_names = filtered_df.sort_values(by = ['Deaths'], ascending = False)[:5]
subgroup_size  = filtered_df.sort_values(by = ['Deaths'], ascending = False)[:5]

subgroup_names = subgroup_names['Cause of Death Code'].tolist()
subgroup_size  = subgroup_size['Deaths'].tolist()



# Very messy complicated thing that literally only adds in a consolidated misc
# category if we go over the top 5 causes of death
if len(filtered_df['Deaths'].sort_values(ascending = False)[5:]) != 0:
    subgroup_names.append(str(len(filtered_df['Deaths'].sort_values(ascending = False)[5:])) + ' others\ncombined')
    subgroup_size.append(filtered_df['Deaths'].sort_values(ascending = False)[5:].sum())


# ----- Pre-work ----- #



# ----- Donut Cooking ----- #

# Create colors
a, d = [plt.cm.Greens, plt.cm.Reds]

fig, ax = plt.subplots()
ax.axis('equal')
mpl.rcParams['font.size'] = 9.0


# First Ring (Outside)
ring, text, perc    = ax.pie(group_size
                            ,radius        = 1.5
                            ,startangle    = 320
                            ,labels        = group_names
                            ,labeldistance = 1.1
                            ,autopct       = make_autopct(group_size)
                            ,pctdistance   = 0.87
                            ,colors        = [a(0.6)
                                             ,d(0.6)
                                             ]
                            )
# Sets the text size for the different groups and their percentages
text[0].set_fontsize(18)
text[1].set_fontsize(18)

perc[0].set_fontsize(12)
perc[1].set_fontsize(12)
perc[0].set_fontweight('bold')
perc[1].set_fontweight('bold')

plt.setp(ring
        ,width = 0.4
        ,edgecolor = 'white')


# Second Ring (Inside)
ring2, text2, perc2 = ax.pie(subgroup_size
                            ,radius        = 1.5 - 0.4
                            ,labels        = subgroup_names
                            ,rotatelabels  = True
                            ,counterclock  = False
                            ,labeldistance = 0.8
                            ,autopct       = make_autopct(subgroup_size)
                            ,pctdistance   = 0.45
                            ,colors        = [d(0.9)
                                             ,d(0.8)
                                             ,d(0.7)
                                             ,d(0.6)
                                             ,d(0.5)
                                             ,d(0.4)
                                             ]
                            )

# perc2[0].set_fontweight('bold')
# perc2[1].set_fontweight('bold')

plt.setp(ring2
        ,width = 0.4
        ,edgecolor = 'white'
        )

plt.setp(text2
        ,rotation_mode = 'anchor'
        ,ha            = 'center'
        ,va            = 'center')


# An additional step that rotates the inner text to go around the ring for
# better legibility
for txt in text2:
    rotation = txt.get_rotation()
    txt.set_rotation(rotation + 90 + (1 - rotation // 180) * 180)

for number in range(0, len(subgroup_size), 1):
    text2[number].set_fontsize(13)
    perc2[number].set_fontsize(10)


# Printing the title
if len(choice[0]) == 1:
    plt.title(str(county_code_dict[choice[2][0]]) +
              ' ' +
              str(choice[0][0]) +
              '\n' +
              'Ages ' +
              choice[3][0] +
              ' years'
              ,fontsize = 18
              ,y = 1.12)
else:
    plt.title(str(county_code_dict[choice[2][0]]) +
              ' ' +
              str(choice[0][0]) +
              ' - ' +
              str(choice[0][-1]) +
              '\n' +
              'Ages ' +
              choice[3][0] +
              ' years'
              ,fontsize = 18
              ,y = 1.12)


# Printing the legend
legend_list = []

for thing in subgroup_names:
    if re.match('[0-9]+ others\ncombined', thing):
        continue
    legend_list.append(fill(str(thing) + ': ' + str(cause_code_dict[thing])
                           ,width = 50))

plt.legend(ring2
          ,legend_list
          ,bbox_to_anchor = (0.9, 1))


plt.show()
# ----- Donut Cooking ----- #

# ---------- Donut Plot ---------- #


# ---------- Seaborn Plot ---------- #
choice      =          [''
                       ,6
                       ,''
                       ,''
                       ,''
                       ]

filtered_df = df_filter(choice)

target   = filtered_df['Deaths']
features = filtered_df.columns.drop(['Deaths'
                                    ,'Year'
                                    ,'Cause of Death'
                                    ,'State'
                                    ,'State Code'
                                    ,'County Code'
                                    ,'Age Group'
                                    ,'Age Group Code'
                                    ,'Population'
                                    ,'Cause of Death Code'
                                    ,'Crude Rate'
                                    ,'Crude Rate Standard Error'])

plt.figure(figsize = (20, 10))
for feature in features:
    plt.scatter(x = feature
               ,y = target
               ,data = filtered_df
               ,alpha = 0.1)
plt.xticks(rotation = 90)
plt.xlim(-1, 53)
plt.ylim(0, 3500)

plt.title('California, all years')


plt.show()
# ---------- Seaborn Plot ---------- #


# ---------- California County Map Plot ---------- #
# world = geo.read_file(geo.datasets.get_path('naturalearth_lowres'))
# cities = geo.read_file(geo.datasets.get_path('naturalearth_cities'))
# world.head()
# world.plot();
#
# world = world[(world.pop_est>0) & (world.name!="Antarctica")]
#
# world['gdp_per_cap'] = world.gdp_md_est / world.pop_est
#
# world.plot(column='gdp_per_cap');
# ---------- California County Map Plot ---------- #

# ---------------------------------- Output ---------------------------------- #

# ---------------------------------- Output ---------------------------------- #
