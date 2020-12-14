import requests
import os
from bs4 import BeautifulSoup
from woocommerce import API

session = requests.Session()

print('GardenScraper by Django Claughan \n')

# Get login details form setup file
thisFolder = os.path.dirname(os.path.abspath(__file__))
setupFile = os.path.join(thisFolder, 'SETUP.txt')
f = open(setupFile, "r")
details = f.read().split('\n') 

print('Gardeners details')
print(details[4])
print(details[5])
print(details[6])
print('')
print('WooCommerce details')
print(details[9])
print(details[12])
print(details[15])
print('')

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

# Start loop to add products
breakout = 'y'
while breakout != 'n':

  # Get Gardeners url from user
  url = input('Please paste Gardeners product url ')

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
  print(title)


  # Get ISBN
  searchBlock = results.find('li', class_='isbn')
  isbn = searchBlock.find_all('span')
  isbn = isbn[1].text
  print(isbn)

  # Get RRP
  searchBlock = results.find('div', class_='purchaseBlock')
  rrp = searchBlock.find('span', class_='retailPrice')
  rrp = rrp.text
  print(rrp)

  # Get stock and change number for site
  stock = searchBlock.find(class_='availability')['data-copies']
  if int(stock) > 4:
      stock = 4
  elif int(stock) > 0:
      stock = stock
  else:
      stock = 0
  print(stock)

  # Get description
  searchBlock = results.find('div', class_='description')
  description = searchBlock.find(class_='productDescription')
  if description == None:
       description = ''
  else:
       description = description.text

  # Get image url
  searchBlock = results.find(class_='imageContainer')
  imageSrc = searchBlock.find('img')['data-zoom-image']
  imageSrc = 'https:' + imageSrc
  print(imageSrc)
  print('')

  # Package data to post to Woocommerce
  data = {
    'images': [{
                  "src": imageSrc
              },
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
  print(wcapi.post('products',data).json())
  
  print('')

  # Ask user if they wish to add more products
  breakout = input('Do you wish to add another product? (y/n) ')
  print('')

print('Program finished')