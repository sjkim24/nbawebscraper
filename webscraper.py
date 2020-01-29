from bs4 import BeautifulSoup
import requests
import json
import re

def scrape_data():
    url = 'https://www.basketball-reference.com/leagues/NBA_2020_per_game.html'
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    playerRows = content.findAll('tr', attrs={"class": "full_table"})
    dataStats = content.findAll('td', {"data-stat": re.compile(r".*")})

    # get all data-stat attributes
    categories = set([])
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

    with open('playersData.json', 'w') as outfile:
        json.dump(playersArr, outfile)

scrape_data()
