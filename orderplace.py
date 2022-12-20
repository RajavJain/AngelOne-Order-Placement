#!/usr/bin/env python
# coding: utf-8

# In[15]:


pip install smartapi-python


# In[16]:


pip install websocket-client


# In[84]:


from smartapi import SmartConnect


# In[85]:


obj=SmartConnect(api_key="****")


# In[86]:


token = '****'


# In[87]:


pip install pyotp


# In[88]:


pip --no-cache-dir install --upgrade smartapi-python


# In[110]:


import pyotp


# In[111]:


pyotp.TOTP(token).now()


# In[180]:


data = obj.generateSession("****","****@20",pyotp.TOTP(token).now())


# In[181]:


refreshToken= data['data']['refreshToken']


# In[182]:


feedToken=obj.getfeedToken()


# In[183]:


userProfile= obj.getProfile(refreshToken)


# In[184]:


userProfile


# In[ ]:





# In[117]:


import pandas as pd
from datetime import datetime
import requests
import numpy as np

url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
token_df['expiry'] = pd.to_datetime(token_df['expiry'])
token_df = token_df.astype({'strike': float})
# credentials.TOKEN_MAP = token_df


# In[141]:


token_df


# In[142]:


def getTokenInfo (df, exch_seg, instrumenttype,symbol,strike_price,pe_ce):
#     df = credentials.TOKEN_MAP
    strike_price = strike_price*100
    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') & (df['symbol'].str.contains('EQ')) ]
        return eq_df[eq_df['name'] == symbol]
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])


# In[185]:


token_info= getTokenInfo(token_df, 'NFO','FUTIDX','BANKNIFTY',2000,'PE').iloc[0]
token_info


# In[186]:


token_info['token']


# In[187]:


token_info['symbol']


# In[188]:


token_info['lotsize']


# In[189]:


try:
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": token_info['symbol'],
        "symboltoken": token_info['token'],
        "transactiontype": "BUY",
        "exchange": "NFO",
        "ordertype": "MARKET",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": "0",
        "squareoff": "0",
        "stoploss": "0",
        "quantity": token_info['lotsize']
        }
    orderId=obj.placeOrder(orderparams)
    print("The order id is: {}".format(orderId))
except Exception as e:
    print("Order placement failed: {}".format(e.message))


# In[ ]:


