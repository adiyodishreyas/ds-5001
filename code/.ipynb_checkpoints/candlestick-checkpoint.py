# Command to execute this file:
# python candlestick.py IBM AA CAT
# You can pass a list of stocks to be visualized via command-line arguments

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import sys

def plot_candlestick_chart(stocks_df, stock, save_file=False):
    '''
        PURPOSE: Given the stocks dataframe and the stock, create a candlestick plot
        
        INPUT
        stocks_df pandas dataframe for stock
        stock_name symbol name of the stock 
        
        OUTPUT
        <plot> candlestick plot will be displayed
    '''
    
    #Filter only the stock's data
    stock_df = stocks_df[stocks_df.stock == stock]
    stock_name = stock_df.iloc[0]['stock_name']
    
    #Process the data for candlestick plot
    stock_df_for_candlestick = stock_df.loc[:, ['date', 'open', 'high', 'low', 'close', 'volume']]
    stock_df_for_candlestick.set_index('date', inplace=True)
    stock_df_for_candlestick.index = pd.DatetimeIndex(stock_df_for_candlestick.index)
    stock_df_for_candlestick = stock_df_for_candlestick.replace('[\$,]', '', regex=True).astype(float)
    
    #Styling for the plot
    m_colors = mpf.make_marketcolors(up='g',down='r')
    custom_style  = mpf.make_mpf_style(marketcolors=m_colors)
    stock_title = stock_name + "(" + stock + ")"
    
    #If save_file is true then store a png image in the visualizations folder
    if save_file:
        return mpf.plot(stock_df_for_candlestick, type='candle', volume=True, style=custom_style, title=stock_title, savefig="./visualizations/candlestick_"+stock+".png", figsize=(25, 12))
    else: 
        return mpf.plot(stock_df_for_candlestick, type='candle', volume=True, style=custom_style, title=stock_title, figsize=(25, 12))



if __name__ == '__main__':
    stocks_df =  pd.read_csv('./final_project.csv')
    stock_list = np.sort(np.unique(stocks_df.stock.values))
    
    # By default generate charts for the first 3 stocks
    default_stocks = stock_list[:3]
    
    # Use stock names from command line arguments, if passed
    arg_stocks = sys.argv[1:]
    
    stocks_to_display = default_stocks if len(arg_stocks) == 0 else arg_stocks
    for stock in stocks_to_display:
        plot_candlestick_chart(stocks_df, stock, True)