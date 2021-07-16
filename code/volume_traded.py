#Visualizations of volume traded/percentage difference in trading volume week to week

import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def get_vol_traded(stocks_df, stock):
    '''
    This function will create a list, the y coordinates, 
    of the percent change in volume traded for the given stock 
    '''
    perc_change_vol = []
    #perc_change_vol_df = pd.DataFrame(stocks_df.loc[:, 'percent_change_volume_over_last_wk'])
    row_indices = stocks_df.index[stocks_df['stock'] == stock].tolist()
    row_indices = row_indices[1:]
    for i in range(len(row_indices)):
        perc_change_vol.append(stocks_df.at[row_indices[i], 'percent_change_volume_over_last_wk'])
    return perc_change_vol


def plot_vol_traded(stocks_df, stock, save_file=False):
    first_quar_dates_excluding_first = list(stocks_df.loc[1:11, 'date'])
    second_quar_dates = list(stocks_df.loc[360:372, 'date'])
    dates_excluding_first = first_quar_dates_excluding_first + second_quar_dates
    
    figure(figsize=(25, 12))
    vol_traded = get_vol_traded(stocks_df, stock)
    plt.plot(dates_excluding_first, vol_traded, label = stock)
    plt.legend()
    plt.xlabel('Dates')
    plt.ylabel('Percent Change')
    plt.title('Percent Change in Volume Traded by Week')
    if save_file:
        plt.savefig('./visualizations/vol_traded_' + stock + '.png')
    return plt    


if __name__ == '__main__':
    stocks_df =  pd.read_csv('./final_project.csv')
    stock_list = np.sort(np.unique(stocks_df.stock.values))
    
    # By default generate charts for the first 3 stocks
    default_stocks = stock_list[:3]
    
    # Use stock names from command line arguments, if passed
    arg_stocks = sys.argv[1:]
    
    stocks_to_display = default_stocks if len(arg_stocks) == 0 else arg_stocks
    for stock in stocks_to_display:
        plot_vol_traded(stocks_df, stock, True)