#si-exercise

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import time
import random

def collectLegoSets(startURL):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        response = requests.get(startURL, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return pd.DataFrame(columns=['Set', 'Price_Euro', 'Pieces', 'Minifigs'])
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    
    lego_data = []
    
    for article in articles:
        row = []
        row.append(article.h1.text)
        

        try:
            price_text = article.find('dt', string="RRP").find_next_sibling().text
            price = float(re.search(r'(\d+.\d+)(\u20AC)', price_text, re.UNICODE).groups()[0])
            row.append(price)
        except AttributeError:
            row.append(np.nan)
        
        try:
            pieces_text = article.find('dt', string="Pieces").find_next_sibling().text
            pieces = int(re.search(r'(\d+)', pieces_text).group(0))
            row.append(pieces)
        except AttributeError:
            row.append(np.nan)
        
        try:
            minifigs_text = article.find('dt', string="Minifigs").find_next_sibling().text
            minifigs = int(re.search(r'(\d+)', minifigs_text).group(0))
            row.append(minifigs)
        except AttributeError:
            row.append(np.nan)
        
        lego_data.append(row)

    
    lego_df = pd.DataFrame(lego_data, columns=['Set', 'Price_Euro', 'Pieces', 'Minifigs'])
    
    try:
        next_page = soup.find('li', class_="next").a['href']
    except AttributeError:
        next_page = None
    
    if next_page:
        time.sleep(random.uniform(1, 3))
        next_page_url = f"https://brickset.com{next_page}"
        next_df = collectLegoSets(next_page_url)
        if not next_df.empty:
            return pd.concat([lego_df, next_df], axis=0)
    
    return lego_df

startURL = "https://brickset.com/sets/year-2019"

print(f"Total sets scraped: {lego2019_df.shape[0]}")

lego2019_df.to_csv('lego2019.csv', index=False)