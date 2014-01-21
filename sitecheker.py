#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
print('console')

for project_name in all_project_names:
    if site.is_it_first_load_of_project(project_name) == True:
        os.mkdir('cache', 0o777)
        site.make_default_status_ini_for_site(project_name)
        status_ini.get_and_write_site_status(project_name)
        cache.make_site_cache(project_name)
    else:
        continue


for project_name in all_project_names:
    if site.get_status_code_of_site(project_name) == 200:
        if status_ini.is_algoritm_status_ON(project_name, 'different rows') == True:
            difference.chek_site_for_row_difference_and_write_to_status_ini(project_name)
            row_difference = site.get_parametr_from_status_ini(project_name, 'different rows')
            if len(row_difference) > 0 and len(row_difference) <= 10:
                msg = site.get_parametr_from_status_ini(project_name, 'different rows')
                msg = ('{0} :: новые строки на сайте >>> {1}'
                          .format(project_name, msg))
                twitter.make_post_to_twitter_from_str(msg)
            if len(row_difference) > 10:
                msg = '{0} Изменилось более 10 строк'.format(project_name)
                twitter.make_post_to_twitter_from_str(msg)

        if status_ini.is_algoritm_status_ON(project_name, 'href status') == True:
            href_status = difference.chek_for_href_count_change(project_name)
            status_ini.write_href_status_to_ini(project_name, href_status)
            if href_status == 'Something wrong':
                new_hrefs_on_site = difference.find_new_hrefs_on_site(project_name)
                msg = '{0}: new links >>> {1}'.format(project_name, new_hrefs_on_site)
                twitter.make_post_to_twitter_from_str(msg)
    else:
        status_ini.get_and_write_site_status(project_name)

for project_name in all_project_names:
    if site.get_status_code_of_site(project_name) == 200:
        cache.get_site_cache(project_name)
    else:
        status_ini.get_and_write_site_status(project_name)

report += 1

if report%10 == 1:
    msg = site.get_status_in_str_off_all_projects()
    twitter.make_post_to_twitter_from_str(msg)

for project_name in all_project_names:
    cache.make_site_cache(project_name)

