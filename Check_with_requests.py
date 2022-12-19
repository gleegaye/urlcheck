# -*- coding: utf-8 -*-
import urllib3, urllib.request
import concurrent.futures
import urllib.request
import os, sys, pathlib
from os import name, system
from datetime import date,datetime
import time
from time import sleep
import requests
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import csv


# disable warnings
urllib3.disable_warnings()

# Remove all whitespace in file
# ^(\s)*$\n

# nettoyer le terminal
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')
clear()


start_time = datetime.now()
# start = time.time()
today=start_time.strftime("%d/%m/%Y %H:%M:%S")


dscr ="Simple URL Tester"
version = "# Version Script : 0.2"
requis ="# Prerequis: Python3"
auteur ="# Auteur : Djily GAYE"
equipe = "# Equipe: XXXX"
date_execution = "# Date execution : {}".format(today)
print(dscr.center(45),"\n","\n",version,"\n",equipe,"\n",date_execution,"\n", requis,"\n")

# filename = str(input("Entrez le nom le du fichier contenant les URLs : "))
filename = "URLs.txt"

# le script et le fichier urls.txt doivent etre dans le meme dossier
DIR=os.path.dirname(__file__)
file=os.path.join(os.path.dirname(__file__), filename)

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

try:
    f = open(file, 'r')
    count = f.readlines()
    if len(count) == 0 :
        color=RED
        print(color+"Le fichier URL",file," est vide !"+ENDC)
        file_status = sys.exit()
    else:
        color=GREEN
        file_status = color+"[OK]"+ENDC
except:
    color=RED
    print(color+"Le fichier URL",file," n'existe pas !"+ENDC)
    file_status = sys.exit()

line = '----'
print(line[0]*70,)
print ("| Nombre d'URL  :",len(count),'|','Date :', today,"| Status fichier URL :",file_status, "|")
print(line[0] * 70)


filename = "tt.txt"
# le script et le fichier urls.txt doivent etre dans le meme dossier
DIR=os.path.dirname(__file__)

report = os.path.join(os.path.dirname(__file__), 'report_'+start_time.strftime("%d-%m-%Y_%H-%M")+'.csv')
report = csv.writer(open(report, 'w'))
report.writerow(['URL', 'Response', ' ViaBack', 'Via', 'Date'])


def load_url(url, timeout):
    chaineAcces,ViaBack, Via,rc,rep = "","","","",""
    try:
        url=url.strip()
        with requests.get(url,  timeout=timeout, verify=False, allow_redirects=True) as r:
            rc = r.status_code
            head = dict(r.headers)
            rep = r.reason
            # on recupere toute la chaine d'acces
            for k, v in head.items():
                if k == "ViaBack":
                    ViaBack = k + " " +v
                if  k == "Via":
                    Via = k + " " +v
            if  rc==200 or rc<=404:
                chaineAcces = ViaBack +"\t"+ Via
                report.writerow([url,rc,ViaBack,Via,today])
            else:
                report.writerow([url,str(rc)+"-"+rep,ViaBack,Via,today])
    except Exception as e:
        report.writerow([url,e,ViaBack,Via,today])
    return rc,rep,chaineAcces


file=os.path.join(os.path.dirname(__file__), filename)
count=0
URLS=[]
good,bad = [],[]
def main():

    with open(file,'r') as f:
        for url in f.readlines():
            url = url.replace('\n','')
            url = url.replace('\x00','')
            if not url.strip():
                continue
            URLS.append(url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
        futures = {executor.submit(load_url, url, 3): url for url in URLS}

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                data = future.result()
            except Exception as e:
                print('{} generated an exception: {}'.format(url, e))
            else:
                if (200 or 404 or 401 or 403 or "OK") in data:
                    print("OK : {},{}".format(url, data))
                    good.append(url)
                else:
                    print("KO: {},{}".format(url, data))
                    bad.append(url)

if __name__ == "__main__":
    if not sys.version_info[0] == 3:
        raise Exception("Please Upgrade or Downgrade your python to python 3.")
    main()

end_time = datetime.now()
duration = end_time - start_time
count = len(URLS)
print("\n\tTotal urls : {}".format(count),GREEN+"\tOK :{}".format(len(good))+ENDC,RED+"\tKO :{}".format(len(bad))+ENDC,"\tDuration : {}".format(duration),"\n")
