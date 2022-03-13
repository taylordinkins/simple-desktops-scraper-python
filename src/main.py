import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import pandas as pd
import argparse

from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('--save_path', help='Sub-directory to save images', default='imgs')
args = parser.parse_args()

curr_dir = os.getcwd()
url_base = "http://simpledesktops.com"
browse_url_base = "http://simpledesktops.com/browse"
save_path = os.path.join(curr_dir, args.save_path)
print("Saving images to {}".format(save_path))

# current number of pages on Simple Desktops
page_nums = np.arange(1, 53)
for num in tqdm(page_nums):
    curr_path = os.path.join(browse_url_base, str(num))
    curr_page = requests.get(curr_path)
    curr_soup = BeautifulSoup(curr_page.content, "html.parser")

    links = curr_soup.findAll('a')
    desktop_links = [link.get('href') for link in links if "desktops" in link.get('href')]
    desktop_links = list(set(desktop_links))
    for f_link in desktop_links:
        link = f_link[1:]
        link_path = os.path.join(url_base, link)
        link_page = requests.get(link_path)
        link_soup = BeautifulSoup(link_page.content, "html.parser")
        img_links = link_soup.findAll('a')

        download_links = [img_link.get('href') for img_link in img_links if "download" in img_link.get('href')]
        download_links = list(set(download_links))
        # this breaks near the end
        assert len(download_links) == 1, "More than one link containing 'download' in path"
        to_download = download_links[0][1:]
        fname = os.path.split(link[:-1])[-1]+'.png'

        img_path = os.path.join(url_base, to_download)
        img_request = requests.get(img_path)
        if img_request.status_code == 200:
            with open(os.path.join(save_path, fname), 'wb') as f:
                f.write(img_request.content)
