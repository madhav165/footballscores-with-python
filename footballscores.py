#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
from terminaltables import AsciiTable

global URL

def set_url():
    global URL
    URL = "http://www.goal.com/en-india/live-scores"

def get_html():
    with urllib.request.urlopen(URL) as response:
        return response.read();

def get_matches(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    
    vs_soup=soup.find_all('td', class_='vs')
    scores = []
    for x in vs_soup:
        scores.append(x.div.string.strip())

    statuses_soup=soup.find_all('td', class_='status')
    statuses = []
    for x in statuses_soup:
        statuses.append(x.span.string.strip())

    teams_soup=soup.find_all('div', class_='module-team')
    teams = []
    for x in teams_soup:
        teams.append(x.span.string.strip())

    matchno = int(len(teams)/2)

    team1s = []
    for i in range(matchno):
        team1s.append(teams[2*i])

    team2s = []
    for i in range(matchno):
        team2s.append(teams[2*i+1])

    matches_data=[]
    for i in range(matchno):
        match_data=[statuses[i],team1s[i],scores[i],team2s[i]]
        matches_data.append(match_data)

    return matches_data


def print_matches(matches_data):
    table = AsciiTable(matches_data)
    table.inner_heading_row_border = False
    table.inner_row_border = False
    print (table.table)

set_url()
html_doc = get_html()
matches_data = get_matches(html_doc)
print_matches(matches_data)
