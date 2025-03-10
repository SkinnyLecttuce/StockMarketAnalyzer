import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#RSI, MACD, Bollinger Bands, ATR, OBV

c='stocks\\'

meta_df = pd.read_csv(c+'tickers.csv')

df=meta_df
 
info={}

for symb,name in zip(meta_df['Ticker'],meta_df['Name']):
    info[symb] = name


def extract_dat(stck_name,normal):
    stck_name+='.csv'
    if(normal == True):
        path='stocks\\stocks\\'+stck_name
    else:
        path='stocks\\etfs\\'+stck_name
    
    stock_df = pd.read_csv(path)
    '''
    plt.xlabel('Opened Value')
    plt.ylabel('Closed Value')
    plt.scatter(stock_df['Open'],stock_df['Adj Close'])
    plt.show()
    plt.xlabel('High Values')
    plt.ylabel('Low Values')
    plt.scatter(stock_df['High'],stock_df['Low'])
    plt.show()'''

    rsi20 = rsi(stock_df)
    macdout = macd(stock_df)
    
    diff_co = stock_df['Close'] - stock_df['Open']
    diff_hl = stock_df['High'] - stock_df['Low']

    print("-----Closes vs Opens difference --------\n Max:{0} \n Min:{1} \n Mean:{2} \n Mode:{3} \n Median:{4} \n".format(diff_co.max(), diff_co.min(), diff_co.mean(), diff_co.mode().iloc[0], diff_co.median()))
    print("-----Highs vs Lows difference --------\n Max:{0} \n Min:{1} \n Mean:{2} \n Mode:{3} \n Median:{4} \n".format(diff_hl.max(), diff_hl.min(), diff_hl.mean(), diff_hl.mode().iloc[0], diff_hl.median()))

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    sns.histplot(diff_co, kde=True, ax=ax[0], color='blue', stat='density', bins=30)
    ax[0].set_title('Closes vs Opens Difference')

    sns.histplot(diff_hl, kde=True, ax=ax[1], color='green', stat='density', bins=30)
    ax[1].set_title('Highs vs Lows Difference')

    plt.tight_layout()
    plt.show()

    plt.xlabel('Days')
    plt.ylabel('Prices')
    stock_df['Date'] = range(1, len(stock_df) + 1)
    plt.scatter(stock_df['Date'],stock_df['Open'],label='Open prices',color='blue')
    plt.scatter(stock_df['Date'],stock_df['Close'],label='Closing prices',color='yellow')
    plt.legend(loc='upper left')
    plt.show()
    
    plt.scatter(stock_df['Date'],stock_df['High'],label='Highest value for a particular day',color='green')
    plt.scatter(stock_df['Date'],stock_df['Low'],label='Lowest value for a particular day',color='orange')
    plt.legend(loc='upper left')
    plt.show()

    plt.title('Volume vs Days')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.bar(stock_df['Date'],stock_df['Volume'])
    plt.show()
    
    corr_matrix = stock_df.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

    plt.title('Stock Price Correlation Heatmap', fontsize=15)
    plt.show()


def find(stck_tag):
    col={}
    i=0
    stck_tag=stck_tag.lower()
    for stck,desc in zip(info.keys(),info.values()):
        if(stck_tag in stck.lower() or stck_tag in desc.lower()):
            col[i] = [stck,desc]
            i+=1
    return col
    
def print_info_dict(info_dict):
    print("\nAll available stocks and their descriptions:\n")
    for index, (key, value) in enumerate(info_dict.items(), start=0):
        print(f"{index}. {key}: {value}")

import ta
def rsi(stockdf):
    df=pd.DataFrame({'RSI_20':[],'Oversold/Overbought/Neutral':[]},dtype=float)
    df['RSI_20'] = ta.momentum.rsi(stockdf['Adj Close'], window=20)

    df['Oversold/Overbought/Neutral'] = np.where(df['RSI_20'] > 70, 'Overbought', np.where(df['RSI_20'] < 30, 'Oversold','Neutral'))
    df.to_csv('RSI20.csv',index=False)

    label_counts = df['Oversold/Overbought/Neutral'].value_counts()

    label_counts.plot(kind='bar', color=['green', 'red', 'blue']) 
    plt.title("RSI Label Frequency")
    plt.xlabel("RSI Label")
    plt.ylabel("Frequency") 
    plt.show()

    return df

def macd(stockdf):
    df=pd.DataFrame({'MACD_line':[],'MACD_signal':[],'MACD_hist':[]},dtype=float)
    
    df['MACD_line'] = ta.trend.macd(
    close=stockdf['Adj Close'], 
    window_slow=26, 
    window_fast=12)

    df['MACD_signal'] = ta.trend.macd_signal(
    close=stockdf['Adj Close'], 
    window_slow=26, 
    window_fast=12, 
    window_sign=9)

    df['MACD_hist'] = ta.trend.macd_diff(
    close=stockdf['Adj Close'], 
    window_slow=26, 
    window_fast=12, 
    window_sign=9)

    df['MACD_Interpretation'] = np.where(
        df['MACD_line'] > df['MACD_signal'],
        'Bullish',
        'Bearish'
    )
    df['MACD_Crossover'] = 'No Crossover'

    bullish_mask = (
        (df['MACD_line'].shift(1) < df['MACD_signal'].shift(1)) & 
        (df['MACD_line'] > df['MACD_signal'])
    )
    bearish_mask = (
        (df['MACD_line'].shift(1) > df['MACD_signal'].shift(1)) & 
        (df['MACD_line'] < df['MACD_signal'])
    )

    df.loc[bullish_mask, 'MACD_Crossover'] = 'Bullish Crossover'
    df.loc[bearish_mask, 'MACD_Crossover'] = 'Bearish Crossover'

    label_counts = df['MACD_Interpretation'].value_counts()

    label_counts.plot(kind='bar', color=['green', 'red']) 
    plt.title("Bullish/Bearish Label Frequency")
    plt.xlabel("Bullish/Bearish Label")
    plt.ylabel("Frequency") 
    plt.show()
    
    df.to_csv('MACD.csv',index=False)
    
    return df

    
while True:
    tag=input('Search what ?')
    print('Finding...')

    db=find(tag)
    print_info_dict(db)
    try:
        if not db:
            print("We dont have that")
        else:
            stoink_name = db[int(input("Select Index:"))][0]
            print(info[stoink_name])
            extract_dat(stoink_name,True)
    except Exception as e:
        print("Skipping... because of "+str(e))


