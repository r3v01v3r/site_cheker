import collections
import time
import os
from tools import Site, Cache, Difference, Twitter, Config, LogFile

twitter = Twitter()
site_cheker_cfg = Config()
site = Site()
all_project_names = site.get_all_project_names()
cache = Cache()
difference = Difference()
sites_status_dict = collections.defaultdict(dict)
report = 0


log_file = LogFile()
log_file.write_to_start_of_log('sdsd')
