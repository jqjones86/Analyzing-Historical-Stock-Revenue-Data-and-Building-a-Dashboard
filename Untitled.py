#!/usr/bin/env python
# coding: utf-8

# !pip install yfinance
# !pip install pandas
# !pip install requests
# !pip install bs4
# !pip install plotly

# In[5]:


import pandas as pd
import yfinance as yf
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[6]:


tesla = yf.Ticker("TSLA")


# In[7]:


tesla_data = tesla.history(period="max")


# In[8]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# In[9]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"


# In[10]:


html_data = requests.get(url).text


# In[11]:


soup = BeautifulSoup(html_data, "html.parser")
soup.find_all('title')


# In[12]:


tesla_revenue = pd.DataFrame(columns = ['Date', 'Revenue'])

for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")
    
    tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index = True)


# In[13]:


tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[14]:


tesla_revenue.tail()


# In[15]:


gamestop = yf.Ticker("GME")


# In[16]:


gamestop_data = gamestop.history(period="max")


# In[17]:


gamestop_data.reset_index(inplace=True)
gamestop_data.head()


# In[18]:


url1 = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"


# In[19]:


html_data = requests.get(url1).text


# In[20]:


soup = BeautifulSoup(html_data, "html.parser")
soup.find_all('title')


# In[21]:


gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if ('GameStop Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')
        
        for row in rows:
            col = row.find_all('td')
            
            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',','').replace('$','')

                gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)


# In[22]:


gme_revenue.tail()


# In[23]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[26]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[27]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# In[28]:


make_graph(gamestop_data, gme_revenue, 'GameStop')


# In[ ]:




