#si-exercise

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def collectLegoSets(startURL):
    sets = []
    prices = []
    pieces = []
    minifigs = []

    for page in range(1, 35):  # Adjust the range based on the number of pages
        url = startURL + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for set_info in soup.find_all('article', class_='set'):
            set_name = set_info.find('h1').text.strip()
            sets.append(set_name)
            
            price = set_info.find('div', class_='meta').find_all('dd')[1].text.strip()
            price = float(price.replace('€', '').replace(',', '')) if '€' in price else np.nan
            prices.append(price)
            
            piece_count = set_info.find('div', class_='meta').find_all('dd')[2].text.strip()
            piece_count = int(piece_count.replace(',', '')) if piece_count.isdigit() else np.nan
            pieces.append(piece_count)
            
            minifig_count = set_info.find('div', class_='meta').find_all('dd')[3].text.strip()
            minifig_count = int(minifig_count) if minifig_count.isdigit() else np.nan
            minifigs.append(minifig_count)
    
    lego_df = pd.DataFrame({
        'Set': sets,
        'Price_Euro': prices,
        'Pieces': pieces,
        'Minifigs': minifigs
    })

    return lego_df

startURL = "https://brickset.com/sets/year-2019"
lego_df = collectLegoSets(startURL)
print(f"Total sets scraped: {lego_df.shape[0]}")

lego_df.to_csv('lego2019.csv', index=False)
print("Data saved to lego2019.csv")