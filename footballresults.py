#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
import re

global URL

def set_url():
    global URL
    URL = "http://www.goal.com/en-india/results"

def get_html():
    with urllib.request.urlopen(URL) as response:
        return response.read();

def get_matches(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    
    matches_soup = soup.findAll('table', class_='match-table')
    series = []
    statuses = []
    teams = []
    scores = []
    team1s = []
    team2s = []
    matches_data = []
    for x in matches_soup:
        match_soup = x.tbody.findAll('tr', class_='clickable')
        for y in match_soup:
            series_name = x.thead.find('span', class_='comp-title').text.strip()
            if(len(series)>0 and series_name == last_series):
                series.append('')
            else:
                series.append(series_name)
                last_series = series_name
            statuses.append(y.find('td', class_='status').text.strip())
            main_score = y.find('td', class_='vs').div.text.strip()
            if(statuses[-1]=='PEN'):
                pen_score=x.find('tr',class_='score-details').td.text.strip()
                pen_score=re.sub('[a-zA-Z]','',pen_score).strip()
                scores.append(main_score+' ('+pen_score+')')
            else:
                scores.append(main_score)
            teams_soup=y.findAll('div', class_='module-team')
            for z in teams_soup:
                teams.append(z.span.text.strip())

    matchno = int(len(teams)/2)
    for i in range(matchno):
        team1s.append(teams[2*i])
    for i in range(matchno):
        team2s.append(teams[2*i+1])

    matches_data.append(['Series', 'Status', 'Team', 'Score', 'Team'])
    for i in range(len(team1s)):
        matches_data.append([series[i], statuses[i], team1s[i], scores[i], team2s[i]])

    return matches_data   

def print_matches(matches_data):
    table = AsciiTable(matches_data)
    table.inner_heading_row_border = True
    table.inner_row_border = False
    print (table.table)

set_url()
html_doc = get_html()
matches_data = get_matches(html_doc)
#get_matches(html_doc)
print_matches(matches_data)
