from datetime import date
import pandas as pd
import numpy as np
import csv
import sys

from pybaseball import plot_stadium
from pybaseball import spraychart
from pybaseball import statcast
from pybaseball import playerid_lookup
from pybaseball import statcast_pitcher
from pybaseball import statcast_batter

import matplotlib.pyplot as plt

def plot_hits(firstname, lastname):
    today = date.today().strftime("%Y-%m-%d")
    players = pd.read_csv("PlayerIDMap.csv")
    try:
        player_id = playerid_lookup(lastname, firstname)['key_mlbam'][0]
    except:
        print('Sorry! That player doesn\'t exist. Try again')
        exit()
    player_team = players[players['MLBID']==player_id].iloc[0]['TEAM']

    with open('team_lookup.csv') as f:
        next(f) 
        reader = csv.reader(f, skipinitialspace=True) # convert CSV to dict
        team_dict = dict(reader)

    player_team_name = '_'.join(team_dict[player_team].split()).lower()
    data = statcast_batter('2021-03-01', today, player_id)
    print(data.head())

    #regular season in playb alls at home
    data_filt = data[(data.game_type =='R') & (data.events.isin(['single','double','triple','home_run'])) & (data.home_team==player_team)] 


    spraychart(data_filt, player_team_name, title='', 
            tooltips=[], size=100, colorby='events', 
            legend_title='', width=900, height=900)
    plt.show()

if __name__ == '__main__':
    firstname = input("Please enter player first name: ")
    print("You entered: " + firstname )
    lastname = input("Please enter player last name: ")
    print("You entered: " + lastname)
    plot_hits(firstname, lastname)
