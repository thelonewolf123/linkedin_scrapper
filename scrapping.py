#!/usr/bin/python3

import sys
import os
import pandas as pd
import re
import requests
import json

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from time import sleep, perf_counter


class LinkedIn:

    def __init__(self, browser, username, passwd, group):
        self.browser    = browser
        self.username   = username
        self.passwd     = passwd
        self.group      = group
        self.members    = []
        self.profession = []
        self.profiles   = []
        self.login()
        self.group_ctrl()
        self.scraper_ctrl()

    def login(self):
        userfiled   = browser.find_element_by_id('username')
        passfield   = browser.find_element_by_id('password')
        submit_form = browser.find_element_by_class_name(
            'login__form_action_container')
        userfiled.send_keys(self.username)
        passfield.send_keys(self.passwd)
        submit_form.click()

    # profile class - ui-entity-action-row__link

    def link_scraper(self, html):
        soup     = BeautifulSoup(html, 'html.parser')
        data_ref = soup.find_all(
            'a', attrs={'class': 'ui-entity-action-row__link'}, href=True)
        raw_data = []
        for data in data_ref:
            raw_data.append('https://www.linkedin.com'+data['href'])
        return raw_data

    def group_ctrl(self):
        self.browser.get(self.group)
        members_count = int(
            browser.find_element_by_class_name('t-24').get_attribute('innerText')[:-8].replace(',', ''))

        while members_count != len(self.profession):
        # for _ in range(0,50):
            browser.find_element_by_tag_name('body').send_keys(Keys.END)
            browser.find_element_by_tag_name('body').send_keys(Keys.DOWN)
            sleep(2)
            self.scraper_ctrl()
            print(self.members,self.profession,self.profiles)
            print('Total Fetched profiles -> ',len(self.profession))
        self.write_data()

    def write_data(self):
        linkedin_data = {
            'Name': self.members,
            'Profession': self.profession,
            'LinkedIn Url': self.profiles
        }

        df  = pd.DataFrame(linkedin_data)
        writer = pd.ExcelWriter('linkedin_data.xlsx')
        df.to_excel(writer, index = False)
        writer.save()

    def scraper_ctrl(self):
        members_list    = self.browser.find_element_by_class_name('groups-members-list')
        members_html    = members_list.get_attribute('innerHTML')

        self.members    = self.scrapper(members_html, 'artdeco-entity-lockup__title')
        self.profession = self.scrapper(members_html, 'artdeco-entity-lockup__subtitle')
        self.profiles   = self.link_scraper(members_html)

    def scrapper(self, html, attribute):
        soup     = BeautifulSoup(html, 'html.parser')
        data_div = soup.find_all('div', attrs={'class': attribute})
        raw_data = []
        for data in data_div:
            raw_data.append(data.getText().split('\n')[0].strip())
        return raw_data

    def get_email(self):
        pass


if __name__ == "__main__":

    t1 = perf_counter()

    try:
        chrome_options = Options()      
        chrome_options.add_argument("--headless")  
        browser = webdriver.Chrome(chrome_options=chrome_options)
        config_file = open('config.py','r')
        config = json.loads(config_file.read())
        config_file.close()
        url         = config['URL']
        group_url   = config['GROUP_URL']
        mail_id     = config['EMAIL_ID']
        password    = config['PASSWORD']
        browser.get(url)
        LinkedIn(browser, mail_id, password, group_url)
    except Exception as e:
        print(str(e))
    finally:
        browser.quit()
        t2 = perf_counter()
        performance = t2-t1
        print('Performance -> ',performance)