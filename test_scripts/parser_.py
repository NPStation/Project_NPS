# -*- coding: utf-8 -*-
from lxml import etree
from lxml.html import parse

# doc = etree.XML('<link>trololo</link>')
# out = doc.xpath('/link')[0].text

# print out

from lxml.html import parse
# Получаем страничку
page = parse('http://mobile.maps.yandex.net/cellid_location/?cellid=12082&operatorid=99&countrycode=250&lac=25254').getroot()
# Ищем все теги <a> с css классом topic
hrefs = page.cssselect("coordinates")
for row in hrefs:
    # Получаем атрибут href
    print row.get("latitude"), row.get("longitude"), row.get("nlatitude"), row.get("nlongitude")

	
# #//*[@id="1"]
# page = parse('http://map.online-gsm.ru/loc/').getroot()
# doc2 = etree.XML(page)
# out2 = unicode(doc2.xpath('//*[@id="1"]')[0].text)

# print unicode(out2)

# Type gsm
# CellID = 88080833
# lac 30445
# mcc 250
# mnc 01
# latitude //*[@id="collapsible0"]/div[1]/div[2]/div/span/span[1]/span[2]
# longitude //*[@id="collapsible0"]/div[1]/div[2]/div/span/span[2]/span[2]


# from bs4 import BeautifulSoup
# from urllib2 import urlopen



# html_doc = urlopen('http://mobile.maps.yandex.net/cellid_location/?cellid=12082&operatorid=99&countrycode=250&lac=25254').read()
# soup = BeautifulSoup(html_doc)
# # print soup

# print soup.find('coordinates')

# for link in soup.find_all('latitude'):
    # print link.get('value')