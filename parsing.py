
import pprint
import re
import requests
from bs4 import BeautifulSoup,  SoupStrainer
import time
import json
# starting from an ID of mathgeneaology  
# e.g. Euler https://www.mathgenealogy.org/id.php?id=38586
# is : 38586 

ALLAUTHORS = {}
EDGES = []
ALLREADYSCRAPED = []
IDCURRENT = 38586
REMAININGIDTOSCRAP = []


def parseIdsAndGetIdsName(idstart):
    idsNames = {}
    page = requests.get("https://www.mathgenealogy.org/id.php?id=" + str(idstart))
    soup = BeautifulSoup(page.content, 'html.parser')
    textAdvisor = soup.find('p', style=re.compile(r'text-align: center; line-height: 2.75ex'))
    try:
        Links = textAdvisor.find_all('a')
        for x in Links:
            id = x['href'].split('=')[1]
            name = x.get_text().replace("  ", " ")
            print("id = " + str(id))
            print("name = " + str(name))
            idsNames[id] = name
    except:
        return {}
    return idsNames


IdsNameStart = parseIdsAndGetIdsName(IDCURRENT)
ALLREADYSCRAPED.append(IdsNameStart)
for idscraped in IdsNameStart:
    ALLAUTHORS[idscraped] =  IdsNameStart[idscraped]
    REMAININGIDTOSCRAP.append(idscraped)



while len(REMAININGIDTOSCRAP) != 0:
    print("remaining ids to scrap: " + str(REMAININGIDTOSCRAP))
    popId = REMAININGIDTOSCRAP.pop()
    if popId in ALLREADYSCRAPED:
        continue
    IdsNameNew = parseIdsAndGetIdsName(popId)
    ALLREADYSCRAPED.append(popId)
    if len(IdsNameNew) == 0:
        continue
    else:
        for idscraped in IdsNameNew:
            ALLAUTHORS[idscraped] =  IdsNameNew[idscraped]
            if idscraped not in REMAININGIDTOSCRAP:
                REMAININGIDTOSCRAP.append(idscraped)
            if (popId,idscraped) not in EDGES:
                EDGES.append((popId,idscraped))
    time.sleep(1)


with open("authors.json","w") as f:
    f.write(json.dumps(ALLAUTHORS))

with open('edges.txt', 'w') as f:
    f.write(json.dumps(EDGES))
