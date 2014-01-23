#!/usr/local/bin/python3.3
# -*- coding: utf-8 -*-
import datetime
import collections
import os
import sys
from tools import Site, Cache, Difference, Twitter, Config

twitter = Twitter()
config = Config()
site = Site()
all_project_names = site.get_all_project_names()
cache = Cache()
difference = Difference()
sites_status_dict = collections.defaultdict(dict)

print('console')

# определяем первый это запуск скрипта или нет
try:
    # не первый запуск
    log = open('logs/main_log', 'r', encoding='utf-8')
    log = open('logs/main_log', 'a', encoding='utf-8')
    log_date = '{0}\n\n'.format(datetime.datetime.now())
    log.write('\n')
    log.write('-' * 20)
    log.write('\n')
    log.write(log_date)
except:
    # первый запуск
    os.mkdir('logs', 0o777)
    log = open('logs/main_log', 'w', encoding='utf-8')
    log.write('\n')
    log.write('-' * 20)
    log.write('\n')
    log_date = '{0}\n\n'.format(datetime.datetime.now())
    log.write(log_date)

# елси папки cache нет, создает ее
try:
    os.mkdir('cache', 0o777)
except:
    pass

for project_name in all_project_names:
    log_msg = ''
    # если это первый запуск для сайта, то только создает кэш
    if site.is_it_first_load_of_project(project_name) == True:
        cache.make_site_cache(project_name)
        log_msg += '[{0}]: \n'.format(project_name)
        log_msg += 'first start of project\n\n'
        log.write(log_msg)
    else:
        log_msg += '[{0}]: \n'.format(project_name)
        # site_status
        try:
            site_status = site.get_status_code_of_site(project_name)
            log_msg += 'site_status={0}\n'.format(site_status)
        except:
            continue

        # href_counting
        try:
            href_counting = site.get_bool_parametr_from_projects_cfg(project_name, 'href_counting')
            if href_counting == True:
                hrefs_on_site = site.how_much_hrefs_on_site(project_name)
                hrefs_in_cahe = cache.how_much_hrefs_in_cache(project_name)
                if hrefs_on_site != hrefs_in_cahe:
                    log_msg += 'href_counting=notOK\n'
                else:
                    log_msg += 'href_counting=OK\n'
        except:
            continue

        # hrefs_different
        try:
            hrefs_different = site.get_bool_parametr_from_projects_cfg(project_name, 'hrefs_different')
            new_hrefs_on_site = difference.find_new_hrefs_on_site(project_name)
            if new_hrefs_on_site != []:
                log_msg += 'hrefs_different=notOK\n'
            else:
                    log_msg += 'hrefs_different=OK\n'
        except:
            continue

        # different_rows
        try:
            different_rows = site.get_bool_parametr_from_projects_cfg(project_name, 'different_rows')
            if different_rows == True:
                different_rows_list = difference.row_difference_to_list(project_name)
                if different_rows_list != []:
                    log_msg += 'different_rows=notOK\n'.format()
                    log_msg += '{0}\n'.format(different_rows_list)
                else:
                    log_msg += 'different_rows=OK\n'
        except:
            continue
        # logging
        log_msg = log_msg
        log.write(log_msg)
        log.write('\n\n')

log.close()
sys.exit()
