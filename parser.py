import requests, time
from xml.etree import ElementTree
from pprint import pprint

# Get the feed data
def make_request(url):
	while True:
		page = requests.get(url)

		# Request the page again if used vic had a 503
		if '503 Service Temporarily Unavailable' not in page.content:
			break
	
	return page.content

# Parse the items
def parse_data(data):

	# Hold all the items here
	items = []

	# For every item
	tree = ElementTree.fromstring(data)
	for element in tree[0].findall('item'):

		# New item dictionary
		new_item = {}

		# Parse the price and title from the title element
		if len(element[0].text.split('- $'))  == 2:
			title,price = element[0].text.split('- $')
		else:
			title = element[0].text
			price = 0

		# Add properties to the new item
		new_item['title'] = title
		new_item['price'] = int(price)
		new_item['link'] = element[1].text
		#new_item['description'] = element[2].text
		new_item['pubdate'] = element[3].text

		# Add the new item to the list of all items
		items.append(new_item)

	return items

url = "http://www.usedvictoria.com/index.rss?category=all"
keywords = ['table']

content = make_request(url)
data = parse_data(content)

pprint(data)