import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import pandas as pd
import datetime

def temp_extraction(text):

    re_temp = re.compile('([0-9]{1,2}\.[0-9])(-?[0-9]{1,2}\.[0-9])')
    if re.search(re_temp,text):
        return np.float(re.search(re_temp,text)[2])
    else:
        return np.nan

def rain_extraction(text):

    re_rain = re.compile('([0-9]{1,2}\.[0-9])(mm)')
    if re.search(re_rain,text):
        return np.float(re.search(re_rain,text)[1])
    else:
        return np.nan

def day_extrator(text):

    if re.search(re.compile('(di|che)\s([0-9]{1,2})$'), text):
        return int(re.search(re.compile('(di|che)\s([0-9]{1,2})$'), text)[2])

def data_to_url(year, month, day, t_min, t_max, rain):

    df = pd.DataFrame({
        'year':year,
        'month':month,
        'day':day,
        't_min':t_min,
        't_max':t_max,
        'rain':rain
    }, index=[datetime.date(year, month, day)]
    )
    return df

def make_the_soup(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def month_name(month):

    month_dict = {
            'janvier':1, 'fevrier':2, 'mars':3, 'avril':4, 'mai':5, 'juin':6, 'juillet':7, 'aout':8, 'septembre':9,
            'octobre':10, 'novembre':11, 'decembre':12
        }
    month_list = [
        'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre',
    'octobre', 'novembre', 'decembre'
    ]

    if type(month)==str:
        return(month_dict[month])

    if type(month)==int:
        return(month_list[month-1])


def monthly_data(year, month, main_url):

    df_data = pd.DataFrame(columns=['year', 'month', 'day', 't_min', 't_max', 'rain'])

    url = main_url.format(month_name(month), year)
    soup = make_the_soup(url)

    for tr in soup.find_all('tr'):
        for ch in tr.children:
            try:
                if day_extrator(ch.get_text()):
                    day = day_extrator(ch.get_text())
                    t_min = temp_extraction(ch.next_sibling.get_text())
                    t_max = temp_extraction(ch.next_sibling.next_sibling.get_text())
                    rain = rain_extraction(ch.next_sibling.next_sibling.next_sibling.get_text())
                    df_data = df_data.append(data_to_url(year, month, day, t_min, t_max, rain))
            except:
                pass
    return df_data
