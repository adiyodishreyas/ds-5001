import pandas as pd
import unittest
from dividend_history import avg_return_next_dividend, create_dividend_dict
from capm import calc_stock_beta


class DividendTestSuite(unittest.TestCase):
    
    unittest_data = pd.read_csv('./test_data/dividend_unit_test_data.csv')
    
    test_names = {'American Express':'AXP',
          'Alcoa':'AA',
          'Bank of America':'BAC',
          'Boeing':'BA'}
    
    def test_avg_return_next_div(self):
        expected = 0.609470106
        self.assertEqual(avg_return_next_dividend(DividendTestSuite.unittest_data, 'AA'), expected)
    
    def test_create_dividend_dict(self):
        expected = {'American Express':0.361802557, 'Alcoa':0.609470106,'Bank of America':0.595843839,'Boeing':0.583589980}
        self.assertEqual(create_dividend_dict(DividendTestSuite.unittest_data, DividendTestSuite.test_names), expected)
        

class CAPMTestSuite(unittest.TestCase):
    
    data = pd.read_csv('./test_data/capm_market_unit_test_data.csv')
    R_f = 0.0175 / 252
    
    def test_calc_stock_beta(self):
        data = CAPMTestSuite.data
        R_f = CAPMTestSuite.R_f
        data.drop('date', 1, inplace=True)
        daily_returns_df = data.pct_change().dropna()
        
        aapl_excess_returns = daily_returns_df.aapl_adj_close.values - R_f
        spy_excess_returns = daily_returns_df.spy_adj_close.values - R_f
        
        result = calc_stock_beta(spy_excess_returns.reshape(-1, 1), aapl_excess_returns.reshape(-1, 1))
        expected = 1.088
        self.assertEqual(round(result, 3), expected)
        
if __name__ == '__main__':
    unittest.main() 