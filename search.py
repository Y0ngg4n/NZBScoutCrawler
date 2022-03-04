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
from datatypes import Item
import numpy as np

base_url = "https://nzbscout.com"
movie_skips = 6
empty_url_skips = 6


class Search:

    @staticmethod
    async def search(query, type, request):
        # Search
        if query == "":
            empty_urls = []
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            empyt_nzbs = []
            empty_threads = []
            for link in soup.find_all('a'):
                href = link.get('href')
                regex = r'\/movies\/'
                if re.search(regex, href):
                    empty_urls.append(href)
            empty_urls = empty_urls[empty_url_skips:]
            for i in range(6):
                thread = Thread(target=Search.get_item, args=(empty_urls[i], empyt_nzbs))
                thread.start()
                empty_threads.append(thread)
            for thread in empty_threads:
                thread.join()
            return Search.create_xml(empyt_nzbs, request)
        page = 1
        urls = []
        request_type = "movies"
        nzb_method = Search.get_item
        if type == "movie":
            request_type = "movies"
        elif type == "tv search":
            request_type = "tv"
        elif type == "music":
            request_type = "audio"
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
        return Search.create_xml(nzbs, request)

    @staticmethod
    def get_item(url, nzbs):
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
            nzbs.append(Item(url=base_url + url,
                             nzb_url=nzb_url,
                             title=title,
                             description=description,
                             length=len(requests.get(base_url + nzb_url).content),
                             language=Search.find_language(soup),
                             posted=Search.find_posted(soup),
                             category="Movie > " + Search.find_category(soup),
                             newznab_category1="2000",
                             file_size=Search.find_file_size(soup),
                             files=Search.find_files(soup),
                             group=Search.find_group(soup)
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
    def find_file_size(soup):
        try:
            description = Search.find_by_text(soup, 'th', "Size")
            size = Search.find_children_text(description, 'td')
            f = float(size[:3])
            factor = 1
            if "GB" in size:
                factor = 1073741824
            elif "MB" in size:
                factor = 1048576
            elif "KB" in size:
                factor = 1024
            return str(int(f * factor))
        except Exception as e:
            return None

    @staticmethod
    def find_files(soup):
        try:
            description = Search.find_by_text(soup, 'th', "Files")
            return Search.find_children_text(description, 'td')
        except:
            return None

    @staticmethod
    def find_group(soup):
        try:
            description = Search.find_by_text(soup, 'th', "Group")
            td = description.parent.find('td')
            return td.find('span').find('a').text
        except:
            return None

    @staticmethod
    def find_by_text(soup, tag_name, text):
        return soup.find(lambda tag: tag.name == tag_name and text in tag.text)

    @staticmethod
    def find_children_text(description, tag_name):
        return description.parent.find(tag_name).text

    @staticmethod
    def create_xml_base(request):
        # https://newznab.readthedocs.io/en/latest/misc/api/?highlight=search#movie-search
        # Create <rss>
        rss = et.Element("rss")
        rss.set('version', '2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        rss.set('xmlns:newznab', 'http://www.newznab.com/DTD/2010/feeds/attributes/')
        channel = et.SubElement(rss, 'channel')

        title = et.SubElement(channel, "title")
        title.text = "NZBScoutCrawler"

        description = et.SubElement(channel, "description")
        description.text = "NZBScoutCrawler"

        return rss, channel

    @staticmethod
    def create_xml(list, request):
        rss, channel = Search.create_xml_base(request)

        newznab_response = et.SubElement(channel, "newznab:response")
        newznab_response.set("offset", '0')
        newznab_response.set("total", str(len(list)))
        atom_link = et.SubElement(channel, "atom:link")
        atom_link.set("href", str(request.url))
        atom_link.set("rel", 'self')
        atom_link.set("type", 'application/rss+xml')
        title = et.SubElement(channel, "title")
        title.text = "NZBScoutCrawler"
        description = et.SubElement(channel, "description")
        description.text = "API Feed"
        link = et.SubElement(channel, "link")
        link.text = str(request.base_url)
        language = et.SubElement(channel, "language")
        language.text = "en-gb"
        webMaster = et.SubElement(channel, "webMaster")
        webMaster.text = "y0ngg4n@github.com (GitHub)"
        category = et.SubElement(channel, "category")
        image = et.SubElement(channel, "image")
        image_url = et.SubElement(image, "url")
        image_url.text = "https://nzbscout.com/images/logo.svg"
        image_title = et.SubElement(image, "title")
        image_title.text = "NZBScout"
        image_link = et.SubElement(image, "link")
        image_link.text = "https://nzbscout.com/"
        image_description = et.SubElement(image, "description")
        image_description.text = "NZBScout"

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
            newznab_category1 = et.SubElement(xmlitem, "newznab:attr")
            newznab_category1.set('name', "category")
            newznab_category1.set('value', item.newznab_category1)
            if (item.file_size):
                newznab_size = et.SubElement(xmlitem, "newznab:attr")
                newznab_size.set('name', "size")
                newznab_size.set('value', item.file_size)
            if (item.files):
                newznab_size = et.SubElement(xmlitem, "newznab:attr")
                newznab_size.set('name', "files")
                newznab_size.set('value', item.files)
            if (item.group):
                newznab_size = et.SubElement(xmlitem, "newznab:attr")
                newznab_size.set('name', "group")
                newznab_size.set('value', item.group)
            enclosure = et.SubElement(xmlitem, "enclosure")
            enclosure.set("url", base_url + item.nzb_url)
            enclosure.set("type", "application/x-nzb")
            enclosure.set("length", str(item.length))
        xdec = """<?xml version="1.0" encoding="UTF-8"?>"""
        xml = et.tostring(rss, encoding="utf-8").decode('utf-8')
        xml = xdec + xml
        return xml.encode('utf-8')
