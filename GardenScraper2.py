import requests
import os
from bs4 import BeautifulSoup
from woocommerce import API

session = requests.Session()

print('GardenScraper v.2 by Django Claughan \nEdited by Fatih Canli' )

# Get login details form setup file
#thisFolder = os.path.dirname(os.path.abspath(__file__))
#setupFile = os.path.join(thisFolder, 'SETUP.txt')
f = open('SETUP.txt', "r")
details = f.read().split('\n') 

links = open('links.txt', "r")
link = links.read().split('\n') 

link = [x for x in link if x.find('https://www.gardners.com/') is 0]

print('Gardeners details')
print(details[4])
print(details[5])
print(details[6])
print('')
print('WooCommerce details')
print(details[9])
print(details[12])
print(details[15])
print(str(len(link))+' entries detected. Please press ENTER to proceed')

input()


# Initialise Woocommerce
wcapi = API(
    url = details[9],
    consumer_key = details[12],
    consumer_secret = details[15],
    version = 'wc/v3'
)

# Package Gardeners login details
payload = {
    'AccountNumber': details[4], 
    'UserName': details[5],
    'Password': details[6]
}

# Post the payload to the site to log in
s = session.post("https://www.gardners.com/Account/LogOn", data=payload)

print()

for url in link:
# Start loop to add products

  # Navigate to the next page and scrape the data
  page = session.get(url)

  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find(id='body')
  # Get title
  searchBlock = results.find('div', class_='titleContributor')
  title = searchBlock.find('h1')
  title = (title.text) 
  # Get author(s)
  author = searchBlock.find_all('a')
    # Add author(s) to title
  n = 0
  for i in author:
      if n == 0:
          title = title + ' by ' + i.text
      elif n == len(author) - 1:
          title = title + ' and ' + i.text
      else:
          title = title + ', ' + i.text
      n = n + 1
   # Get ISBN
  searchBlock = results.find('li', class_='isbn')
  if searchBlock == None:
        isbn ='No ISBN'
  else:
        isbn = searchBlock.find_all('span')
        isbn = isbn[1].text
  # Get RRP
  searchBlock1 = results.find('div', class_='purchaseBlock')
  rrp = searchBlock1.find('span', class_='retailPrice')
  if rrp == None:
        print(url)
        print(isbn+' '+title+' '+'is unavailable.')
        print('\n\n')
  else: 
          print(isbn+' '+title+' '+'is available.')
          rrp = rrp.text
          print(rrp)
          
        
          # Get stock and change number for site
        
          stock = searchBlock1.find(class_='availability')['data-copies']
  
        
          if int(stock) > 4:
              stock = 4
          elif int(stock) > 0:
              stock = stock
          else:
              stock = 0
          print('Stock: '+str(stock))
          

          # Get description
          searchBlock = results.find('div', class_='description')
          if searchBlock == None:
                description = 'No description Available'
                print(description)
          else:
                description = searchBlock.find(class_='productDescription')
                description = description.text

          # Get image url
          searchBlock = results.find(class_='imageContainer')

          if searchBlock.find('img')['src'] == "/Public/Images/noimage.jpg":
                imageSrc = 'https://www.narberthmuseum.co.uk/wp-content/uploads/woocommerce-placeholder.png'
                print('No image available')
          else:
                imageSrc = searchBlock.find('img')['data-zoom-image']
                imageSrc = 'https:' + imageSrc

          print('\n\n')
          # Package data to post to Woocommerce
          data = {
            'images': [
                    ],
            'name': title,
            'regular_price': rrp,
            'short_description': description,
            'sku': isbn,
            'manage_stock': True,
            'stock_quantity': stock,
            'status': 'publish',
            'type': 'simple'
          }

              # Post data to the Woocommerce API
"""    
              print(wcapi.post('products',data).json())
  
              print('')


"""
print('Program finished. Press ENTER to close')
input()