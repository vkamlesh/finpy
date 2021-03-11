#!/usr/bin/env /Users/vkamlesh/.virtualenvs/finpy/bin/python
#import sys
#sys.path.insert(1, '/Users/vkamlesh/src/finpy/mftool/mftool')
import json
import pandas as pd
import os.path
from mftool import Mftool
import sys

mf = Mftool()
#debt_fund = mf.get_open_ended_debt_scheme_performance(as_json=False)

debt_fund_keys = ['Long Duration', 
          'Medium to Long Duration', 
          'Medium Duration', 
          'Short Duration', 
          'Low Duration', 
          'Ultra Short Duration', 
          'Liquid', 
          'Money Market', 
          'Overnight', 
          'Dynamic Bond', 
          'Corporate Bond', 
          'Credit Risk', 
          'Banking and PSU',
          'Floater', 
          'FMP', 
          'Gilt',
          'Gilt with 10 year constant duration']


equity_fund_keys = ['Large Cap', 'Large & Mid Cap', 'Multi Cap', 'Mid Cap', 'Small Cap', 'Value', 'ELSS', 'Contra', 'Dividend Yield', 'Focused']  

#KeyError: 'Dynamic Asset Allocation or Balanced Advantage'
#hybrid_fund_keys=['Aggressive Hybrid','Balanced Hybrid', 'Conservative Hybrid', 'Equity Savings', 'Arbitrage', 'Multi Asset Allocation', 'Dynamic Asset Allocation or Balanced Advantage']
hybrid_fund_keys = ['Aggressive Hybrid', 'Balanced Hybrid', 'Conservative Hybrid', 'Equity Savings', 'Arbitrage', 'Multi Asset Allocation']
solution_fund_keys = ["Children's","Retirement"]

other_fund_keys = ["Index Funds/ETFs","FoFs(Oversease/Domestic)"]


if os.path.isfile('scheme_code.json'):
    pass
else:
    scheme_code = mf.get_scheme_codes()
    with open('scheme_code.json', 'w') as outfile:
        json.dump(scheme_code, outfile, indent=4)       

        
def debt_fund_direct_perf():
    debt_ld = mf.get_open_ended_debt_scheme_performance()
    #writer = pd.ExcelWriter('Debt_Fund_Direct_Performance.xlsx', engine='xlsxwriter')
    with pd.ExcelWriter('Debt_Fund_Direct_Performance.xlsx') as writer:                
        for key in debt_fund_keys:
            debt_fund_list = pd.DataFrame.from_dict(debt_ld[key])
            debt_direct_perf = debt_fund_list.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)
                                                        
            if key == "Gilt with 10 year constant duration":
                new_key="Gilt With 10Year"
                debt_direct_perf.to_excel(writer, sheet_name=new_key)
            else:    
                debt_direct_perf.to_excel(writer, sheet_name=key)


def equity_fund_direct_perf():
    equity_ld = mf.get_open_ended_equity_scheme_performance()
    with pd.ExcelWriter('Equity_Fund_Direct_Performance.xlsx') as writer:
        for key in equity_fund_keys:
            equity_fund_list = pd.DataFrame.from_dict(equity_ld[key])
            equity_direct_perf = equity_fund_list.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)      
            equity_direct_perf.to_excel(writer, sheet_name=key)

def hybrid_fund_direct_perf():
    hybrid_ld = mf.get_open_ended_hybrid_scheme_performance()
    with pd.ExcelWriter('Hybrid_Fund_Direct_Performance.xlsx') as writer:
        for key in hybrid_fund_keys:
            hybrid_fund_list = pd.DataFrame.from_dict(hybrid_ld[key])
            hybrid_direct_perf = hybrid_fund_list.drop(columns=['latest NAV- Regular', '1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)
            hybrid_direct_perf.to_excel(writer, sheet_name=key)
            #hybrid_fund_list.to_excel(writer,sheet_name=key)


# def solution_fund_direct_perf():
#     solution_ld = mf.get_open_ended_soultion_scheme_performance()
#     with pd.ExcelWriter('Solution_Fund_Direct_Performance.xlsx') as writer:
#         for key in solution_fund_keys:
#             solution_fund_list = pd.DataFrame.from_dict(solution_ld[key])
#             solution_direct_perf = solution_fund_list.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)
#             solution_direct_perf.to_excel(writer, sheet_name=key)

#def other_fund_direct_perf():
#     other_ld = mf.get_open_ended_other_scheme_performance()
#     with pd.ExcelFile('Other_Fund_Direct_Performance.xlsx') as writer:
#         for key in other_fund_keys:
#             other_fund_list = pd.DataFrame.from_dict(other_ld[key])
#             other_direct_perf = other_fund_list.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)
#             other_direct_perf.to_excel(writer,sheet_name=key)
            


#debt_fund_direct_perf()    
#equity_fund_direct_perf()
#solution_fund_direct_perf()
#hybrid_fund_direct_perf()



def mf_return(scheme_code):
    banner="Rolling returns "

    mf_name = input("Mutual Fund Name:")
    nav_start_date = input("Investment Start Date in D-M-YYYY \n")
    nav_end_date = input("Investment End Date in D-M-YYYY \n")
    with open(scheme_code_file,'r') as jdata:
        mf_code = json.load(scheme_code)
        data = json.load(jdata)
        for code,name in data.items():
            if mf_name == name:
                print("Name: {} and Code: {}".format(mf_name,code))

        #value = mf.get_scheme_historical_nav_for_dates(







mf_return(scheme_code)




#Unused Code
'''
with open(scheme_code_file,'r') as jdata:
        data = json.load(jdata)
        #rev_dic = {i: j for j, i in data.items()}
        for code, name in data.items():
            print(mf.get_scheme_quote(code))
                
'''

