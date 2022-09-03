# PROMET V1.0

import csv
import re
from collections import Counter
from urllib.request import urlopen

from bs4 import BeautifulSoup as Soup

PAGENUMBER = 2019
ARAWDATA = []
BRAWDATA = []
OFFICIALDATA = {}
NUMBERS = []
TIMES = []
CHANCE = []
zc = 0

while PAGENUMBER <= 2021:  # Our way of filtering through pages
    COUNTER = 0  # We will need this later
    #url = urlopen('https://www.usamega.com/mega-millions-history.asp?p={}'.format(PAGENUMBER))
    url = urlopen('https://www.lottery.co.za/daily-lotto/results/{}'.format(PAGENUMBER))
    RAW = url.read()  # Reads data into variable
    url.close()  # Closes connection
    PARSED = Soup(RAW, 'html.parser')  # (DATA, Type of Parser)

    for line in PARSED.findAll('td', {'style': 'text-align: center;'}):  # Finds all the 'td' tags with align:right
        if 'Draw Number' not in str(line):  # Checks if tag has those char
            #pRAW = re.findall('d=(.*?)\">', str(line))  # Gathers only the dates from that text
            pRAW = re.findall(r'<td style="text-align: center;">(.*?)</td>', str(line))
            #pRAW = re.findall(r'<td data-title="Draw Number" style="text-align: center;">(.*?)</td>', str(line))
            for pline in pRAW:
                ARAWDATA.append(pline)  # Stores data in list for mutation later

    for line in PARSED.findAll('td', {'style': 'text-align: center; white-space: nowrap;'}):
        #if 'nowrap;' in str(line):  # Needs to be setup this long way
        pRAW = re.findall(r'<div class="result small daily-lotto-ball">(.*?)</div>', str(line))
        #pRAW.extend(re.findall(r'<div class="result small lotto-bonus-ball">(.*?)</div>', str(line)))

        pline = str(pRAW).replace("[", "")
        pline = pline.replace("]", "")
        pline = pline.replace(",", "")
        pline = pline.replace("'", "")

        BRAWDATA.append(pline)

    for date in ARAWDATA:
        OFFICIALDATA[date] = BRAWDATA[COUNTER]  # For every date it will give it value of the numbers
        COUNTER += 1
    PAGENUMBER += 1

with open('lotto.csv', 'w', newline='') as data:
    file = csv.writer(data)
    file.writerows(OFFICIALDATA.items())


def frequency(list):
    global zc
    BUFFED = []  # Local list to manipulate
    for line in list:
        buffer = line.split()
        for bbuffer in buffer:
            BUFFED.append(bbuffer)
    STORED = Counter(BUFFED)  # Counts each unique number
    zc = len(STORED)  # Used to tell us how unique numbers there are

    with open('occurrence.csv', 'w', newline='') as data:
        file = csv.writer(data)
        file.writerows(STORED.items())


def solution():
    with open('occurrence.csv', 'r') as data:
        fileReader = csv.reader(data)
        for row in fileReader:
            NUMBERS.append(row[0])  # Grabs first row which are numbers
            TIMES.append(row[1])  # Grabs second row which is the occurrence
            a = str((int(row[1]) / len(BRAWDATA)))  # Calculates the occurrence divided by total
            CHANCE.append(a[2:4])  # Possible Chance Strips 00.02345 -> 02 which is in percent


REPORT = {  # Dictionary of the list
    'Numbers': NUMBERS,
    'Times': TIMES,
    'Chance': CHANCE,
}

frequency(BRAWDATA)
solution()

with open('report.csv', 'w', newline='') as data:
    dataWriter = csv.writer(data)
    z = 0
    while z < zc:  # Unique numbers there are
        dataWriter.writerow([
            str(REPORT['Numbers'][z]),
            str(REPORT['Times'][z]),
            str(REPORT['Chance'][z]),
        ])
        z += 1

# print(REPORT['Numbers'][10], REPORT['Times'][10], REPORT['Chance'][10])
