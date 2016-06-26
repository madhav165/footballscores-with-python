#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
import re

global URL

def set_url():
    global URL
    URL = "http://www.goal.com/en-india/live-scores"

def get_html():
    with urllib.request.urlopen(URL) as response:
        return response.read();

def get_matches(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    
    matches_soup = soup.findAll('section', class_='matchday')
    matches_soup = matches_soup[3:]
    dates = []
    series = []
    statuses = []
    teams = []
    scores = []
    team1s = []
    team2s = []
    match_data = []
    for x in matches_soup:
        series_soup = x.findAll('table', class_='matches')
        for y in series_soup:
            indi_matches_soup = y.findAll('tbody', class_='match')
            for z in indi_matches_soup:
                if (len(series)>0 and y.find('span', class_='comp-title').text.strip() == last_series):
                    series.append('')
                else:
                    series.append(y.find('span', class_='comp-title').text.strip())
                    last_series=y.find('span', class_='comp-title').text.strip()
                date = re.sub(r'.*day\ ', '', x.h3.text.strip())
                if (len(dates)>0 and date == last_date):
                    dates.append('')
                else:
                    dates.append(date)
                    last_date=date
                statuses.append(z.find('td', class_='status').text.strip())
                for k in z.findAll('td', class_='team'):
                    teams.append(k.text.strip())
                main_score = z.find('td', class_='vs').div.text.strip()
                if(statuses[-1]=='PEN'):
                    pen_score=z.find('tr',class_='score-details').td.text.strip()
                    winning_team = pen_score.split()[0].strip()
                    pen_score=re.sub('[a-zA-Z]','',pen_score).strip()
                    if (winning_team is teams[-2]):
                        scores.append(main_score+' ('+pen_score+')')
                    else:
                        scores.append(main_score+' ('+pen_score[::-1]+')')
                else:
                    scores.append(main_score)
                #scores.append(z.find('td', class_='vs').text.strip())

    
    matchno = int(len(teams)/2)
    for i in range(matchno):
        team1s.append(teams[2*i])
    for i in range(matchno):
        team2s.append(teams[2*i+1])

    match_data.append(['Date', 'Series', 'Status', 'Team', 'Score', 'Team'])
    for i in range(len(team1s)):
        match_data.append([dates[i], series[i], statuses[i], team1s[i], scores[i], team2s[i]])

    return match_data


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
