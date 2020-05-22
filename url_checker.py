import urllib
import urllib.request
import csv
import sys
import time
from datetime import date
import os
import pathlib

clear = lambda: os.system('cls')
clear()

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

dscr ="Simple tester d'URL "
version = "# Version : 0.1"
auteur ="# Auteur : Abdou Khadre D. GAYE"
date_creation="# Date : 22/05/2020"
print(dscr.center(45),"\n","\n",version,"\n",auteur,"\n",date_creation,"\n")


sleeptime=2
today=date.today()
file=pathlib.Path('urls.txt')

if file.exists ():
    f = open(file, 'r')
    count = f.readlines()
else:
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



bad_urls = csv.writer(open('bad_urls.csv', 'w'))
bad_urls.writerow(['URL', 'Response', 'Date :', today])

good_urls = csv.writer(open('good_urls.csv', 'w'))
good_urls.writerow(['URL', 'Response', 'Date :', today])


count = 0
good_url = 0
bad_url = 0


with open(file, 'r') as urls:
 for r in urls:
    count += 1
    time.sleep(sleeptime)
    print("\n")
    try:
        r = urllib.request.urlopen(r.strip())
        rc = r.getcode()
        rmsg = r.msg
        
        print([count],"Traitement : ", r.url ,"\n[RC] Response : ",rc)
        if rc == 200:
            good_url += 1
            good_urls.writerow([r.url, rc])
            color = GREEN
        else:
            bad_url += 1
            color=RED
            continue
    except urllib.error.URLError as e:              
        print(e.reason)
        

def recap():
    print(color+"\nBons URLs  (200 OK):"+ENDC,[good_url],"\n---", RED+"\nMauvaises URLs :"+ENDC,[bad_url],"\n---", "\nTotal URLs :",[count],"\n")

recap() 