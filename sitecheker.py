#!/usr/local/bin/python3.3
# -*- coding: utf-8 -*-
import datetime
import sys
import collections
import os
from tools import Site, Cache, Difference, StatusINI, Twitter, Config

twitter = Twitter()
config = Config()
site = Site()
all_project_names = site.get_all_project_names()
cache = Cache()
difference = Difference()
status_ini = StatusINI()
sites_status_dict = collections.defaultdict(dict)

print('console')

try:
    log = open('log', 'a', encoding = 'utf-8')
    log_date = '{0}\n'.format(datetime.datetime.now())
    log.write('\n')
    log.write('-'*20)
    log.write('\n')
    log.write(log_date)
except:
    log = open('log', 'w', encoding = 'utf-8')
    log_date = '{0}\n'.format(datetime.datetime.now())
    log.write(log_date)
    sys.exit()


for project_name in all_project_names:
    if site.is_it_first_load_of_project(project_name) == True:
        os.mkdir('cache', 0o777)
        site.make_default_status_ini_for_site(project_name)
        status_ini.get_and_write_site_status(project_name)
        log.write(project_name)
        log.write(site.get_status_code_of_site(project_name))
        cache.make_site_cache(project_name)
        break
    else:
        continue

sms_msg = ''

for project_name in all_project_names:
    twitter_msg = ''
    twitter_msg += '[{0}]: \n'.format(project_name)

    # site_status
    try:
        site_status = site.get_status_code_of_site(project_name)
        twitter_msg += 'site_status={0}\n'.format(site_status)
    except:
        continue


    # href_counting
    try:
        href_counting = site.get_bool_parametr_from_projects_cfg(project_name, 'href_counting')
        if href_counting == True:
            hrefs_on_site = site.how_much_hrefs_on_site(project_name)
            print('hrefs_on_site', href_counting)
            hrefs_in_cahe = cache.how_much_hrefs_in_cache(project_name)
            print('hrefs_in_cahe', href_counting)
            if hrefs_on_site != hrefs_in_cahe:
                twitter_msg += 'href_counting=notOK\n'
            else:
                twitter_msg += 'href_counting=OK\n'
    except:
        continue


    # hrefs_different
    try:
        hrefs_different = site.get_bool_parametr_from_projects_cfg(project_name, 'hrefs_different')
        new_hrefs_on_site = difference.find_new_hrefs_on_site(project_name)
        if new_hrefs_on_site != []:
            twitter_msg += 'hrefs_different=notOK\n'
        else:
                twitter_msg += 'hrefs_different=OK\n'
    except:
        continue


    
    # different_rows
    try:
        different_rows = site.get_bool_parametr_from_projects_cfg(project_name, 'different_rows')
        if different_rows == True:
            difference.chek_site_for_row_difference_and_write_to_status_ini(project_name)
            if site.get_parametr_from_status_ini(project_name, 'different_rows') != []:
                different_rows_list = difference.row_difference_to_list(project_name)
                print('different_rows_list', different_rows_list)
                twitter_msg += 'different_rows=notOK\n'.format()
                twitter_msg += '{0}\n'.format(different_rows_list)
            else:
                twitter_msg += 'different_rows=OK\n'
    except:
        continue

    # logging
    log_msg = twitter_msg
    log.write(twitter_msg)




