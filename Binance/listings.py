import sys
import time
import re
import urllib.request as urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
from dateutil import parser

class BinanceListings():

    def __init__(self):
        # Binance webpage with different types of announcements
        self.base_url = 'https://www.binance.com'
        self.chrome_ser = Service('C:\Program Files\Google\Chrome Beta\Application\chromedriver.exe')
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("prefs", {"profile.default_content_setting.cookies": 2})
        self.cc_listings = dict()
        self.future_releasedate = True

    # Scrape Binance announcements webpage and return the url for 'New Cryptocurreny Listing'
    def url_new_cc_listings(self):
        page = urllib2.urlopen(f'{self.base_url}/en/support/announcement/')

        binance_ann = BeautifulSoup(page, 'html.parser')
        
        # Find element with child div containing our wanted title
        cc_listing = binance_ann.find('div', attrs=dict(title="New Cryptocurrency Listing"))
        
        # Find the parent (anchor) element which will contain the url
        cc_listing_href = cc_listing.find_parent('a')["href"]

        print(f'Webpage for New Cryptocurrency Listing: {cc_listing_href}')

        return cc_listing_href

    # Iterate over each page in New CC Listing until a release date is older than or equal to now
    # Return a dictionary of newly found cryptocurrency pair releases and their release dates
    def future_cc_listing_releases(self):
        self.driver = webdriver.Chrome(service=self.chrome_ser, options=self.options)
        self.driver.get(self.url_new_cc_listings())
        try:
            self.driver.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]').click()
        except Exception as e:
            pass
        
        cur_releases_page = self.driver.current_url
        self.scrape_cc_releases_page(self.driver.page_source)
        while self.future_releasedate:
            self.driver.get(cur_releases_page)
            self.driver.find_element(By.XPATH, '//*[@id="__APP"]/div/div/main/div[1]/div[2]/section/div[2]/div[2]/button[7]/svg').click()
            cur_releases_page = self.driver.current_url
            self.scrape_cc_releases_page(self.driver.page_source)
        self.close()
        return self.cc_listings

    def scrape_cc_releases_page(self, cur_listings_source):
        new_cc_listings = self.format_cc_releases(cur_listings_source)
        
        accepted_listings = dict()
        for href, cc_vals in new_cc_listings.items():
            if  cc_vals['release_date'] <= datetime.datetime.now(datetime.timezone.utc):
                self.future_releasedate = False
                break
            else:
                accepted_listings[href] = cc_vals
        self.cc_listings.update(accepted_listings)

    def format_cc_releases(self, source):
        cc_listings_page = BeautifulSoup(source, 'html.parser')
        
        cc_listings_links = dict()
        for cc_release in cc_listings_page.findAll('div', class_='css-k5e9j4'):
            cc_listings_links[f'{self.base_url}{cc_release.find("a").get("href")}'] = cc_release.text

        return self.filter_announcements(cc_listings_links)

    def filter_announcements(self, links):
        filtered_releases = dict()

        for href, announcement in links.items():
            if re.match("(Binance Adds .* Trading Pairs)|(Binance Will List .* in the Innovation Zone.*)", announcement):
                filtered_releases[href] = self.scrape_tokens_and_release(href)
        
        return filtered_releases

    def scrape_tokens_and_release(self, href):
        self.driver.get(href)
        try:
            self.driver.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]').click()
        except Exception as e:
            pass

        tokens_elem = self.driver.find_element(By.XPATH, '//*[@id="__APP"]/div/div/main/div/div[2]/div[2]/div[2]/article/div[2]/article/div[2]')
        tokens_rel = re.findall('[A-Z]+\/[A-Z]+', tokens_elem.text)
        timestamp_str = re.findall('\d{4}\-\d{2}-\d{2} \d{2}:\d{2} \(\w+\)', tokens_elem.text)[0]
        timestamp = parser.parse(re.sub('[()]', '', timestamp_str))

        return dict(release_date=timestamp, tokens=tokens_rel)

    def close(self):
        self.driver.close()
        self.future_releasedate = True
