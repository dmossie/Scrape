import requests
from bs4 import BeautifulSoup

#url = 'https://www.usedvictoria.com/classifieds/all?description=hello+world'
url = "http://www.usedvictoria.com/classifieds/general-merchandise"

# Get html and parse
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Get all articles on first page
articles = soup.findAll('div', attrs={'class': 'useditem-header'})
for item in articles:

	# Parse title
	title = item.find('p', attrs={'class': 'title'})

	# Parse username
	username = item.find('p', attrs={'class': 'username'})

	# Parse description
	description = item.find('p', attrs={'class': 'description'})

	# Parse properties
	properties = item.find('div', attrs={'class': 'property'})

	print title.text.strip()
	print username.text.strip()
	print description.text.strip()
	print properties.text.strip()
	print '-------------------------------'
	print