from io import BytesIO

import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
from xml.dom import minidom
import xml.etree.ElementTree as et
import asyncio
from threading import Thread
from datetime import datetime, timezone
from email.utils import format_datetime
from datatypes import Movie, TV, Music
import numpy as np

base_url = "https://nzbscout.com"
movie_skips = 6


class Search:

    @staticmethod
    async def search(query, type):
        # Search
        if query == "":
            return Search.create_xml([])
        page = 1
        urls = []
        request_type = "movies"
        nzb_method = Search.get_movie
        if type == "movie":
            request_type = "movies"
            nzb_method = Search.get_movie
        elif type == "tv search":
            request_type = "tv"
            nzb_method = Search.get_tv
        elif type == "music":
            request_type = "audio"
            nzb_method = Search.get_audio
        elif type == "book":
            request_type = "books"

        old_page_urls = []
        page_urls = []
        while (len(page_urls) == 0 or len(old_page_urls) == 0) or (
                (len(page_urls) > 0 or len(old_page_urls) > 0) and np.array_equal(old_page_urls, page_urls)):
            print("Checking page " + str(page))
            old_page_urls = page_urls.copy()
            urls += page_urls
            page_urls = []
            response = requests.get(base_url + "/search?q=" + query + "&page=" + str(page))
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a'):
                href = link.get('href')
                if type == "search":
                    page_urls.append(href)
                else:
                    regex = r'\/' + request_type + r'\/'
                    if re.search(regex, href):
                        page_urls.append(href)
            # Check empty search result
            page_urls = page_urls[movie_skips:]
            print(page_urls)
            if len(page_urls) == 0:
                break
            page += 1
        nzbs = []
        threads = []
        for url in urls:
            thread = Thread(target=nzb_method, args=(url, nzbs))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return Search.create_xml(nzbs)

    @staticmethod
    def get_movie(url, nzbs):
        try:
            print(base_url + url)
            response = requests.get(base_url + url)
            soup = BeautifulSoup(response.text, 'html5lib')
            nzb_url = soup.select_one(
                'a.btn.btn-outline-light.align-items-center.justify-content-center.btn-dwn.w-lg-220rem.h-52rem.ml-5').get(
                'href')
            title = soup.select_one('h6.font-size-36.text-white.mb-4.pb-1').text
            description = soup.select_one('p.text-gray-5500.font-size-16.mb-5.pb-1.text-lh-md').text
            print("Got NZB!")
            nzbs.append(Movie(url=base_url + url,
                              nzb_url=nzb_url,
                              title=title,
                              description=description,
                              length=len(requests.get(base_url + nzb_url).content),
                              language=Search.find_language(soup),
                              posted=Search.find_posted(soup),
                              category="Movie > " + Search.find_category(soup)
                              )
                        )
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def get_tv(url, nzbs):
        try:
            print(base_url + url)
            response = requests.get(base_url + url)
            soup = BeautifulSoup(response.text, 'html5lib')
            nzb_url = soup.select_one(
                'a.btn.btn-outline-light.align-items-center.justify-content-center.btn-dwn.w-lg-220rem.h-52rem.ml-5').get(
                'href')
            title = soup.select_one('h6.font-size-36.text-white.mb-4.pb-1').text
            description = soup.select_one('p.text-gray-5500.font-size-16.mb-5.pb-1.text-lh-md').text
            print("Got NZB!")
            nzbs.append(TV(url=base_url + url,
                           nzb_url=nzb_url,
                           title=title,
                           description=description,
                           length=len(requests.get(base_url + nzb_url).content),
                           language=Search.find_language(soup),
                           posted=Search.find_posted(soup),
                           category="TV > " + Search.find_category(soup)
                           )
                        )
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def get_music(url, nzbs):
        try:
            print(base_url + url)
            response = requests.get(base_url + url)
            soup = BeautifulSoup(response.text, 'html5lib')
            nzb_url = soup.select_one(
                'a.btn.btn-outline-light.align-items-center.justify-content-center.btn-dwn.w-lg-220rem.h-52rem.ml-5').get(
                'href')
            title = soup.select_one('h6.font-size-36.text-white.mb-4.pb-1').text
            description = soup.select_one('p.text-gray-5500.font-size-16.mb-5.pb-1.text-lh-md').text
            print("Got NZB!")
            nzbs.append(Music(url=base_url + url,
                              nzb_url=nzb_url,
                              title=title,
                              description=description,
                              length=len(requests.get(base_url + nzb_url).content),
                              language=Search.find_language(soup),
                              posted=Search.find_posted(soup),
                              category="TV > " + Search.find_category(soup)
                              )
                        )
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def get_music(url, nzbs):
        try:
            print(base_url + url)
            response = requests.get(base_url + url)
            soup = BeautifulSoup(response.text, 'html5lib')
            nzb_url = soup.select_one(
                'a.btn.btn-outline-light.align-items-center.justify-content-center.btn-dwn.w-lg-220rem.h-52rem.ml-5').get(
                'href')
            title = soup.select_one('h6.font-size-36.text-white.mb-4.pb-1').text
            description = soup.select_one('p.text-gray-5500.font-size-16.mb-5.pb-1.text-lh-md').text
            print("Got NZB!")
            nzbs.append(TV(url=base_url + url,
                           nzb_url=nzb_url,
                           title=title,
                           description=description,
                           length=len(requests.get(base_url + nzb_url).content),
                           language=Search.find_language(soup),
                           posted=Search.find_posted(soup),
                           category="Music > " + Search.find_category(soup)
                           )
                        )
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def find_language(soup):
        try:
            description = Search.find_by_text(soup, 'th', "Language")
            return Search.find_children_text(description, 'td')
        except:
            return None

    @staticmethod
    def find_posted(soup):
        try:
            description = Search.find_by_text(soup, 'th', "Posted")
            posted = Search.find_children_text(description, 'td')
            dt = datetime.strptime(posted, '%Y-%m-%d %H:%M:%S')
            return format_datetime(dt.utcnow().replace(tzinfo=timezone.utc), usegmt=False)
        except:
            return None

    @staticmethod
    def find_category(soup):
        try:
            parent = soup.select_one('ol.breadcrumb.dark.font-size-1')
            category = parent.findChildren()[4]
            return category.findChildren()[0].text
        except:
            return None

    @staticmethod
    def find_by_text(soup, tag_name, text):
        return soup.find(lambda tag: tag.name == tag_name and text in tag.text)

    @staticmethod
    def find_children_text(description, tag_name):
        return description.parent.find(tag_name).text

    @staticmethod
    def create_xml_base():
        # https://newznab.readthedocs.io/en/latest/misc/api/?highlight=search#movie-search
        # Create <rss>
        rss = et.Element("rss")
        rss.set('version', '2.0')
        channel = et.SubElement(rss, 'channel')

        title = et.SubElement(channel, "title")
        title.text = "NZBScoutCrawler"

        description = et.SubElement(channel, "description")
        description.text = "NZBScoutCrawler"

        return rss, channel

    @staticmethod
    def create_xml(list):
        rss, channel = Search.create_xml_base()

        newznab_response = et.SubElement(channel, "newznab:response")
        newznab_response.set("offset", '0')
        newznab_response.set("total", str(len(list)))

        for item in list:
            print("Film: " + item.title)
            xmlitem = et.SubElement(channel, "item")
            if item.title:
                title = et.SubElement(xmlitem, "title")
                title.text = item.title
            description = et.SubElement(xmlitem, "description")
            if item.description:
                description.text = item.description
            elif item.title:
                description.text = item.title
            guid = et.SubElement(xmlitem, "guid")
            guid.text = item.url
            link = et.SubElement(xmlitem, "link")
            link.text = item.url
            if item.language:
                language = et.SubElement(xmlitem, "language")
                language.text = item.language
            if item.posted:
                posted = et.SubElement(xmlitem, "pubDate")
                posted.text = item.posted
            if item.category:
                category = et.SubElement(xmlitem, "category")
                category.text = item.category
            enclosure = et.SubElement(xmlitem, "enclosure")
            enclosure.set("url", item.nzb_url)
            enclosure.set("type", "application/x-nzb")
            enclosure.set("length", str(item.length))
        xdec = """<?xml version="1.0" encoding="UTF-8"?>"""
        xml = et.tostring(rss, encoding="utf-8").decode('utf-8')
        xml = xdec + xml
        return xml.encode('utf-8')
