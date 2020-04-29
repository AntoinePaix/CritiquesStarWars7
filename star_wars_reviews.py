#!/usr/bin/python3
# Coding: utf-8

import requests
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup
import time

def convert_date(date):
    date = date.replace('Publiée le ', '')
    day, month, year = date.split()
    day = int(day)
    year = int(year)
    months = {'janvier':1, 'février':2, 'mars':3, 'avril':4, 'mai':5, 'juin':6, 'juillet':7, 'août':8, 'septembre':9, 'octobre':10, 'novembre':11, 'décembre':12}
    month = months[month]
    date = datetime(year, month, day)
    return date

link_generator = ('http://www.allocine.fr/film/fichefilm-215097/critiques/spectateurs/recentes/?page=' + str(i) for i in range(1, 308))

def parsing(lien):

    url = lien

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    reviews = soup.find_all('div', class_='hred review-card cf')

    auteurs = [auteur.find('div', class_='meta-title').text.strip() for auteur in reviews]
    notes = [note.find('span', class_='stareval-note').text.strip() for note in reviews]
    dates = [convert_date(date.find('span', class_='review-card-meta-date light').text.strip()) for date in reviews]
    critiques = [critique.text for critique in soup.find_all('div', class_='content-txt review-card-content')]

    return list(zip(auteurs, notes, dates, critiques))

        
# Main Program
compteur = 0

with open('datas/critiques_star_wars_7.csv', 'w') as csvfile:
    fieldnames = ['auteur', 'note', 'date', 'critique']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for lien in link_generator:
        for elem in parsing(lien):
            auteur, note, date, critique = elem
            print('*' * 100)
            print("MESSAGE :", compteur)
            print(auteur, note, date, critique)
            writer.writerow({'auteur':auteur, 'note':note, 'date':date, 'critique':critique})
            compteur += 1
            # time.sleep(5)
