from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re

all_paintings_url = 'https://www.twoinchbrush.com/all-paintings'
painting_base_url = 'https://www.twoinchbrush.com/painting/'
image_base_url = 'https://www.twoinchbrush.com/images/painting'


page = get(all_paintings_url)
soup = BeautifulSoup(page.text, 'html.parser')

painting_numbers = []


#get a list of all the painting numbers
anchors = soup.find_all('a', {'class':'progressive replace'})
for a in anchors:
   painting_numbers.append((a['href']).replace('/painting/', ''))


for painting_num in painting_numbers:
    
    #let's get our 'key' the season/episode
    page = get(painting_base_url + painting_num)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    
    header = soup.find('h3')
    #we'll need to 0 pad these numbers to match our key
    season, episode = re.findall(r'\d+', header.text)
    key = 'S' + season.zfill(2) + 'E' + episode.zfill(2)
    
    #get our list of colors
    colors = soup.find_all('li', style=re.compile(r'color'))
    color_dict = {}
    for color in colors:
        color_dict[color.find('a').text.strip()] = color['style'][7:]
    
    #download the painting image - ONLY IF DATA ISN'T ALREADY SCRAPED
    #img_data = requests.get(image_base_url + painting_num + '.png').content
    #with open('images/' + key + '.png', 'wb') as handler:
    #    handler.write(img_data)