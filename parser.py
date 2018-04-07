import requests, time
from xml.etree import ElementTree


while True:

	# Load RSS feed
	page = requests.get("http://www.usedvictoria.com/index.rss?category=all")
	
	# Request the page again if if used vic had a 503
	if '503 Service Temporarily Unavailable' not in page.content:

		# Parse the items

		# Hold all the items here
		items = []

		# For every item
		tree = ElementTree.fromstring(page.content)
		for element in tree[0].findall('item'):

			# Item dictionary
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
			new_item['description'] = element[2].text
			new_item['pubdate'] = element[3].text

			# Add the new item to the list of all items
			items.append(new_item)

		for item in items:
			if 'table' in item['title']:
				print item

		time.sleep(10)