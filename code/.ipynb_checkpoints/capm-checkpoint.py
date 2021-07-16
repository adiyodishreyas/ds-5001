# load modules
import numpy as np
import pandas as pd

def calc_stock_beta(index, stock):
    ''' 
    PURPOSE: Given Excess Returns of the stock and index, calculate CAPM beta value for the stock 
    
    INPUT:
    index: excess returns of an index
    stock: excess returns of an stock
    
    OUTPUT:
    beta: float type, the CAPM beta of the stock
    
    '''
    index_T = index.transpose()

    first_part = np.linalg.inv(np.matmul(index_T, index))
    second_part =  np.matmul(index_T, stock)

    beta = np.matmul(first_part, second_part)[0][0]
    return beta


def get_index_percent_change_price(stocks_df):
    stocks_df['open'] = pd.to_numeric(stocks_df['open'].str.replace('$', '', regex=True))
    stocks_df['close'] = pd.to_numeric(stocks_df['close'].str.replace('$', '', regex=True))

    open_price_mean = stocks_df.groupby("date").open.mean()
    close_price_mean = stocks_df.groupby("date").close.mean()

    index_percent_change_price = (close_price_mean - open_price_mean)*100/open_price_mean
    index_percent_change_price_df = pd.DataFrame(data = index_percent_change_price, columns=["percent_change_price"])
    index_percent_change_price_df.rename(columns={'percent_change_price': 'INDEX'}, inplace=True)
    return index_percent_change_price_df

def plot_capm_beta(stocks_df, save_file=False):
    # risk-free Treasury rate
    R_f = 0.0175 / 252
    
    index_percent_change_price_df = get_index_percent_change_price(stocks_df)
    stocks_percent_change_price_df = pd.pivot_table(stocks_df, values="percent_change_price", columns=["stock_name"], index=["date"])
    stocks_with_index_df = pd.merge(stocks_percent_change_price_df, index_percent_change_price_df, on="date", how="inner")
    index_excess_returns = stocks_with_index_df['INDEX'].values - R_f
    
    stock_list = stocks_with_index_df.columns
    beta_df = pd.DataFrame()
    for s in stock_list:
        s_excess_returns = stocks_with_index_df[s].values - R_f
        beta = calc_stock_beta(index_excess_returns.reshape(-1, 1), s_excess_returns.reshape(-1, 1))
        t_df = pd.DataFrame(data=[beta], columns=[s])
        beta_df = pd.concat([beta_df, t_df], axis=1)
    
    beta_df.index = ['Beta']
    ax = beta_df.T.sort_values('Beta').plot.bar(ylabel='CAPM Beta',figsize=(25, 12), legend=False)
    
    if save_file:
        ax.figure.savefig('./visualizations/capm.png')
    return ax
    
    
if __name__ == '__main__':
    stocks_df =  pd.read_csv('./final_project.csv')
    plot_capm_beta(stocks_df, True)