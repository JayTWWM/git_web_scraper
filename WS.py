import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
import os

def handle(handled):
    if handled == None:
        return "NaN"
    else:
        return handled.text.strip()

data = []
count = 1

print("Input github id:")
id = input()

page = requests.get("https://github.com/" + id + "?tab=repositories")
content = page.content
soup = BeautifulSoup(content, 'html.parser')

div = soup.find('div', attrs={'class':'clearfix'})
img = div.img['src']
name = div.find('span', itemprop = 'additionalName').text

dir = os.path.join("./",name)
if not os.path.exists(dir):
    os.mkdir(dir)

f = open('./' + name + '/Profile.jpg','wb')
f.write(urllib.request.urlopen(img).read())
f.close()

list = soup.find(id='user-repositories-list')
all_repo = list.find_all('li', attrs={'class':'col-12 d-flex width-full py-4 border-bottom public source'})

for repo in all_repo:
    title = handle(repo.find('h3', attrs={'class':'wb-break-all'}))
    desc = handle(repo.find('p', itemprop='description'))
    time = handle(repo.find('relative-time', attrs={'class':'no-wrap'}))
    lang = handle(repo.find('span', itemprop='programmingLanguage'))
    star = handle(repo.find('a', class_="muted-link mr-3"))
    data.append([count, title, desc, time, lang, star])
    count+=1

with open('./' + name + '/repositories.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Sr. No.", "Name", "Description", "Date", "Programming Language", "Stars"])
    writer.writerows(data)