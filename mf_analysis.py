#!/usr/bin/env /Users/vkamlesh/.virtualenvs/finpy/bin/python
import json
import pandas as pd
import os.path
from mftool import Mftool

mf = Mftool()
#debt_fund = mf.get_open_ended_debt_scheme_performance(as_json=False)


if os.path.isfile('scheme_code.json'):
    pass
else:
    scheme_code = mf.get_scheme_codes()
    with open('scheme_code.json', 'w') as outfile:
        json.dump(scheme_code, outfile, indent=4)



def debt_Long_Duration(scheme_code_file):
    debt_ld = mf.get_open_ended_debt_scheme_performance()
    debt_ld_df = pd.DataFrame.from_dict(debt_ld['Long Duration'])
    debt_ld_df_direct = (debt_ld_df.drop(columns=['latest NAV- Regular','1-Year Return(%)- Regular','3-Year Return(%)- Regular','5-Year Return(%)- Regular']))
    debt_ld_df_reg = debt_ld_df.drop(columns=['latest NAV- Direct', '1-Year Return(%)- Direct','3-Year Return(%)- Direct','5-Year Return(%)- Direct'])
    with open(scheme_code_file,'r') as jdata:
        data = json.load(jdata)
        #rev_dic = {i: j for j, i in data.items()}
        for scheme_name in debt_ld_df_direct['scheme_name']:
            for code, name in data.items():
                if scheme_name in name and "Direct Plan -" in name:
                    print(mf.get_today())
                


    print(debt_ld_df_direct)





debt_Long_Duration('scheme_code.json')    






#gilt_debt_fund = debt_fund['Gilt']

#df = pd.DataFrame(gilt_debt_fund, index=['scheme_name', 'benchmark','latest NAV- Regular', 'latest NAV- Direct', '1-Year Return(%)- Regular', '1-Year Return(%)- Direct', '3-Year Return(%)- Regular', '3-Year Return(%)- Direct', '5-Year Return(%)- Regular', '5-Year Return(%)- Direct'])
#df = pd.DataFrame.from_dict(gilt_debt_fund)


#print(df)



#dict_keys(['Long Duration', 
#           'Medium to Long Duration', 
#           'Medium Duration', 
#           'Short Duration', 
#           'Low Duration', 
#           'Ultra Short Duration', 
#           'Liquid', 
#           'Money Market', 
#           'Overnight', 
#           'Dynamic Bond', 
#           'Corporate Bond', 
#           'Credit Risk', 
#           'Banking and PSU',
#           'Floater', 
#           'FMP', 
#           'Gilt', 
#           'Gilt with 10 year constant duration'])

#print(debt_fund['Gilt'])



#[{'scheme_name': 'Aditya Birla Sun Life Government Securities Fund', 'benchmark': 'NIFTY All Duration G-Sec Total Return Index', 'latest NAV- Regular': '63.7908', 'latest NAV- Direct': '66.5728', '1-Year Return(%)- Regular': '12.09', '1-Year Return(%)- Direct': '12.76', '3-Year Return(%)- Regular': '9.93', '3-Year Return(%)- Direct': '10.58', '5-Year Return(%)- Regular': '10.10', '5-Year Return(%)- Direct': '10.70'},


#print(debt_fund.keys())

#print(debt_fund)

#with open('debt_fund.json', 'w') as outfile:
#    json.dump(debt_fund, outfile, indent=4)

