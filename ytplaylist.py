#!/bin/env python

# WARNING: THIS SCRIPT MAY VIOLATE YOUTUBE'S TOS AND IS AN OPTIONAL, AT YOUR OWN RISK MODULE FOR THE ORIGINAL PROGRAM. BY USING THIS CODE YOU ARE STILL SUBJECT TO THE TERMS OF THE GPL v2.0 Source Code License

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from urllib.request import Request, urlopen
from urllib import error

# LOCAL
#from Downloader import Downloader

import requests
import sys
import subprocess
import argparse

DRIVER_WAIT_TIME = 10

class YTPlaylist:

	@staticmethod
	def __getWebElem(driver, xpath, wait=DRIVER_WAIT_TIME):
		try:
			element = WebDriverWait(driver, DRIVER_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, xpath)))
			return element
		except TimeoutException:
			print("ERROR: Timeout Exception")
		except StaleElementReferenceException:
			print("ERROR: StaleElementReferenceException")

		return False


	@staticmethod
	def fetchPlaylist(playlistID):
		link = "https://www.youtube.com/playlist?list=" + playlistID
		songs = None

		driver = webdriver.PhantomJS()
		driver.set_window_size(1120, 550)
		driver.get(link)

		elemExists = YTPlaylist.__getWebElem(driver, "//tr[contains(@class,'pl-video')]") 
		elements = driver.find_elements_by_xpath("//tr[contains(@class,'pl-video')]")
		if not elemExists:
			print("No pl-video on page")
			driver.save_screenshot('screen.png')
		if elements:
			songs = dict()
			songs['items'] = list()
			for item in elements:
				snip = dict()
				snip['snippet'] = dict()
				snip['snippet']['title'] = item.get_attribute('data-title')
				snip['snippet']['resourceId'] = dict()
				snip['snippet']['resourceId']['videoId'] = item.get_attribute('data-video-id')
				songs['items'].append(snip)
		else:
			print("No Element")
		
		driver.quit()
		return songs
