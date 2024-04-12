#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 12:23:36 2023

@author: deji
"""

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup 

''' Scraping College info '''

# DIV 1 FBS

fbs = 'https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_programs'

response = requests.get(fbs)
table_class = 'wikitable sortable jquery-tablesorter'

soup = BeautifulSoup(response.text, 'html.parser')
fbs_table = soup.find('table',{'class':"wikitable"})

fbs = pd.read_html(str(fbs_table))
fbs = pd.DataFrame(fbs[0])



fbs.drop(columns=['Enrollment', 'Former Conferences', 'Joined FBS', 'First Year', 'First Joined FBS', 'Left FBS', 'City',  'State [n 1]'], inplace = True)
fbs.rename(columns={'Current Conference[n 2]':'Conference', 'School':'Team'}, inplace = True)
fbs.replace(['Independent[n 5]', 'Pac-12[n 7]', 'Pac-12[n 4]', 'Mountain West[n 9]', 'American[n 15]', 'Big 12[n 17]', 'Pac-12[n 19]', 'ACC[n 24]', 'Independent[n 30]'], 
            ['Independent', 'Pac-12', 'Pac-12', 'Mountain West', 'American', 'Big 12', 'Pac-12', 'ACC', 'Independent'], inplace=True)

# NAIA  
naia_url = 'https://en.wikipedia.org/wiki/List_of_NAIA_football_programs'

response_2 = requests.get(naia_url)

soup = BeautifulSoup(response_2.text, 'html.parser')
naia_table = soup.find('table',{'class':"wikitable"})

naia = pd.read_html(str(naia_table))
naia = pd.DataFrame(naia[0])


naia.drop(columns=['Primary conference', 'State', 'City'], inplace = True)
naia.rename(columns={'Conference for football':'Conference', 'Institution':'Team'}, inplace = True)


# FCS
fcs_url = 'https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FCS_football_programs'

response_3 = requests.get(fcs_url)

soup = BeautifulSoup(response_3.text, 'html.parser')
fcs_table = soup.find('table',{'class':"wikitable"})

fcs = pd.read_html(str(fcs_table))
fcs = pd.DataFrame(fcs[0])


fcs.drop(columns=['School', 'Program established', 'First FCS season', 'City', 'State[a]'], inplace = True)
fcs.rename(columns={'Name':'Nickname', 'Conference[b]':'Conference'}, inplace = True)
fcs.replace(['LIU[f]', 'CAA[c]', 'Big Sky[e]'], ['LIU', 'CAA', 'Big Sky'], inplace=True)

# DIV 2
d2_url = 'https://en.wikipedia.org/wiki/List_of_NCAA_Division_II_football_programs'

response_4 = requests.get(d2_url)

soup = BeautifulSoup(response_4.text, 'html.parser')
d2_table = soup.find('table',{'class':"wikitable"})

d2 = pd.read_html(str(d2_table))
d2 = pd.DataFrame(d2[0])


d2.drop(columns=['Note', 'First Division II season', 'Stadium', 'Cap.', 'City', 'State[a]'], inplace = True)
d2.rename(columns={'School':'Team', 'Conference[b]':'Conference'}, inplace = True)
d2.replace(['Pennsylvania Western University California (California [PA])[D2 5]', 'Pennsylvania Western University Clarion (Clarion)[D2 11]','Colorado School of Mines (Colorado Mines)', 'Colorado State University–Pueblo (CSU Pueblo)',
            'Pennsylvania Western University Edinboro (Edinboro)[D2 14]', 'Missouri University of Science and Technology (Missouri S&T)', 'Indiana University of Pennsylvania (IUP)', 'Michigan Technological University (Michigan Tech)',
            'South Dakota School of Mines and Technology (South Dakota Mines)'],
           ['California (PA)', 'Clarion', 'Colorado Mines', 'CSU Pueblo', 'Edinboro','Missouri S&T', 'IUP', 'Michigan Tech', 'South Dakota Mines'], inplace=True)


# DIV 3
d3_url = 'https://en.wikipedia.org/wiki/List_of_NCAA_Division_III_football_programs'

response_5 = requests.get(d3_url)

soup = BeautifulSoup(response_5.text, 'html.parser')
d3_table = soup.find_all('table',{'class':'wikitable'})

d3 = pd.read_html(str(d3_table))
d3 = pd.DataFrame(d3[1])


d3.drop(columns=['Enrollment', 'First played', 'City', 'State[a]', 'Joined Division III'], inplace = True)
d3.rename(columns={'Current conference[b]':'Conference'}, inplace = True)
d3['Team'] = d3['Team'].str.replace('^','')
d3['Team'] = d3['Team'].str.replace('*','')
d3.replace(['ECFC[c]', 'ECFC[d]', 'OAC[l]'], ['ECFC', 'ECFC', 'OAC'], inplace= True)


all_colleges = pd.concat([fbs,fcs,d2,d3,naia], ignore_index=True)

fbs.to_csv('fbs.csv') 
fcs.to_csv('fcs.csv')
naia.to_csv('naia.csv')  
d3.to_csv('d3.csv') 
d2.to_csv('d2.csv') 

all_colleges.to_csv('all_colleges.csv') 



''' Name Cleaning''' 

cols = ['Name', 'Gender', 'Frequency', 'Include?']
first_names = pd.read_csv('SSA_Names_DB.csv', names = cols)

first_names = first_names.loc[first_names['Gender'] == 'M',:]
first_names.drop(columns=['Gender', 'Include?'], inplace = True)

last_names = pd.read_csv('Names_2010Census.csv')
last_names.drop(columns=['count','cum_prop100k', 'pctaian', 'pct2prace', 'pcthispanic'], inplace = True)
last_names['name'] = last_names['name'].str.title()
last_names = last_names.iloc[:-1 , :]

last_names['pctwhite'] = pd.to_numeric(last_names['pctwhite'], errors='coerce')
last_names['pctblack'] = pd.to_numeric(last_names['pctblack'], errors='coerce')
last_names['pctapi'] = pd.to_numeric(last_names['pctapi'], errors='coerce')
last_names['prop100k'] = pd.to_numeric(last_names['prop100k'], errors='coerce')

first_names.to_csv('firstNameList.csv')
last_names.to_csv('lastNameList.csv')









