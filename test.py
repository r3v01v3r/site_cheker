import collections
import time
import os
from tools import Site, Cache, Difference, StatusINI, Twitter, SiteChekerCFG

twitter = Twitter()
site_cheker_cfg = SiteChekerCFG()
site = Site()
all_project_names = site.get_all_project_names()
cache = Cache()
difference = Difference()
status_ini = StatusINI()
sites_status_dict = collections.defaultdict(dict)
report = 0

print(site_cheker_cfg.get_setting_of_sitecheker('delta time'))



