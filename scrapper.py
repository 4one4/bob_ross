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
all_paint_colors = {}
datacols = ['episode',
        'alizarin_crimson',
        'bright_red',
        'cadmium_yellow',
        'phthalo_green',
        'prussian_blue',
        'sap_green',
        'titanium_white',
        'van_dyke_brown',
        'black_gesso',
        'burnt_umber',
        'indian_yellow',
        'phthalo_blue',
        'yellow_ochre',
        'liquid_black',
        'midnight_black',
        'liquid_clear',
        'dark_sienna',
        'indian_red']
df_painting_colors = pd.DataFrame(columns=datacols)

#get a list of all the painting numbers
anchors = soup.find_all('a', {'class':'progressive replace'})
for a in anchors:
   painting_numbers.append((a['href']).replace('/painting/', ''))


for painting_num in painting_numbers[:5]:
    
    #let's get our 'key' the season/episode
    page = get(painting_base_url + painting_num)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    
    header = soup.find('h3')
    #we'll need to 0 pad these numbers to match our key
    season, episode = re.findall(r'\d+', header.text)
    key = 'S' + season.zfill(2) + 'E' + episode.zfill(2)
    
    #get our list of colors
    colors = soup.find_all('li', style=re.compile(r'color'))
    
    row_dict = {}
    row_dict['episode'] = key
    for color in colors:
        color_name = color.find('a').text.strip()
        color_hex = color['style'][7:]
        formatted_color_name = str.lower(color_name.replace(' ', '_'))
        row_dict[formatted_color_name] = 1
        
        
        #check to see if we have this color in our global list
        if color_name not in all_paint_colors:
            all_paint_colors[color_name] = color_hex
        
    
    df_painting_colors = df_painting_colors.append(row_dict, ignore_index=True)

df_painting_colors.fillna('0', inplace=True)

df_painting_colors.to_csv('painting_colors.csv')

    #download the painting image - ONLY IF DATA ISN'T ALREADY SCRAPED
    #img_data = requests.get(image_base_url + painting_num + '.png').content
    #with open('images/' + key + '.png', 'wb') as handler:
    #    handler.write(img_data)