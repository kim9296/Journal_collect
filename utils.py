import logging
from selenium import webdriver
import argparse

Months = {
    'January'   : '01',
    'February'  : '02',
    'March'     : '03',
    'April'     : '04',
    'May'       : '05',
    'June'      : '06',
    'July'      : '07',
    'August'    : '08',
    'September' : '09',
    'October'   : '10',
    'November'  : '11',
    'December'  : '12'
}

def getlog():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter=logging.Formatter('%(asctime)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def getdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('/Users/hyunjinkim/utils/chromedriver', chrome_options=options)
    driver.implicitly_wait(3)
    return driver

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ( 'yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')