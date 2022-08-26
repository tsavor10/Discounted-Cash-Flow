# import statements
import requests
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy_financial as npf
import yfinance as yf

# collect stock info
company = input("Ticker: ")
stock_info = yf.Ticker(company).info
market_price = stock_info['regularMarketPrice']
print('Current Price of ' + company + ": ", market_price)

# revenue growth
demo = 'API_Key'
IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey={demo}').json()
count = 0
revenue_g = []
for item in IS:
  if count < 4:
    revenue_g.append(item['revenue'])
    count = count + 1
revenue_g = (revenue_g[0] - revenue_g[1]) /revenue_g[0] 

# income statement and balance sheet
net_income = IS[0]['netIncome']
BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?apikey={demo}').json()
income_statement = pd.DataFrame.from_dict(IS[0], orient='index')
income_statement = income_statement[7:31]
income_statement.columns = ['current_year']
income_statement['as_%_of_revenue'] = income_statement.iloc[1:].astype(float)  / float(income_statement.iloc[1])
income_statement['next_year'] =  (income_statement['current_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue'] 
income_statement['next_2_year'] =  (income_statement['next_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue'] 
income_statement['next_3_year'] =  (income_statement['next_2_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue'] 
income_statement['next_4_year'] =  (income_statement['next_3_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue'] 
income_statement['next_5_year'] =  (income_statement['next_4_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue']
balance_sheet = pd.DataFrame.from_dict(BS[0],orient='index')
balance_sheet = balance_sheet[8:-2]
balance_sheet.columns = ['current_year']
balance_sheet['as_%_of_revenue'] = balance_sheet.iloc[3:].astype(float) / float(income_statement['current_year'].iloc[1])
balance_sheet['next_year'] =  income_statement['next_year'] ['revenue'] * balance_sheet['as_%_of_revenue']
balance_sheet['next_2_year'] =  income_statement['next_2_year'] ['revenue'] * balance_sheet['as_%_of_revenue']
balance_sheet['next_3_year'] =  income_statement['next_3_year']['revenue'] * balance_sheet['as_%_of_revenue'] 
balance_sheet['next_4_year'] =  income_statement['next_4_year']['revenue']  * balance_sheet['as_%_of_revenue'] 
balance_sheet['next_5_year'] =  income_statement['next_5_year']['revenue'] * balance_sheet['as_%_of_revenue']

# future cash flow
CF_forecast = {}
CF_forecast['next_year'] = {}
CF_forecast['next_year']['netIncome'] = income_statement['next_year']['netIncome']
CF_forecast['next_year']['inc_depreciation'] = income_statement['next_year']['depreciationAndAmortization'] - income_statement['current_year']['depreciationAndAmortization']
CF_forecast['next_year']['inc_receivables'] = balance_sheet['next_year']['netReceivables'] - balance_sheet['current_year']['netReceivables']
CF_forecast['next_year']['inc_inventory'] = balance_sheet['next_year']['inventory'] - balance_sheet['current_year']['inventory']
CF_forecast['next_year']['inc_payables'] = balance_sheet['next_year']['accountPayables'] - balance_sheet['current_year']['accountPayables']
CF_forecast['next_year']['CF_operations'] = CF_forecast['next_year']['netIncome'] + CF_forecast['next_year']['inc_depreciation'] + (CF_forecast['next_year']['inc_receivables'] * -1) + (CF_forecast['next_year']['inc_inventory'] *-1) + CF_forecast['next_year']['inc_payables']
CF_forecast['next_year']['CAPEX'] = balance_sheet['next_year']['propertyPlantEquipmentNet'] - balance_sheet['current_year']['propertyPlantEquipmentNet'] + income_statement['next_year']['depreciationAndAmortization']
CF_forecast['next_year']['FCF'] = CF_forecast['next_year']['CAPEX'] + CF_forecast['next_year']['CF_operations']
CF_forecast['next_2_year'] = {}
CF_forecast['next_2_year']['netIncome'] = income_statement['next_2_year']['netIncome']
CF_forecast['next_2_year']['inc_depreciation'] = income_statement['next_2_year']['depreciationAndAmortization'] - income_statement['next_year']['depreciationAndAmortization']
CF_forecast['next_2_year']['inc_receivables'] = balance_sheet['next_2_year']['netReceivables'] - balance_sheet['next_year']['netReceivables']
CF_forecast['next_2_year']['inc_inventory'] = balance_sheet['next_2_year']['inventory'] - balance_sheet['next_year']['inventory']
CF_forecast['next_2_year']['inc_payables'] = balance_sheet['next_2_year']['accountPayables'] - balance_sheet['next_year']['accountPayables']
CF_forecast['next_2_year']['CF_operations'] = CF_forecast['next_2_year']['netIncome'] + CF_forecast['next_2_year']['inc_depreciation'] + (CF_forecast['next_2_year']['inc_receivables'] * -1) + (CF_forecast['next_2_year']['inc_inventory'] *-1) + CF_forecast['next_2_year']['inc_payables']
CF_forecast['next_2_year']['CAPEX'] = balance_sheet['next_2_year']['propertyPlantEquipmentNet'] - balance_sheet['next_year']['propertyPlantEquipmentNet'] + income_statement['next_2_year']['depreciationAndAmortization']
CF_forecast['next_2_year']['FCF'] = CF_forecast['next_2_year']['CAPEX'] + CF_forecast['next_2_year']['CF_operations']
CF_forecast['next_3_year'] = {}
CF_forecast['next_3_year']['netIncome'] = income_statement['next_3_year']['netIncome']
CF_forecast['next_3_year']['inc_depreciation'] = income_statement['next_3_year']['depreciationAndAmortization'] - income_statement['next_2_year']['depreciationAndAmortization']
CF_forecast['next_3_year']['inc_receivables'] = balance_sheet['next_3_year']['netReceivables'] - balance_sheet['next_2_year']['netReceivables']
CF_forecast['next_3_year']['inc_inventory'] = balance_sheet['next_3_year']['inventory'] - balance_sheet['next_2_year']['inventory']
CF_forecast['next_3_year']['inc_payables'] = balance_sheet['next_3_year']['accountPayables'] - balance_sheet['next_2_year']['accountPayables']
CF_forecast['next_3_year']['CF_operations'] = CF_forecast['next_3_year']['netIncome'] + CF_forecast['next_3_year']['inc_depreciation'] + (CF_forecast['next_3_year']['inc_receivables'] * -1) + (CF_forecast['next_3_year']['inc_inventory'] *-1) + CF_forecast['next_3_year']['inc_payables']
CF_forecast['next_3_year']['CAPEX'] = balance_sheet['next_3_year']['propertyPlantEquipmentNet'] - balance_sheet['next_2_year']['propertyPlantEquipmentNet'] + income_statement['next_3_year']['depreciationAndAmortization']
CF_forecast['next_3_year']['FCF'] = CF_forecast['next_3_year']['CAPEX'] + CF_forecast['next_3_year']['CF_operations']
CF_forecast['next_4_year'] = {}
CF_forecast['next_4_year']['netIncome'] = income_statement['next_4_year']['netIncome']
CF_forecast['next_4_year']['inc_depreciation'] = income_statement['next_4_year']['depreciationAndAmortization'] - income_statement['next_3_year']['depreciationAndAmortization']
CF_forecast['next_4_year']['inc_receivables'] = balance_sheet['next_4_year']['netReceivables'] - balance_sheet['next_3_year']['netReceivables']
CF_forecast['next_4_year']['inc_inventory'] = balance_sheet['next_4_year']['inventory'] - balance_sheet['next_3_year']['inventory']
CF_forecast['next_4_year']['inc_payables'] = balance_sheet['next_4_year']['accountPayables'] - balance_sheet['next_3_year']['accountPayables']
CF_forecast['next_4_year']['CF_operations'] = CF_forecast['next_4_year']['netIncome'] + CF_forecast['next_4_year']['inc_depreciation'] + (CF_forecast['next_4_year']['inc_receivables'] * -1) + (CF_forecast['next_4_year']['inc_inventory'] *-1) + CF_forecast['next_4_year']['inc_payables']
CF_forecast['next_4_year']['CAPEX'] = balance_sheet['next_4_year']['propertyPlantEquipmentNet'] - balance_sheet['next_3_year']['propertyPlantEquipmentNet'] + income_statement['next_4_year']['depreciationAndAmortization']
CF_forecast['next_4_year']['FCF'] = CF_forecast['next_4_year']['CAPEX'] + CF_forecast['next_4_year']['CF_operations']
CF_forecast['next_5_year'] = {}
CF_forecast['next_5_year']['netIncome'] = income_statement['next_5_year']['netIncome']
CF_forecast['next_5_year']['inc_depreciation'] = income_statement['next_5_year']['depreciationAndAmortization'] - income_statement['next_4_year']['depreciationAndAmortization']
CF_forecast['next_5_year']['inc_receivables'] = balance_sheet['next_5_year']['netReceivables'] - balance_sheet['next_4_year']['netReceivables']
CF_forecast['next_5_year']['inc_inventory'] = balance_sheet['next_5_year']['inventory'] - balance_sheet['next_4_year']['inventory']
CF_forecast['next_5_year']['inc_payables'] = balance_sheet['next_5_year']['accountPayables'] - balance_sheet['next_4_year']['accountPayables']
CF_forecast['next_5_year']['CF_operations'] = CF_forecast['next_5_year']['netIncome'] + CF_forecast['next_5_year']['inc_depreciation'] + (CF_forecast['next_5_year']['inc_receivables'] * -1) + (CF_forecast['next_5_year']['inc_inventory'] *-1) + CF_forecast['next_5_year']['inc_payables']
CF_forecast['next_5_year']['CAPEX'] = balance_sheet['next_5_year']['propertyPlantEquipmentNet'] - balance_sheet['next_4_year']['propertyPlantEquipmentNet'] + income_statement['next_5_year']['depreciationAndAmortization']
CF_forecast['next_5_year']['FCF'] = CF_forecast['next_5_year']['CAPEX'] + CF_forecast['next_5_year']['CF_operations']

# convert cash flow into pandas
CF_forec = pd.DataFrame.from_dict(CF_forecast,orient='columns')
pd.options.display.float_format = '{:,.0f}'.format

# cost of capital
def interest_coveraga_and_RF(company):
  EBIT= IS[0]['ebitda'] - IS[0]['depreciationAndAmortization'] 
  interest_expense = IS[0]['interestExpense']
  interest_coverage_ratio = EBIT / interest_expense
  start = datetime.datetime(2021, 1, 1)    
  end= datetime.datetime.today().strftime('%Y-%m-%d')
  Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
  RF = float(Treasury.iloc[-1])
  RF = RF/100
  return [RF,interest_coverage_ratio]
def cost_of_debt(company, RF,interest_coverage_ratio):
  if interest_coverage_ratio > 8.5:
    credit_spread = 0.0063
  if (interest_coverage_ratio > 6.5) & (interest_coverage_ratio <= 8.5):
    credit_spread = 0.0078
  if (interest_coverage_ratio > 5.5) & (interest_coverage_ratio <=  6.5):
    credit_spread = 0.0098
  if (interest_coverage_ratio > 4.25) & (interest_coverage_ratio <=  5.49):
    credit_spread = 0.0108
  if (interest_coverage_ratio > 3) & (interest_coverage_ratio <=  4.25):
    credit_spread = 0.0122
  if (interest_coverage_ratio > 2.5) & (interest_coverage_ratio <=  3):
    credit_spread = 0.0156
  if (interest_coverage_ratio > 2.25) & (interest_coverage_ratio <=  2.5):
    credit_spread = 0.02
  if (interest_coverage_ratio > 2) & (interest_coverage_ratio <=  2.25):
    credit_spread = 0.0240
  if (interest_coverage_ratio > 1.75) & (interest_coverage_ratio <=  2):
    credit_spread = 0.0351
  if (interest_coverage_ratio > 1.5) & (interest_coverage_ratio <=  1.75):
    credit_spread = 0.0421
  if (interest_coverage_ratio > 1.25) & (interest_coverage_ratio <=  1.5):
    credit_spread = 0.0515
  if (interest_coverage_ratio > 0.8) & (interest_coverage_ratio <=  1.25):
    credit_spread = 0.0820
  if (interest_coverage_ratio > 0.65) & (interest_coverage_ratio <=  0.8):
    credit_spread = 0.0864
  if (interest_coverage_ratio > 0.2) & (interest_coverage_ratio <=  0.65):
    credit_spread = 0.1134
  if interest_coverage_ratio <=  0.2:
    credit_spread = 0.1512
  cost_of_debt = RF + credit_spread
  return cost_of_debt
def costofequity(company):
  start = datetime.datetime(2021, 1, 1)
  end= datetime.datetime.today().strftime('%Y-%m-%d')
  Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
  RF = float(Treasury.iloc[-1])
  RF = RF/100
  beta = requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{company}?apikey={demo}')
  beta = beta.json()
  beta = float(beta['profile']['beta'])
  start = datetime.datetime(2021, 1, 1)
  end= datetime.datetime.today().strftime('%Y-%m-%d')
  SP500 = web.DataReader(['sp500'], 'fred', start, end)
  SP500.dropna(inplace = True)
  SP500yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-252])-1
  cost_of_equity = RF+(beta*(SP500yearlyreturn - RF))
  return cost_of_equity
def wacc(company):
  FR = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey={demo}').json()
  ETR = FR[0]['effectiveTaxRate']
  Debt_to = BS[0]['totalDebt'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])
  equity_to = BS[0]['totalStockholdersEquity'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])
  WACC = (kd*(1-ETR)*Debt_to) + (ke*equity_to)
  return WACC
RF_and_IntCov = interest_coveraga_and_RF(company)
RF = RF_and_IntCov[0]
interest_coverage_ratio = RF_and_IntCov[1]
ke = costofequity(company)
kd = cost_of_debt(company,RF,interest_coverage_ratio)
wacc_company = abs(wacc(company))

# net present value
FCF_List = CF_forec.iloc[-1].values.tolist()
npv = npf.npv(wacc_company,FCF_List)

# terminal value
LTGrowth = 0.02
Terminal_value = (CF_forecast['next_5_year']['FCF'] * (1+ LTGrowth)) / (wacc_company - LTGrowth)
Terminal_value_Discounted = Terminal_value / (1 + wacc_company)**4
Terminal_value_Discounted

# target price
target_equity_value = Terminal_value_Discounted + npv
debt = balance_sheet['current_year']['totalDebt']
target_value = target_equity_value - debt
numbre_of_shares = requests.get(f'https://financialmodelingprep.com/api/v3/enterprise-values/{company}?apikey={demo}').json()
numbre_of_shares = numbre_of_shares[0]['numberOfShares']
target_price_per_share = target_value/numbre_of_shares

# print statements
print("Forecasted Price per Stock of " + company + ": " + str(target_price_per_share) )
print()
print(CF_forec.to_string())
print()
print('Revenue Growth: ' + str(revenue_g))
print('WACC: ' + str((wacc_company*100)) + '%')
print("NPV: " + str(npv))
print('Cost of Capital: ' + str(wacc_company) )
print('Perpetuity Growth: ' + str(LTGrowth)  )
