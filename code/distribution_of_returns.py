#Distribution of Returns: Mean, Standard deviation of stock price from the mean, 

import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt

def get_returns(df, stock):
    '''
    This function will create a list, the y coordinates, 
    of the weekly returns for the given stock 
    '''
    first_quar_dates = list(df.loc[:11, 'date'])
    second_quar_dates = list(df.loc[360:372, 'date'])
    dates = first_quar_dates + second_quar_dates
    weekly_returns = []
    weekly_returns_df = pd.DataFrame(df.loc[:, 'percent_change_price'])
    row_indices = df.index[df['stock'] == stock].tolist()
    row_indices = row_indices[:]
    for i in range(len(row_indices)):
        weekly_returns.append(df.at[row_indices[i], 'percent_change_price'])
    return weekly_returns


def plot_returns(df, stock, save_file=False):
    plt.hist(get_returns(df, stock), label = stock)
    plt.legend()
    plt.title('Distribution of Returns')
    plt.xlabel('Return')
    plt.ylabel('Frequency')
    
    if save_file:
        plt.savefig('./visualizations/distribution_of_returns_' + stock + '.png')
        plt.close()
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
        plot_returns(stocks_df, stock, True)