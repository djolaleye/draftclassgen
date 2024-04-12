#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 17:30:51 2022

@author: deji
"""

import math
import random
import numpy as np
import pandas as pd

pd.options.display.max_columns = None
pd.options.display.max_rows = None


def generateDC():
    d_class_info = pd.DataFrame()
    d_class_players = pd.DataFrame()
    college_info = college_rankings()
    
    d_class_info['depth_rating'], d_class_info['strength_rating'] = depth_strength()
    d_class_strength = (((d_class_info['depth_rating'].mean()) + (2*(d_class_info['strength_rating'].mean()))))/3
    d_class_info['dc_strength'] = d_class_strength
    d_class_info['position'] = ('QB', 'RB', 'WR', 'TE','OT', 'IOL', 'IDL', 'EDGE', 'LB', 'CB', 'SAF')
    
    d_class_players['pos'] = randomize_pos()
    d_class_players['college'] = randomize_college()
    d_class_players['first_name'], d_class_players['last_name'], d_class_players['age']  = randomize_names()
    
    
    d_class_players['tags'] = generate_tags(d_class_players['pos'])
    
    d_class_players['player_rating'] = player_rating(college_info, d_class_info, d_class_players)
    d_class_players.index += 1
    return d_class_info, d_class_players

def generate_tags(pos_list):
    
    player_tags = []   
    for i in pos_list:
        get_tag = random.randint(0,100)
        if get_tag <= 70:
            player_tags.append('none')
            continue
        tags = {'QB': 18*['high-volume'] + 33*['turnover-prone'] + 33*['dual-threat'] + 15*['injury-risk'],
                 'RB' : 20*['high-volume'] + 15*['turnover-prone'] + 50*['dual-threat'] + 15*['injury-risk'], 
                 'WR' : 42*['high-volume'] + 43*['dual-threat'] + 15*['injury-risk'],
                 'TE' : 35*['high-volume'] + 50*['none'] + 15*['injury-risk'], 
                 'OT' : 85*['none'] + 15*['injury-risk'], 'IOL' : 85*['none'] + 15*['injury-risk'],
                 'IDL': 20*['rush-specialist'] + 50*['run-stuffer'] + 15*['high-motor'] + 15*['injury-risk'],
                 'EDGE': 50*['rush-specialist'] + 20*['run-stuffer'] + 15*['high-motor'] + 15*['injury-risk'],
                 'LB' : 33*['coverage'] + 20*['hammer'] + 33*['sl-sl'] + 14*['injury-risk'],
                 'CB' : 42*['ballhawk'] + 41*['peanut'] + 2*['dual-threat'] + 15*['injury-risk'],
                 'SAF' : 20*['ballhawk'] + 20*['peanut'] + 20*['hammer'] + 25*['sl-sl'] + 15*['injury-risk']}
        
        tag = random.choice(tags[i])
        player_tags.append(tag)
    
    return player_tags


   
'''

ITEM 1: POSITIONS

'''

def randomize_pos():
    pos_counter = {'QB': 0,'RB' : 0, 'WR' : 0, 'TE' : 0, 'OT' :  0, 'IOL' : 0,
                   'IDL': 0, 'EDGE' : 0, 'LB' : 0, 'CB' : 0, 'SAF' : 0}
    
    pos_max = {'QB': 13,'RB' : 24, 'WR' : 36, 'TE' : 17, 'OT' :  28, 'IOL' : 22,
                   'IDL': 24, 'EDGE' : 33, 'LB' : 33, 'CB' : 37, 'SAF' : 22}
    
    off_counter, def_counter = 0,0
    max_off, max_def = 142, 149
    
    player_position = {'OFF':['QB', 'RB', 'WR','TE', 'OT', 'IOL'], 'DEF':['IDL', 'EDGE', 'LB', 'CB', 'SAF']}
    pos_list = []
    
    for i in range(0,262):
        random_key = random.sample(player_position.keys(), 1)[0]
        if random_key == 'OFF':
            off_counter += 1
        elif random_key == 'DEF':
            def_counter += 1
            
        if off_counter > max_off:
            off_counter -=1
            random_key == 'DEF'
        elif def_counter > max_def:
            def_counter -=1
            random_key == 'OFF'
            
        val = random.choice(player_position[random_key])
        while pos_counter[val] >= pos_max[val]:
            player_position[random_key].remove(val)
            val = random.choice(player_position[random_key])
        
        pos_counter[val] += 1
        pos_list.append(val)
        
    return pos_list
    
def depth_strength():
    pos_strength = {'QB': 0,'RB' : 0, 'WR' : 0, 'TE' : 0, 'OT' :  0, 'IOL' : 0,
                   'IDL': 0, 'EDGE' : 0, 'LB' : 0, 'CB' : 0, 'SAF' : 0}
    pos_depth = {'QB': 0,'RB' : 0, 'WR' : 0, 'TE' : 0, 'OT' :  0, 'IOL' : 0,
                   'IDL': 0, 'EDGE' : 0, 'LB' : 0, 'CB' : 0, 'SAF' : 0}
    
    depth = []
    strength = []
    for i in pos_strength:
        pos_strength[i] = random.randrange(0,50,5)/10
        strength.append(pos_strength[i])
        pos_depth[i] = random.randrange(0,55,5)/10
        depth.append(pos_depth[i])
    
    return depth, strength


'''

ITEM 2: COLLEGES

'''
all_colleges = pd.read_csv('all_colleges.csv')
fbs = pd.read_csv('fbs.csv') 
fcs = pd.read_csv('fcs.csv')
naia = pd.read_csv('naia.csv')  
d3 = pd.read_csv('d3.csv') 
d2 = pd.read_csv('d2.csv')



def randomize_college():
    '''
    .9 = fbs      conference: sec 0.25, b10 0.18, acc .18, pac .11, b12 .11, aac .07, ind .06, mw/cusa /mac/sun belt = .01
    .065 = fcs
    .025 = d2
    .005 = d3
    .005 = naia
    
    
    '''
    col_list = []
    y = ['SEC']*25 + ['Big Ten']*18 + ['ACC']*18 + ['Pac-12']*11 +['Big 12']*11 + ['American']*7 +['Independent']*6 + ['Mountain West'] + ['C-USA'] + ['MAC'] +['Sun Belt']
    for i in range(0,262):
        x = random.randint(1,1000)
        if x <= 890:
            chosen_conf = random.choice(y)
            col_selected = random.choice(list(fbs.loc[fbs['Conference'] == chosen_conf, 'Team']))
            col_list.append(col_selected)
        elif 890 < x <= 955:
            col_selected = random.choice(fcs['Team'])
            col_list.append(col_selected)
        elif 955 < x <= 970:
            col_selected = random.choice(d2['Team'])
            col_list.append(col_selected)
        elif 970 < x <= 975:
            col_selected = random.choice(d3['Team'])
            col_list.append(col_selected)
        else:
            col_selected = random.choice(naia['Team'])
            col_list.append(col_selected)
    return col_list

def college_rankings():
    '''
    
     name, ranking, W/L, strength of schedule
    
    '''
    college_strength = all_colleges
    
    conf_sec = fbs.loc[fbs['Conference'] == 'SEC', 'Team'].tolist()
    conf_b10 = fbs.loc[fbs['Conference'] == 'Big Ten', 'Team'].tolist()
    conf_b12 = fbs.loc[fbs['Conference'] == 'Big 12', 'Team'].tolist()
    conf_acc = fbs.loc[fbs['Conference'] == 'ACC', 'Team'].tolist()
    conf_pac = fbs.loc[fbs['Conference'] == 'Pac-12', 'Team'].tolist()
    conf_sb = fbs.loc[fbs['Conference'] == 'Sun Belt', 'Team'].tolist()
    conf_mac = fbs.loc[fbs['Conference'] == 'MAC', 'Team'].tolist()
    conf_mw = fbs.loc[fbs['Conference'] == 'Mountain West', 'Team'].tolist()
    conf_i = fbs.loc[fbs['Conference'] == 'Independent', 'Team'].tolist()
    conf_amer = fbs.loc[fbs['Conference'] == 'American', 'Team'].tolist()
    conf_usa = fbs.loc[fbs['Conference'] == 'C-USA', 'Team'].tolist()
    
    group_5 = conf_amer + conf_mac + conf_mw + conf_sb + conf_usa
    
    fbs_strength = random.randint(60,90)
    sec_mod = random.randint(90,110)/100
    b10_mod = random.randint(90,110)/100
    b12_mod = random.randint(80,110)/100
    acc_mod = random.randint(75,110)/100
    pac_mod = random.randint(75,110)/100
    g5_mod = random.randint(70,105)/100
    ind_mod = random.randint(75,108)/100
    
    sec_str = round((sec_mod * fbs_strength), 1)
    b10_str = round((b10_mod * fbs_strength), 1)
    b12_str = round((b12_mod * fbs_strength), 1)
    acc_str = round((acc_mod * fbs_strength), 1)
    pac_str = round((pac_mod * fbs_strength), 1)
    g5_str = round((g5_mod * (.8 * fbs_strength)), 1)
    ind_str = round((ind_mod * (0.9 * fbs_strength)), 1)
    
    if sec_str > 100:
        sec_str = 100
    if b10_str > 100:
        b10_str = 100
    if acc_str > 100:
        acc_str = 100
    if b12_str > 100:
        b12_str = 100
    if pac_str > 100:
        pac_str = 100
    
    
    fcs_strength = random.randint(int(fbs_strength/4), int(0.75*fbs_strength))

    college_strength['strength'] = fcs_strength
    
    for team in college_strength['Team']:
        if team in conf_sec:
             college_strength.loc[college_strength.Team == team, 'strength'] = random.uniform(0.67 * sec_str, 1.25 * sec_str)
        elif team in conf_b10:
            college_strength.loc[college_strength.Team == team, 'strength'] = random.uniform(0.67 * b10_str, 1.25 * b10_str)
        elif team in conf_b12:
            college_strength.loc[college_strength.Team == team, 'strength'] = random.uniform(0.67 * b12_str, 1.25 * b12_str)
        elif team in conf_pac:
            college_strength.loc[college_strength.Team == team, 'strength'] = random.uniform(0.67 * pac_str, 1.25 * pac_str)
        elif team in conf_acc: 
            college_strength.loc[college_strength.Team == team, 'strength'] = random.uniform(0.67 * acc_str,  1.25 * acc_str)
        elif team in group_5:
            college_strength.loc[college_strength.Team == team, 'strength'] = random.uniform(0.67 * g5_str, 1.25 * g5_str)
        elif team in conf_i:
            college_strength.loc[college_strength.Team == team, 'strength'] = random.uniform(0.67 * ind_str, 1.25 * ind_str)
        else:
            college_strength.loc[college_strength.Team == team, 'strength'] = random.uniform(0.5 * fcs_strength, 1.33 * fcs_strength)
         
    
    return college_strength



''' 

ITEM 3: NAMES

'''

first_names = pd.read_csv('firstNameList.csv')
last_names = pd.read_csv('lastNameList.csv')

def randomize_names():
    first = []
    last = []
    age = []
    age_list = [20, 21, 22, 23, 24, 25]
    races = ['B', 'W', 'PI','R']
    black_name_list = last_names.loc[((last_names['pctblack'] >= 40.00) & (last_names['prop100k'] >= 2.0)), 'name']
    white_name_list = last_names.loc[((last_names['pctwhite'] >= 40.00) & (last_names['prop100k'] >= 2.0)), 'name']
    api_name_list = last_names.loc[((last_names['pctapi'] >= 40.00) & (last_names['prop100k'] >= 2.0)), 'name']
    
    portion1 = first_names.loc[first_names['Frequency'] >= 100].sample(frac=0.33)
    portion2 = first_names.loc[first_names['Frequency'] >= 100].sample(frac=0.33)
    portion3 = first_names.loc[first_names['Frequency'] >= 20].sample(frac=0.33)
    
    for i in range(0,262):
        player_race = random.choices(races, weights=(65, 28, 1.6, 5.4))

        if player_race[0] == 'B':
            f_name = portion1['Name'].sample(n=1)
            first.append(f_name.iloc[0])
            l_name = black_name_list.sample(n=1)
            last.append(l_name.iloc[0])
        elif player_race[0] == 'W':
            f_name = portion2['Name'].sample(n=1)
            first.append(f_name.iloc[0])
            l_name = white_name_list.sample(n=1)
            last.append(l_name.iloc[0])
        elif player_race[0] == 'PI':
            f_name = portion3['Name'].sample(n=1)
            first.append(f_name.iloc[0])
            l_name = api_name_list.sample(n=1)
            last.append(l_name.iloc[0])
        else:
            f_name = first_names['Name'].sample(n=1)
            first.append(f_name.iloc[0])
            l_name = random.choice(last_names['name'])
            last.append(l_name)
            
        if i <= 100:
            p_age = random.choices(age_list, weights=(20, 30, 45, 20, 10, 1), k=1)
            age.append(p_age[0])
        else:
            p_age = random.choices(age_list, weights=(5, 15, 45, 30, 30, 5), k=1)
            age.append(p_age[0])
        
        
    return first, last, age




'''

ITEM 4: TAGS + RATING

'''

def player_rating(colleges_data, class_data, player_data):
    rating_list = []
    
    class_strength = class_data['dc_strength'][0]
    class_depth = class_data['depth_rating'].median()
    
    for row in range(0, player_data.shape[0]):
        position = player_data['pos'][row]
        pos_strength = class_data.loc[class_data['position'] == position, 'strength_rating'].values[0]
        pos_depth = class_data.loc[class_data['position'] == position, 'depth_rating'].values[0]
        player_college = player_data['college'][row]
        college_strength = colleges_data.loc[colleges_data['Team'] == player_college, 'strength'].values[0]
        if row <= 31:
            rating = np.quantile(colleges_data['strength'], 0.95)
        elif 31 < row <= 100:
            rating = np.quantile(colleges_data['strength'], 0.94)
        else:
            rating = np.quantile(colleges_data['strength'], 0.93)
        rating_bump = ((pos_strength * (1 + (pos_strength/3))) / (1 + (row/(1 + pos_depth)))) + (random.uniform(0, 0.15 * college_strength))    
        rating += rating_bump
        rating_list.append(rating)
    
    

    for i in range(0, len(rating_list)):
        multiplier = random.uniform(0.95, 1.05)
        if i <= 5:
            max_pot = rating_list[i] * (1 + (((2 * class_strength) + (class_depth))/75))
            min_pot = rating_list[i] * (0.95 + (((2 * class_strength) + (class_depth))/150))
            rating_list[i] = random.uniform((min_pot * multiplier), (max_pot * multiplier))
        elif i <= 10:
            max_pot = rating_list[i] * (1 + (((2 * class_strength) + (class_depth))/85))
            min_pot = rating_list[i] * (0.9 + (((2 * class_strength) + (class_depth))/150))
            rating_list[i] = random.uniform((min_pot * multiplier), (max_pot * multiplier))
        elif i <= 32:
            max_pot = rating_list[i] * (1 + (((1.7 * class_strength) + (1.3 * class_depth))/150))
            min_pot = rating_list[i] * (0.9 + (((1.7 * class_strength) + (1.3 * class_depth))/150))
            rating_list[i] = random.uniform((min_pot * multiplier), (max_pot * multiplier))
        elif i <= 100:
            max_pot = rating_list[i] * (1 + (((1.5 * class_strength) + (1.5 * class_depth))/150))
            min_pot = rating_list[i] * (0.85 + (((1.5 * class_strength) + (1.5 * class_depth))/150))
            rating_list[i] = random.uniform((min_pot * multiplier), (max_pot * multiplier))
        else:
            max_pot = rating_list[i] * (1 + (((class_strength) + (2 * class_depth))/300))
            min_pot = rating_list[i] * (0.85 + (((class_strength) + (2 * class_depth))/150))
            rating_list[i] = random.uniform((min_pot * multiplier), (max_pot * multiplier))
        
        if rating_list[i] > 100:
            rating_list[i] = 100

    return rating_list
    











'''

ITEM 5: STATS + AWARDS

'''




























































































































































