# -*- coding: utf-8 -*-

import urllib, urllib.request
import requests
import csv, re
from datetime import date,datetime
from socket import timeout
import time
import os, sys, pathlib
import logging
import threading



# Remove all whitespace in file
# ^(\s)*$\n

#clear = lambda: os.system('clear') # linux
clear = lambda: os.system('cls') # windows
clear()

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

sleeptime=0.5
start_time = datetime.now()
start = time.time()
today=start_time.strftime("%d/%m/%Y %H:%M:%S")

dscr ="Simple URL Tester"
version = "# Version Script : 0.1"
requis ="# Prerequis: Python3"
auteur ="# Auteur : Abdou Khadre D. GAYE"
date_execution = "# Date execution : {}".format(today)
print(dscr.center(45),"\n","\n",version,"\n",auteur,"\n",date_execution,"\n", requis,"\n")

# filename = str(input("Entrez le nom le du fichier avec les URLs : "))

filename = "URL.txt"
# filename = "tst.txt"
# le script et le fichier urls.txt doivent etre dans le meme dossier
DIR=os.path.dirname(__file__)
file=os.path.join(os.path.dirname(__file__), filename)

try:
    f = open(file, 'r')
    count = f.readlines()
except:
    color=RED
    print(color+"Le fichier URL",file," n'existe pas !"+ENDC)
    file_status = sys.exit()

if len(count) == 0 :
    color=RED
    print(color+"Le fichier URL",file," est vide !"+ENDC)
    file_status = sys.exit()
else:
    color=GREEN
    file_status = color+"[OK]"+ENDC

line = '----'
print(line[0]*70,)
print ("| Nombre d'URL  :",len(count),'|','Date :', today,"| Status fichier URL :",file_status, "|")
print(line[0] * 70)



good_file = os.path.join(os.path.dirname(__file__), 'good_urls_'+start_time.strftime("%d-%m-%Y_%H-%M")+'.csv')
bad_file = os.path.join(os.path.dirname(__file__), 'bad_urls_'+start_time.strftime("%d-%m-%Y_%H-%M")+'.csv')
# Initialisation
bad_file = csv.writer(open(bad_file, 'w'))
bad_file.writerow(['URL', 'Raison', 'Date'])

good_file = csv.writer(open(good_file, 'w'))
good_file.writerow(['URL', 'CodeResponse', 'SFRViaBack', 'SFRVia', 'Date'])



threads = []
# headers = []

def checker():
    global SFRVia, SFRViaBack, chaineAcces

    count = 0
    good_url = 0
    bad_url = 0
    color1 = GREEN
    color2 = RED

    with open(file,"r") as f:
        for url in f.readlines():
            if not url.strip():
                continue
            if url:
                url = url.replace('\n','')
                # time.sleep(sleeptime)
                print("\n")
                count += 1
            try:
                r = requests.get(url, timeout=10, verify=False, allow_redirects=True)
                rc = r.status_code
                head = r.headers
                rep = r.reason
                if  rc==200 or rc<=404:

                    print([count],"Traitement : ", url ,"\n[CR] Code : ",rc, "\n[-] Header :", head, "\n")
                    good_url += 1
                    good_file.writerow([url,rc,SFRViaBack,SFRVia,today])
                else:
                    print([count],"Traitement : ", url ,"\n[CR] Code : ",rc,"\n[-] Response : ",rep, "\n")
                    bad_url += 1
                    bad_file.writerow([url,str(rc)+"-"+rep,today])
            except Exception as e:
                print([count]," URL : ", url.replace('\n',''), "\n[CR] Response : ", e)
                bad_url += 1
                bad_file.writerow([url,e,today])
        end_time = datetime.now()
        duree = end_time - start_time
        print("\n********************************"+color1+"\nBons URL  (200-404 OK):"+ENDC,[good_url],"\n--------------------------------", color2+"\nMauvaises URL :"+ENDC,[bad_url],"\n--------------------------------", "\nTotal URL :",[count],"\tDUREE: {} ".format(duree),"\n--------------------------------\n""********************************")

t = threading.Thread(target=checker)
threads.append(t)
t.start()

