import requests
import re
import random
import pandas as pd
from bs4 import BeautifulSoup
from math import ceil
from tqdm import tqdm
from user_agents import user_agent_list


class DkWholesaleScraper():

    def __init__(self, url):
        self.url = url        

    
    def scraper(self):
         # Pick a random uer agent
        user_agent = random.choice(user_agent_list.user_agent_list)

        # Set the headers
        headers = {
            'User-Agent': user_agent
        }

        # This is the session
        s = requests.Session()

        # Make a request in a session
        r = s.get(self.url, headers=headers)

        # Scrape the content to end page
        soup = BeautifulSoup(r.content, 'lxml')

        # Scrape the end page number
        try:
            end_page_number = int(soup.find('ul', class_='items pages-items').find_all('li', class_='item')[3].text.strip())
        except:
            end_page_number = 'no end page'

        end_page = end_page_number + 1
                       
        # print(end_page_number)       
        # print(end_page)

        # A list to productlinks
        productlinks = []

        # Iterate all productlinks between a range
        for x in range(1, end_page):

            # Make a request in a session                  
            r = s.get(self.url + f'?p={x}', headers=headers)

            # Scrape the content
            soup = BeautifulSoup(r.content, 'lxml')

            # Identify all products
            productlist = soup.find_all('strong', class_='product name product-item-name')

            # Save all links in productlinks list
            for item in productlist:
                for link in item.find_all('a', href=True):
                    productlinks.append(link['href'])
                    #print(link['href'])
        
         # A list to the scraping data        
        list = []

        # Iterate all links in productlinks
        for link in tqdm(productlinks):
            
            # Make requests with headers in one sessions (s)
            r = s.get(link, headers=headers)

            # Scrape the content in the soup variable with 'lxml' parser
            soup = BeautifulSoup(r.content, 'lxml') 

            # Scrape name
            try:
                name = str(soup.title.string.strip()[:-13])
            except:
                name = ''

            # Scrape barcode
            try:
                barcode = str(soup.find('ul', {'id': 'product-attribute-specs-table'}).find(text=re.compile("Bar code:"))[10:-1])

                if barcode == 'N/A':
                    barcode = ''              

            except:
                barcode = ''
            
            # Scrape pack size
            pack_size = '1'

            # Scrape netto unit price and origi price
            try:
                netto_unit_price_origi_price = float(soup.find('span', class_='price').text.strip()[1:])
            except:
                netto_unit_price_origi_price = float() 

            try:
                # Scraper gross unit price and origi price
                gross_unit_price_origi_price = float(round(netto_unit_price_origi_price * 1.2, 2))

                # VAT calculation
                vat = round(((gross_unit_price_origi_price - netto_unit_price_origi_price) / netto_unit_price_origi_price) * 100)
            except:
                pass                        
            
            # Scrape product code
            try:                
                product_code = str(soup.find('strong', class_='type').find_next_sibling('div').string.strip())
            except:
                product_code = ''

            # Scrape availability
            try:
                availability = bool(soup.find('button', {'id': 'product-addtocart-button'}))            
            except:
                availability = bool(False)

            # Define a dictionary for csv
            dkwholesale = {                 
                'link': link,
                'name': name,
                'barcode': barcode,
                'pack_size': pack_size,
                'netto_unit_price_origi_price': netto_unit_price_origi_price,
                'gross_unit_price_origi_price': gross_unit_price_origi_price,
                'vat': vat,                
                'product_code': product_code,        
                'availability': availability
            }

            # Add the dictionary to the list every iteration
            list.append(dkwholesale)

            # Print every iteration        
            # print(
            #     '\n--------- Saving: ---------\n'             
            #     'link: ' + str(dkwholesale['link']) + '\n'
            #     'name: ' + str(dkwholesale['name']) + '\n'
            #     'barcode: ' + str(dkwholesale['barcode']) + '\n'
            #     'pack size: ' + str(dkwholesale['pack_size']) + '\n'
            #     'netto unit price origi price: ' + str(dkwholesale['netto_unit_price_origi_price']) + '\n'
            #     'gross unit price origi price: ' + str(dkwholesale['gross_unit_price_origi_price']) + '\n'
            #     'vat: ' + str(dkwholesale['vat']) + '\n'                
            #     'product code: ' + str(dkwholesale['product_code']) + '\n'
            #     'availability: ' + str(dkwholesale['availability']) + '\n'
            # )

        # Make table to list
        df = pd.DataFrame(list)

        # Save to csv
        df.to_csv(r'C:\WEBDEV\dkwholesale_scraper\exports\dkwholesale.csv', mode='a', index=False, header=True)        


get_dkwholesale_watches = DkWholesaleScraper('https://www.dkwholesale.com/watches.html')
get_dkwholesale_clocks = DkWholesaleScraper('https://www.dkwholesale.com/clocks.html')
get_dkwholesale_audio_video = DkWholesaleScraper('https://www.dkwholesale.com/audio-video.html')
get_dkwholesale_domestic_appliances = DkWholesaleScraper('https://www.dkwholesale.com/domestic-appliances.html')
get_dkwholesale_electrical = DkWholesaleScraper('https://www.dkwholesale.com/electricals.html')
get_dkwholesale_mobile_phones_accessories = DkWholesaleScraper('https://www.dkwholesale.com/mobile-phones-accessories.html')
get_dkwholesale_kitchenware = DkWholesaleScraper('https://www.dkwholesale.com/kitchenware.html')
get_dkwholesale_personal_care = DkWholesaleScraper('https://www.dkwholesale.com/personal-care.html')
get_dkwholesale_toys = DkWholesaleScraper('https://www.dkwholesale.com/toys.html')

get_dkwholesale_watches.scraper()
get_dkwholesale_clocks.scraper()
get_dkwholesale_audio_video.scraper()
get_dkwholesale_domestic_appliances.scraper()
get_dkwholesale_electrical.scraper()
get_dkwholesale_mobile_phones_accessories.scraper()
get_dkwholesale_kitchenware.scraper()
get_dkwholesale_personal_care.scraper()
get_dkwholesale_toys.scraper()
