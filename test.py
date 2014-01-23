import collections
import time
import os
from tools import Site, Cache, Difference, Twitter, Config

twitter = Twitter()
site_cheker_cfg = Config()
site = Site()
all_project_names = site.get_all_project_names()
cache = Cache()
difference = Difference()
sites_status_dict = collections.defaultdict(dict)
report = 0


file = open('logs/main_log.html', 'r', encoding='utf-8')
print(file.read())
