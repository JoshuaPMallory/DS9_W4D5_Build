import os
import numpy as np
import pandas as pd
import matplotlib as mpl
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

print(df.head())
print(df.dtypes)
# ------------------------------ Data Cleaning ------------------------------ #



# ----------------------------------- Work ----------------------------------- #
# I need a way to filter based on arbitrary stats, e.g. County, Age Group, etc.

# The default values for ALL RESULTS
years      = range(1999, 2017, 1)
states     = range(1, 51, 1)
counties   = range(6001, 6116, 1)
age_groups = ['< 1 year'
             ,'1-4 years'
             ,'5-9 years'
             ,'10-14 years'
             ,'15-19 years'
             ,'20-24 years'
             ,'25-34 years'
             ,'35-44 years'
             ,'45-54 years'
             ,'55-64 years'
             ,'65-74 years'
             ,'75-84 years'
             ,'85+ years'
             ,'Not Stated'
             ]
cause      = df['Cause of death Code'].unique()

# Default
filter = [['Year',           years]
         ,['State Code',     states]
         ,['County Code',    counties]
         ,['Age Group',      age_groups]
         ,['Cause of death', cause]
         ]

def df_filter(year, state, county, age_group, cause):
    # Any choices must be put in lists, else .isin() can't function
    filter = [['Year',                year]
             ,['State Code',          state]
             ,['County Code',         county]
             ,['Age Group',           age_group]
             ,['Cause of death Code', cause]
             ]

    # From right to left
    # This checks our specified filters against what's in the dataframe, then
    # for each part of the filter, top to bottom, it weeds out the False values.
    # Any value which includes a list of all possible values will pass through
    # that entire chunk of the dataframe.

    # Can't think of a less chunky version of this. It needs to save over prior
    # data to make the dataframe correctly.
    filtering   = df
    filtering   = filtering[filtering[filter[0][0]].isin(filter[0][1])]
    filtering   = filtering[filtering[filter[1][0]].isin(filter[1][1])]
    filtering   = filtering[filtering[filter[2][0]].isin(filter[2][1])]
    filtering   = filtering[filtering[filter[3][0]].isin(filter[3][1])]
    filtered_df = filtering[filtering[filter[4][0]].isin(filter[4][1])]

    return filtered_df


# I need a way of summing the number of deaths per type of death,
# or within any other category

#  [ ]
#  [ ]

# ----------------------------------- Work ----------------------------------- #



# ---------------------------------- Output ---------------------------------- #

mpl.rcParams['font.size'] = 9.0

# ---------- Graph ---------- #
# plt.scatter(filtered_df['Age Group'], filtered_df['Deaths'])
# plt.xticks(rotation = 45)


# plt.show()
# ---------- Graph ---------- #


# ---------- Donut Plot ---------- #

# We're going to set the title for this to be whichever county it is
# Then we'll make it show the total population for the circle
# Then divide the circle into two parts; alive and dead

# All of this will be pre-sorted by year, state, etc.

# I'd like to use the dataframe filter within this.

choice = [[1999]
         ,[6]
         ,[6073]
         ,['< 1 year']
         ,cause
         ]

filtered_df = df_filter(choice[0]
                       ,choice[1]
                       ,choice[2]
                       ,choice[3]
                       ,choice[4]
                       )


total_pop = filtered_df['Population'].iloc[0]
alive     = filtered_df['Population'].iloc[0] - filtered_df['Deaths'].sum()
dead      = filtered_df['Deaths'].sum()


# This is the outer ring of the donut chart showing the living vs the dead for
# a given subset of the dataframe
group_names    = ['Alive', 'Dead']
group_size     = [alive, dead]


# This is the inner ring showing the most common causes
# Need to make it so that only the top 4 are listed with a misc. 5th slot
subgroup_names = filtered_df['Cause of death'].unique().tolist()
subgroup_size  = filtered_df['Deaths'].unique().tolist()


# Create colors
a, b = [plt.cm.Greens, plt.cm.Reds]


# First Ring (outside)
fig, ax = plt.subplots()

ax.axis('equal')


pie, text = ax.pie(group_size
                  ,radius = 1.3
                  ,labels = group_names
                  ,colors = [a(0.6)
                            ,b(0.6)
                            ]
               )

text[0].set_fontsize(15)
text[1].set_fontsize(15)


plt.setp(pie
        ,width = 0.3
        ,edgecolor = 'white')


# Second Ring (Inside)
pie2, text = ax.pie(subgroup_size
                   ,radius        = 1.3 - 0.3
                   ,labels        = subgroup_names
                   ,labeldistance = 1
                   ,colors        = [b(0.5)
                                    ,b(0.4)
                                    ,b(0.1)
                                    ,b(0.9)
                                    ]
                )
text[0].set_fontsize(12)
text[1].set_fontsize(12)
text[2].set_fontsize(12)
text[3].set_fontsize(12)

plt.setp(pie2
        ,width = 0.4
        ,edgecolor = 'white'
        )

plt.margins(0, 0)
plt.title('San Diego ' + str(choice[0][0]) + '\n' + 'Ages ' + choice[3][0]
         ,fontsize = 18)

plt.show()

# ---------- Donut Plot ---------- #


# ---------- California County Map Plot ---------- #

# ---------- California County Map Plot ---------- #


# ---------------------------------- Output ---------------------------------- #
