#!/usr/bin/env /Users/vkamlesh/.virtualenvs/finpy/bin/python
import json
import pandas as pd
import os.path
from mftool import Mftool
import sys

mf = Mftool()
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
hybrid_fund_keys=['Aggressive Hybrid','Balanced Hybrid', 'Conservative Hybrid', 'Equity Savings', 'Arbitrage', 'Multi Asset Allocation', 'Dynamic Asset Allocation or Balanced Advantage']
solution_fund_keys = ["Children's","Retirement"]

other_fund_keys = ["Index Funds/ETFs","FoFs(Oversease/Domestic)"]

if os.path.isfile('scheme_code.json'):
    pass
else:
    scheme_code = mf.get_scheme_codes(as_json=True)
    with open('scheme_code.json', 'w') as outfile:
        json.dump(scheme_code, outfile, indent=4)    



def main(choice):
    if choice == "1":
        debt_fund_direct_perf()
    elif choice == "2":
        equity_fund_direct_perf()
    elif choice == "3":
        hybrid_fund_direct_perf()
    elif choice == "4":
        solution_fund_direct_perf()
    elif choice == "5":
        other_fund_direct_perf()
    else:
        print("Please select right choice\n")                    


#Exception handling due to data unavailability at www.amfiindia.com.(https://www.amfiindia.com/research-information/other-data/mf-scheme-performance-details)
        
def debt_fund_direct_perf():
    debt_ld = mf.get_open_ended_debt_scheme_performance()
    #writer = pd.ExcelWriter('Debt_Fund_Direct_Performance.xlsx', engine='xlsxwriter')
    with pd.ExcelWriter('Debt_Fund_Direct_Performance.xlsx') as writer:                
        for key in debt_fund_keys:
            try:
                debt_fund_list = pd.DataFrame.from_dict(debt_ld[key])
                debt_direct_perf = debt_fund_list.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)
                                                            
                if key == "Gilt with 10 year constant duration":
                    new_key="Gilt With 10Year"
                    debt_direct_perf.to_excel(writer, sheet_name=new_key)
                else:    
                    debt_direct_perf.to_excel(writer, sheet_name=key)
            except KeyError:
                print("Data for {} is not available Today.".format(key))
                pass
            except Exception as exc:
                print("Unexpected error: {}".format(exc))         


def equity_fund_direct_perf():
    equity_ld = mf.get_open_ended_equity_scheme_performance()
    with pd.ExcelWriter('Equity_Fund_Direct_Performance.xlsx') as writer:
        for key in equity_fund_keys:
            try:                    
                equity_fund_list = pd.DataFrame.from_dict(equity_ld[key])
                equity_direct_perf = equity_fund_list.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)      
                equity_direct_perf.to_excel(writer, sheet_name=key)
            except KeyError:
                print("Data for {} is not available Today.".format(key))
                pass
            except Exception as exc:
                print("Unexpected error: {}".format(exc))     
                

def hybrid_fund_direct_perf():
    hybrid_ld = mf.get_open_ended_hybrid_scheme_performance()
    with pd.ExcelWriter('Hybrid_Fund_Direct_Performance.xlsx') as writer:             
        for key in hybrid_fund_keys:
            try:
                hybrid_fund_list = pd.DataFrame.from_dict(hybrid_ld[key])
                hybrid_direct_perf = hybrid_fund_list.drop(columns=['latest NAV- Regular', '1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)
                hybrid_direct_perf.to_excel(writer, sheet_name=key)
                #hybrid_fund_list.to_excel(writer,sheet_name=key)
            except KeyError:
                print("Data for {} is not available Today.".format(key))
                pass
            except Exception as exc:
                print("Unexpected error: {}".format(exc)) 



def solution_fund_direct_perf():
    solution_ld = mf.get_open_ended_solution_scheme_performance()
    with pd.ExcelWriter('Solution_Fund_Direct_Performance.xlsx') as writer: 
        for key in solution_fund_keys:
            try:
                solution_fund_list = pd.DataFrame.from_dict(solution_ld[key])
                solution_direct_perf = solution_fund_list.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)
                solution_direct_perf.to_excel(writer, sheet_name=key)
            except KeyError:
                print("Data for {} is not available Today.".format(key))
                pass
            except Exception as exc:
                print("Unexpected error: {}".format(exc))


def other_fund_direct_perf():
    other_ld = mf.get_open_ended_other_scheme_performance()
    with pd.ExcelWriter('Other_Fund_Direct_Performance.xlsx') as writer: 
        for key in other_fund_keys:
            try:
                other_fund_list = pd.DataFrame.from_dict(other_ld[key])
                if key == 'Index Funds/ETFs':
                    ETF_VALUE = []
                    INDEX_VALUE = []
                    for scheme in other_fund_list['scheme_name']:
                        if "ETF" in scheme:
                            etf = pd.DataFrame(other_fund_list.loc[other_fund_list['scheme_name'] == scheme])
                            ETF_VALUE.append(etf)
                        else:
                            idx = pd.DataFrame(other_fund_list.loc[other_fund_list['scheme_name'] == scheme])
                            INDEX_VALUE.append(idx)
                    ETF_VALUE = pd.concat(ETF_VALUE)
                    INDEX_VALUE = pd.concat(INDEX_VALUE)      
                    ETF_DATA = ETF_VALUE.drop(columns=['latest NAV- Direct','1-Year Return(%)- Direct','3-Year Return(%)- Direct','5-Year Return(%)- Direct'],axis=1)    
                    INDEX_DATA = INDEX_VALUE.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)

                    ETF_DATA.to_excel(writer,sheet_name='ETF')            
                    INDEX_DATA.to_excel(writer,sheet_name='IndexFund')
                else:
                    other_direct_perf = other_fund_list.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular'],axis=1)
                    new_key = ''.join(s for s in key if s.isalnum()) #Handle Error: Invalid Excel character '[]:*?/\' in sheetname
                    other_direct_perf.to_excel(writer,sheet_name=new_key)
            except KeyError:
                print("Data for {} is not available Today.".format(key))
                pass
            except Exception as exc:
                print("Unexpected error: {}".format(exc))     
            

if __name__ == '__main__':

    choice = input("Select fund category from following list.\n1.Debt\n2.Equity\n3.Hybrid\n4.Solution-Oriented\n5.Index/ETF\n")
    main(choice)
