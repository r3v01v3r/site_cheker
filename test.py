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

l = site.find_all_hrefs_on_site('rdx')
old = cache.find_all_hrefs_in_cache('rdx')

diff = difference.find_new_hrefs_on_site('rdx')
print(diff)
