import quandl
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
import numpy as np
import datetime as dt

def zscore(x,window):
    r = x.rolling(window=window)
    m = r.mean().shift(1)
    s = r.std(ddof=0).shift(1)
    z = (x-m)/s
    return z

from pytrends.request import TrendReq
from pytrends import dailydata
import pandas as pd
import time


#IMPORT API DATA


#1) BITCOIN (Quandl)
#price
BTC_Price = quandl.get("BCHAIN/MKPRU", authtoken="MLqdBGHGkytXGq-YPLZE")
BTC_MarketCap = quandl.get("BCHAIN/MKTCP", authtoken="MLqdBGHGkytXGq-YPLZE")

#users of the network
BTC_NrTransactions = quandl.get("BCHAIN/NTRAN", authtoken="MLqdBGHGkytXGq-YPLZE")
BTC_USDVolume = quandl.get("BCHAIN/TRVOU", authtoken="MLqdBGHGkytXGq-YPLZE")
BTC_MyWalletUsers = quandl.get("BCHAIN/MWNUS", authtoken="MLqdBGHGkytXGq-YPLZE")
BTC_NrUniqueAddress = quandl.get("BCHAIN/NADDU", authtoken="MLqdBGHGkytXGq-YPLZE")

#miners
BTC_HashRate = quandl.get("BCHAIN/HRATE", authtoken="MLqdBGHGkytXGq-YPLZE")
BTC_CostperTransaction = quandl.get("BCHAIN/CPTRA", authtoken="MLqdBGHGkytXGq-YPLZE")
BTC_MinersRevenue = quandl.get("BCHAIN/MIREV", authtoken="MLqdBGHGkytXGq-YPLZE")
BTC_BlockSize = quandl.get("BCHAIN/AVBLS", authtoken="MLqdBGHGkytXGq-YPLZE")
BTC_Difficulty = quandl.get("BCHAIN/DIFF", authtoken="MLqdBGHGkytXGq-YPLZE")


#INDICATORS

#1) BITCOIN (Quandl)

#users of the network
BTC_NrTransactions_MOM = pd.DataFrame(BTC_NrTransactions/BTC_NrTransactions.shift(91)-1)
BTC_MCtoTrans = pd.DataFrame(BTC_MarketCap/BTC_NrTransactions).reset_index()
BTC_MCtoTrans_MOM = pd.DataFrame((BTC_MarketCap/BTC_NrTransactions)/(BTC_MarketCap/BTC_NrTransactions).shift(91) - 1).reset_index()
BTC_USDVolume_MOM = pd.DataFrame(BTC_USDVolume/BTC_USDVolume.shift(91)-1)
BTC_USDVolume_zscore = pd.DataFrame(zscore(BTC_USDVolume,365))
BTC_MyWalletUsers_MOM = pd.DataFrame(BTC_MyWalletUsers/BTC_MyWalletUsers.shift(91)-1)
BTC_NrUniqueAddress_MOM = pd.DataFrame(BTC_NrUniqueAddress/BTC_NrUniqueAddress.shift(91)-1)

#miners
BTC_MCtoHR = pd.DataFrame(BTC_MarketCap/BTC_HashRate).reset_index()
BTC_MCtoHR_MOM = pd.DataFrame((BTC_MarketCap/BTC_HashRate)/(BTC_MarketCap/BTC_HashRate).shift(91) - 1).reset_index()
#BTC_MCtoHR_zscore = pd.DataFrame(zscore(BTC_MCtoHR,365))
BTC_CostperTransaction_MOM = pd.DataFrame(BTC_CostperTransaction/BTC_CostperTransaction.shift(91)-1)
BTC_MinersRevenue_MOM = pd.DataFrame(BTC_MinersRevenue/BTC_MinersRevenue.shift(91)-1)
BTC_BlockSize_MOM = pd.DataFrame(BTC_BlockSize/BTC_BlockSize.shift(91)-1)
BTC_Difficulty_MOM = pd.DataFrame(BTC_Difficulty/BTC_Difficulty.shift(91)-1)




'''
Bitcoin:Number of Transactions
'''

#CHARTS ATTRIBUTES
#amount of data to display
hist = 1500
fig, (ax1, ax3) = plt.subplots(1, 2)
#size of chart
fig.set_size_inches(12, 6)
#chart title
#fig.suptitle('Market Cap to transactions and 3M Momentum', fontsize=16, y=1)


#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Mcap/Tx', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_MCtoTrans['Value'].tail(hist).rolling(window=7).mean(), color=color)
ax1.tick_params(axis='y', labelcolor=color)




#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('Market cap to transactions')

 
#second chart, first axis:
color = 'tab:red'
ax3.set_xlabel('Date')
ax3.set_ylabel('MCap/Tx (3M change, 1-week MA)', color=color)
ax3.plot(BTC_MCtoHR['Date'].tail(hist), BTC_MCtoTrans_MOM['Value'].tail(hist).rolling(window=7).mean(), color=color)
ax3.tick_params(axis='y', labelcolor=color)

 
#second chart, second axis:
ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax4.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax4.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('3 months change')

#format x axis
plt.sca(ax1)
plt.xticks(rotation=45)
plt.sca(ax3)
plt.xticks(rotation=45)

#spacing between charts
fig.tight_layout()


'''
Bitcoin:USD Volume
'''
 
#CHARTS ATTRIBUTES
#amount of data to display
hist = 365
fig, ax1 = plt.subplots()
#size of chart
fig.set_size_inches(12, 6)
#chart title
fig.suptitle('USD Volume')
 
#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('USD Volume', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_USDVolume['Value'].tail(hist), color=color)
ax1.tick_params(axis='y', labelcolor=color)
#ax1.invert_yaxis()
 
#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'

ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
#plt.yscale(value='log')

 '''
Bitcoin:MyWallet users
'''

#CHARTS ATTRIBUTES
#amount of data to display
hist = 720
fig, (ax1, ax3) = plt.subplots(1, 2)
#size of chart
fig.set_size_inches(12, 6)
#chart title
#fig.suptitle('MyWallet users and 3M Momentum')
 
#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('MyWallet users', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_MyWalletUsers['Value'].tail(hist), color=color)
ax1.tick_params(axis='y', labelcolor=color)
#ax1.invert_yaxis()

#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('MyWallet users')
 
#second chart, first axis:
color = 'tab:red'
ax3.set_xlabel('Date')
ax3.set_ylabel('MyWallet users (3M Momentum)', color=color)
ax3.plot(BTC_MCtoHR['Date'].tail(hist), BTC_MyWalletUsers_MOM['Value'].tail(hist), color=color)
ax3.tick_params(axis='y', labelcolor=color)
 
#second chart, second axis:
ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax4.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax4.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('3-months change')
 
#format x axis
plt.sca(ax1)
plt.xticks(rotation=45)
plt.sca(ax3)
plt.xticks(rotation=45)    

#spacing between charts
fig.tight_layout()
 
'''
Bitcoin: Unique Address
'''
 
#CHARTS ATTRIBUTES
#amount of data to display
hist = 720
fig, (ax1, ax3) = plt.subplots(1, 2)
#size of chart
fig.set_size_inches(12, 6)
#chart title
#fig.suptitle('Unique Address and 3M Momentum (1-week MA)')
 
#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Unique Address', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_NrUniqueAddress['Value'].tail(hist), color=color)
ax1.tick_params(axis='y', labelcolor=color)
#ax1.invert_yaxis()
 
#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('Unique Address')
 
#second chart, first axis:
color = 'tab:red'
ax3.set_xlabel('Date')
ax3.set_ylabel('Unique Address (3M Momentum)', color=color)
ax3.plot(BTC_MCtoHR['Date'].tail(hist), BTC_NrUniqueAddress_MOM['Value'].tail(hist).rolling(window=7).mean(), color=color)
ax3.tick_params(axis='y', labelcolor=color)
 
#second chart, second axis:
ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax4.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax4.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('3-months change')

#format x axis
plt.sca(ax1)
plt.xticks(rotation=45)
plt.sca(ax3)
plt.xticks(rotation=45)
 
#spacing between charts
fig.tight_layout()
 
'''
Bitcoin: Hash Rate
'''
 
#CHARTS ATTRIBUTES
#amount of data to display
hist = 2500
fig, ax1 = plt.subplots()
#size of chart
fig.set_size_inches(12, 6)
#chart title
fig.suptitle('Hash Rate')
 

#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Hash Rate', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_HashRate['Value'].tail(hist), color=color)
ax1.tick_params(axis='y', labelcolor=color)
#ax1.invert_yaxis()
 
#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
 
#spacing between charts
fig.tight_layout()


'''
Bitcoin: Hash Rate
'''

#CHARTS ATTRIBUTES
#amount of data to display

hist = 2500
fig, (ax1, ax3) = plt.subplots(1, 2)
#size of chart
fig.set_size_inches(12, 6)
#chart title
#fig.suptitle('Market Cap per Hash Rate and 3M Momentum')
 


#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Market Cap to Hash Rate', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_MCtoHR['Value'].tail(hist), color=color)
ax1.tick_params(axis='y', labelcolor=color)
#ax1.invert_yaxis()
 
#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('Market Cap per Hash Rate')

 
#second chart, first axis:
color = 'tab:red'
ax3.set_xlabel('Date')
ax3.set_ylabel('Market Cap to Hash Rate (3M change, 1w MA)', color=color)
ax3.plot(BTC_MCtoHR['Date'].tail(hist), BTC_MCtoHR_MOM['Value'].tail(hist).rolling(window=7).mean(), color=color)
ax3.tick_params(axis='y', labelcolor=color)
 
#second chart, second axis:
ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax4.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax4.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('3-months change')
 
#format x axis
plt.sca(ax1)
plt.xticks(rotation=45)
plt.sca(ax3)
plt.xticks(rotation=45)

#spacing between charts
fig.tight_layout()'''
Bitcoin: Cost per Transaction
'''
 
#CHARTS ATTRIBUTES
#amount of data to display
hist = 2500
fig, (ax1, ax3) = plt.subplots(1, 2)
#size of chart
fig.set_size_inches(12, 6)
#chart title
#fig.suptitle('Cost per Transaction and 3M Momentum')
 
#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Cost per Transaction', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_CostperTransaction['Value'].tail(hist), color=color)
ax1.tick_params(axis='y', labelcolor=color)
#ax1.invert_yaxis()
 
#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('Cost per Transaction')
 
#second chart, first axis:
color = 'tab:red'
ax3.set_xlabel('Date')
ax3.set_ylabel('Cost per Transaction (3M change, 1w MA)', color=color)
ax3.plot(BTC_MCtoHR['Date'].tail(hist), BTC_CostperTransaction_MOM['Value'].tail(hist).rolling(window=7).mean(), color=color)
ax3.tick_params(axis='y', labelcolor=color)
 
#second chart, second axis:
ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax4.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax4.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
plt.title('3-months change')
 
#format x axis
plt.sca(ax1)
plt.xticks(rotation=45)
plt.sca(ax3)
plt.xticks(rotation=45)

#spacing between charts
fig.tight_layout()
 '''
Bitcoin: Miners Revenue
'''
 
#CHARTS ATTRIBUTES
#amount of data to display
hist = 720
fig, (ax1, ax3) = plt.subplots(1, 2)
#size of chart
fig.set_size_inches(12, 6)
#chart title
fig.suptitle('Miners Revenue and 3M Momentum')
 
#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Miners Revenue', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_MinersRevenue['Value'].tail(hist), color=color)
ax1.tick_params(axis='y', labelcolor=color)
#ax1.invert_yaxis()
 
#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
 
#second chart, first axis:
color = 'tab:red'
ax3.set_xlabel('Date')
ax3.set_ylabel('Miners Revenue (3M Momentum)', color=color)
ax3.plot(BTC_MCtoHR['Date'].tail(hist), BTC_MinersRevenue_MOM['Value'].tail(hist), color=color)
ax3.tick_params(axis='y', labelcolor=color)
 
#second chart, second axis:
ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax4.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax4.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
 
#format x axis
plt.sca(ax1)
plt.xticks(rotation=45)
plt.sca(ax3)
plt.xticks(rotation=45)

#spacing between charts
fig.tight_layout()
 
 '''
Bitcoin: Average Block Size
'''
 
#CHARTS ATTRIBUTES
#amount of data to display
hist = 2500
fig, (ax1, ax3) = plt.subplots(1, 2)
#size of chart
fig.set_size_inches(12, 6)
#chart title
fig.suptitle('Average Block Size and 3M Momentum')
 
#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Average Block Size', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_BlockSize['Value'].tail(hist), color=color)
ax1.tick_params(axis='y', labelcolor=color)
#ax1.invert_yaxis()
 
#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
 
#second chart, first axis:
color = 'tab:red'
ax3.set_xlabel('Date')
ax3.set_ylabel('Average Block Size (3M Momentum)', color=color)
ax3.plot(BTC_MCtoHR['Date'].tail(hist), BTC_BlockSize_MOM['Value'].tail(hist), color=color)
ax3.tick_params(axis='y', labelcolor=color)
 
#second chart, second axis:
ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax4.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax4.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
 
#format x axis
plt.sca(ax1)
plt.xticks(rotation=45)
plt.sca(ax3)
plt.xticks(rotation=45)

#spacing between charts
fig.tight_layout()'''
Bitcoin: Difficulty
'''

#CHARTS ATTRIBUTES
#amount of data to display
hist = 1000
fig, (ax1, ax3) = plt.subplots(1, 2)
#size of chart
fig.set_size_inches(12, 6)
#chart title
fig.suptitle('Difficulty and 3M Momentum')
 
#first chart, first axis:
color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Difficulty', color=color)
ax1.plot(BTC_MCtoHR['Date'].tail(hist), BTC_Difficulty['Value'].tail(hist), color=color)
ax1.tick_params(axis='y', labelcolor=color)
#ax1.invert_yaxis()
 
#first chart, second axis:
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax2.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
 
#second chart, first axis:
color = 'tab:red'
ax3.set_xlabel('Date')
ax3.set_ylabel('Difficulty (3M Momentum)', color=color)
ax3.plot(BTC_MCtoHR['Date'].tail(hist), BTC_Difficulty_MOM['Value'].tail(hist), color=color)
ax3.tick_params(axis='y', labelcolor=color)
 
#second chart, second axis:
ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.set_ylabel('Price', color=color)  # we already handled the x-label with ax1
ax4.plot(BTC_MCtoHR['Date'].tail(hist),BTC_Price['Value'].tail(hist), color=color)
ax4.tick_params(axis='y', labelcolor=color)
plt.yscale(value='log')
 
#format x axis
plt.sca(ax1)
plt.xticks(rotation=45)
plt.sca(ax3)
plt.xticks(rotation=45)

#spacing between charts
fig.tight_layout()
 
