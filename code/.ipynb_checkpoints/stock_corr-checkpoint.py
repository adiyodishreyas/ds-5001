import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df_dow = pd.read_csv('./final_project.csv')

def generate_correlation_data():
    # Pivoting the dataframe
    df_date_stock_pctchg = df_dow.pivot('date', 'stock', 'percent_change_price').reset_index()
    # Calculating correlation
    df_corr = df_date_stock_pctchg.corr(method='pearson')
    # Save to csv
    df_corr.to_csv('./dow_jones_stock_correlation.csv')

# Run this command to generate correlation data  
# generate_correlation_data()


stock_list = df_dow["stock"].unique()
num_stock = len(stock_list)
pctchg_dict = {}
for each in stock_list:
    pctchg_dict[each] = df_dow.loc[df_dow['stock'] == each]['percent_change_price'].values
# Overall correlation
df_corr = pd.read_csv('./dow_jones_stock_correlation.csv')
df_corr = df_corr.set_index('stock', drop=True).rename_axis(None)
mask = np.zeros_like(df_corr)
mask[np.triu_indices_from(mask)] = True

df_corr_masked = df_corr.mask(mask.astype(bool))
df_corr_unique = df_corr_masked.unstack().dropna().sort_values()


def plot_corr(stock_1, stock_2, save_file=False):
    corrceof_1_2 = df_corr_unique[df_corr_unique.index == (stock_1, stock_2)]
    corrceof_2_1 = df_corr_unique[df_corr_unique.index == (stock_2, stock_1)]   
    if len(corrceof_1_2) or len(corrceof_2_1):
        corrcoef = corrceof_1_2[0] if len(corrceof_1_2) else corrceof_2_1[0]
    else:
        return plt
    
    # Extract weekly percentage change
    stock_1_pctchg = pctchg_dict[stock_1]
    stock_2_pctchg = pctchg_dict[stock_2]
    # Plot the change
    fig, ax = plt.subplots(2, 2, figsize=(10, 10), sharex='col', sharey='row',
                           gridspec_kw={'width_ratios': [7, 1],
                                        'height_ratios': [1, 7],
                                        'wspace': 0.0, 'hspace': 0.0})
    # Histogram of daily return
    ax[0][0].hist(stock_1_pctchg)
    ax[0][0].set_yticklabels([])
    ax[1][1].hist(stock_2_pctchg, orientation='horizontal')
    ax[1][1].set_xticklabels([])
    # Empty square
    ax[0][1].axis('off')
    # Correlation plot
    ax[1][0].plot(stock_1_pctchg, stock_2_pctchg, 'bo', 
                  label='R = %.2f' % corrcoef)
    ax[1][0].set_xlabel(stock_1, fontsize=24)
    ax[1][0].set_ylabel(stock_2, fontsize=24)
    ax[1][0].legend(fontsize=24)
    ax[1][0].tick_params(axis='both', which='major', labelsize=20)
    if save_file:
        fig.savefig('./visualizations/' + stock_1 + '_' + stock_2 + '_corr.png', 
                dpi=300)
        plt.close(fig)
    return plt



def plot_overall_corr(save_file=False):
    plt.figure(figsize=(12, 10))
    sns.heatmap(df_corr, cmap='RdYlGn', vmax=1.0, vmin=-1.0, mask=mask,
            linewidths=2.5, xticklabels=df_corr.columns,
            yticklabels=df_corr.columns)
    if save_file:
        plt.savefig('./visualizations/dow_corr.png', dpi=300, bbox_inches='tight', pad_inches=0)

# 3 most positively correlated stocks
def plot_top_3_correlated_stocks(save_file):
    for idx, corr in df_corr_unique.tail(3).items():
        plot_corr(idx[0], idx[1], save_file)
        
        
if __name__ == '__main__':
    plot_overall_corr(True)
    plot_top_3_correlated_stocks(True)