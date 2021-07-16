# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 08:28:20 2021

@author: crjol
"""

import pandas as pd
import matplotlib.pyplot as plt

#df = pd.read_csv("dow_jones_index.data")
#df.to_csv('final_project.csv')

data = pd.read_csv('final_project.csv')

stocks = {'3M':'MMM',
          'American Express':'AXP',
          'Alcoa':'AA',
          'AT&T':'T',
          'Bank of America':'BAC',
          'Boeing':'BA',
          'Caterpillar':'CAT',
          'Chevron':'CVX',
          'Cisco Systems':'CSCO',
          'Coca-Cola':'KO',
          'DuPont':'DD',
          'ExxonMobil':'XOM',
          'General Electric':'GE',
          'Hewlett-Packard':'HPQ',
          'The Home Depot':'HD',
          'Intel':'INTC',
          'IBM':'IBM',
          'Johnson & Johnson':'JNJ',
          'JPMorgan Chase':'JPM',
          'Kraft':'KRFT',
          "McDonald's":'MCD',
          'Merck':'MRK',
          'Microsoft':'MSFT',
          'Pfizer':'PFE',
          'Procter & Gamble':'PG',
          'Travelers':'TRV',
          'United Technologies':'UTX',
          'Verizon':'VZ',
          'Wal-Mart':'WMT',
          'Walt Disney':'DIS'}

def avg_return_next_dividend(x):
    '''
    Parameters
    ----------
    x : string
        stock symbol for a stock in the 2011 Dow Jones Index.

    Returns
    -------
    avg : float
        average percentage of return on the next dividend.
    '''
    total = 0
    count = 0
    
    for i in range(len(data['stock'])):
        if data['stock'][i] == x:
            total += data['percent_return_next_dividend'][i]
            count += 1
            
    avg = total/count
    return avg


def plot_avg_returns():
    avg_returns = {}

    for key, val in stocks.items():
        avg_return = avg_return_next_dividend(val)
        avg_returns[key] = avg_return

    avg_returns_df = pd.DataFrame.from_dict(avg_returns, orient = 'index')
    avg_returns_df.columns = ['Average Percent Return']
    avg_returns_df = avg_returns_df.sort_values('Average Percent Return')

    avg_returns_df.plot.bar(ylabel = 'Average Percent Return', legend = False)