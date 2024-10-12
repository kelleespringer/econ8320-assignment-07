#si-exercise

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def collectLegoSets(year):
    base_url = f"https://brickset.com/sets/year-2019"
    sets_data = []
    page = 1
    
    while True:
        url = f"{base_url}/page-{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        sets = soup.find_all('article', class_='set')
        
        if not sets:
            break
        
        for set in sets:
            name = set.find('h1').text.strip()
            
            price = set.find('dt', string='RRP')
            price_euro = np.nan
            if price:
                price_text = price.find_next('dd').text.strip()
                if '€' in price_text:
                    # Split the price text by '|', take the first part, and remove commas
                    price_euro_str = price_text.split('|')[0].split('€')[1].replace(',', '.')  
                    #Try to convert to float, if it fails assign np.nan
                    try:
                        price_euro = float(price_euro_str)
                    except ValueError:
                        price_euro = np.nan
            
            pieces = set.find('dt', string='Pieces')
            pieces_count = np.nan
            if pieces:
                pieces_text = pieces.find_next('dd').text.strip()
                if pieces_text.isdigit():
                    pieces_count = int(pieces_text)
            
            minifigs = set.find('dt', string='Minifigs')
            minifigs_count = np.nan
            if minifigs:
                minifigs_text = minifigs.find_next('dd').text.strip()
                if minifigs_text.isdigit():
                    minifigs_count = int(minifigs_text)
            
            sets_data.append({
                'Set': name,
                'Price_Euro': price_euro,
                'Pieces': pieces_count,
                'Minifigs': minifigs_count
            })
        
        page += 1
    
    return pd.DataFrame(sets_data)

df_2019 = collectLegoSets(2019)

# Save to CSV
df_2019.to_csv('lego2019.csv', index=False)

print(f"Saved {len(df_2019)} Lego sets to lego2019.csv")
