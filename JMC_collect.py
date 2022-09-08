from ast import arg
from lib2to3.pgen2 import driver
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from argparse import ArgumentParser
from utils import getdriver, getlog, str2bool

parser = ArgumentParser(description = 'Collect JMC')
parser.add_argument('--issue',  help='issue',      dest='issue',  required=True)
parser.add_argument('--vol',    help='vol',        dest='vol',    required=True)
parser.add_argument('--update', help='is update?', dest='update', default=True, type=str2bool)

def GetInfo(issue, vol, driver, driver, logger, start):
    driver.get(f'https://pubs.acs.org/toc/jmcmar/{issue}/{vol}')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    res = list()
    if start:
        pass 
        #TODO

    for i in range(100):
        try:
            title = soup.select(f'#pb-page-content > div > main > div:nth-child(3) > div > div:nth-child({i}) > div.issue-item_metadata > span > h5 > a')
            abstract = soup.select(f'#pb-page-content > div > main > div:nth-child(3) > div > div:nth-child({i}) > div.issue-item_metadata > div.issue-item_footer > div > div > span > p') 
            res.append({'title': title[0].text, 'issue' : issue, 'vol' : vol, 'abstract' : abstract[0].text, 'doi' : title[0].get('id')})
        except:
            if len(title) != 0:
                if title[0].text == 'Issue Editorial Masthead':
                    break
    logger.info('{}, {}, {}'.format(issue, vol, len(res)))

    time.sleep(5)
    return res

def main(iss_l, vol_l, iss_b, vol_b, is_update):          
      
    total_res = list()
    driver = getdriver()
    logger = getlog()
    if iss_l == iss_b:
        if vol_l == vol_b:
            raise Exception ('updated already')
        else:
            shows = sorted(set(zip([iss_l] * (vol_l - vol_b) , range(vol_l, vol_b, -1))), reverse=True)
    else:
        shows = list()
        if vol_b == 24:
            for iss in range(iss_l, iss_b, -1):
                if iss == iss_l:
                    shows += sorted(set(zip([iss_l] * vol_l , range(vol_l, 0, -1))), reverse=True)
                else:
                    shows += sorted(set(zip([iss] * 24 , range(24, 0, -1))), reverse=True)
        else:
            for iss in range(iss_l, iss_b - 1, -1):
                if iss == iss_l:
                    shows += sorted(set(zip([iss_l] * vol_l , range(vol_l, 0, -1))), reverse=True)
                elif iss == iss_b:
                    shows += sorted(set(zip([iss_b] * (24 - vol_b) , range(24, vol_b, -1))), reverse=True)
                else:
                    shows += sorted(set(zip([iss] * 24 , range(24, 0, -1))), reverse=True)
    
    start = True
    for issue, vol in shows:
        total_res += GetInfo(issue, vol, driver, logger, start)
        start = False

    if is_update:
        csv = [x for x in os.listdir('.') if 'JMC_' in x][0]
        df = pd.read_csv(csv)
    else:
        pd.DataFrame(res).to_csv('JMC_201001to202208.csv', index = False)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.update:
        with open('JMC.json', 'r') as f:
            temp = json.load(f)
            iss_b = temp['issue']
            vol_b = temp['vol']
        f.close()
    else:
        iss_b = 52,
        vol_b = 1
    main(args.issue, args.vol, iss_b, vol_b, args.update)