from bs4 import BeautifulSoup
import requests
import json
import re
import pdb;

def scrape_players_data():
    url = 'https://www.basketball-reference.com/leagues/NBA_2020_per_game.html'
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    playerRows = content.findAll('tr', attrs={"class": "full_table"})
    dataStats = content.findAll('td', {"data-stat": re.compile(r".*")})

    # get all data-stat attributes
    categories = set()
    for dataStat in dataStats:
        categories.add(dataStat.get("data-stat"))

    # create playerObject JSONs
    playersArr = []
    for playerRow in content.findAll('tr', attrs={"class": "full_table"}):
        playerObject = {}
        for category in categories:
            categoryColumn = playerRow.find('td', attrs={"data-stat": category})
            if category == 'player':
                playerObject["first_name"] = categoryColumn.get("csk").split(",")[1]
                playerObject["last_name"] = categoryColumn.get("csk").split(",")[0]
            else:
                playerObject[category] = categoryColumn.text

        playersArr.append(playerObject)

    with open('json_data/playersData.json', 'w') as outfile:
        json.dump(playersArr, outfile)


def scrape_schedule_data():
    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april']
    schedulesArr = []

    for month in months:
        url = f'https://www.basketball-reference.com/leagues/NBA_2020_games-{month}.html'
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser")
        dataStats = content.findAll('td', {"data-stat": re.compile(r".*")})
        dataStats.insert(0, content.find('th', {"data-stat": "date_game"}))
        scheduleRows = content.findAll('tr')

        # get all data-stat attributes
        categories = set()
        for dataStat in dataStats:
            categories.add(dataStat.get("data-stat"))

        # create scheduleObject JSONS
        row_index = 0
        for scheduleRow in scheduleRows:
            if row_index == 0:
                row_index += 1
                continue
            else:
                scheduleObject = {}
                for category in categories:
                    if category == 'date_game':

                        categoryColumn = scheduleRow.find('th', attrs={"data-stat": category})
                        scheduleObject[category] = categoryColumn.get("csk")
                    else:
                        categoryColumn = scheduleRow.find('td', attrs={"data-stat": category})
                        scheduleObject[category] = categoryColumn.text

                schedulesArr.append(scheduleObject)
                row_index += 1
        with open('json_data/schedulesData.json', 'w') as outfile:
            json.dump(schedulesArr, outfile)

scrape_players_data()
scrape_schedule_data()
