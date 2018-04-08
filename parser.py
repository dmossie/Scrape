import requests, time, re
from xml.etree import ElementTree
from pprint import pprint
from datetime import datetime, timedelta

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

		# Shift time back by 7 hours
		raw_time = element[3].text.strip('-0000').strip()
		parsed_time = datetime.strptime(raw_time, "%a, %d %b %Y %H:%M:%S")
		pubdate = parsed_time - timedelta(hours=7)

		# Add properties to the new item
		new_item['title'] = title.lower()
		new_item['price'] = int(price)
		new_item['link'] = element[1].text
		new_item['description'] = parse_description(element[2].text)
		new_item['pubdate'] = pubdate

		# Add the new item to the list of all items
		items.append(new_item)

	return items

# Make the description readable
def parse_description(raw):
	raw = re.sub('<[^<]+?>', '', raw)
	raw = raw.replace('&nbsp','')
	raw = raw.replace(';','')
	raw = raw.replace('&gt','')
	return raw.strip().lower()

# Search the title for each item, if it has all keywords in it, return it
def find_matches(items, keywords, price):
	matches = []
	for item in items:
		if item['price'] > price:
			continue
		for keyword in keywords:
			if keyword not in item['title'] and keyword not in item['description']:
				break
			if keyword == keywords[-1]:
				matches.append(item)
	return matches

# Add items from one list to another, if they don't exist already
def add_new(main_list, new_list):
	for i in new_list:
		if i not in main_list:
			main_list.append(i)

	return main_list
# User Input
url = "http://www.usedvictoria.com/index.rss?category=motorcycles"
keywords = ['2008']
price = 10000

# Current List
data = []
matches = []


# Program
while True:
	# Get and parse feed
	request = make_request(url)
	content = parse_data(request)

	# Find out which are the new items
	new_items = []
	for i in content:
		if i not in data:
			new_items.append(i)

	# Check if new items have key words
	new_matches = find_matches(new_items, keywords, price)
	matches = add_new(matches,new_matches)

	# Do something with the matches
	print matches

	# Save the new items and sleep
	data = add_new(data, new_items)

	time.sleep(30)