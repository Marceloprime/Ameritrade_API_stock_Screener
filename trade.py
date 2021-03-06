import requests, time, re, pickle
import pandas as pd
import pickle as pkl
import os

key = '*'
url = 'https://api.tdameritrade.com/v1/instruments'

df = pd.read_csv('nasdaq_screener_1614989401267.csv')
symbols = df['Symbol'].values.tolist()

start = 0
end = 500
files = []

while start < len(symbols):
    tickers = symbols[start:end]

    payload = {
        "apikey" : key, 
        "symbol" : tickers,
        "projection" : "fundamental"
    }

    results = requests.get(url,params=payload)
    data = results.json()
    f_name = time.asctime() + '.pkl'
    f_name = re.sub('[ :]', ' ', f_name)
    files.append(f_name)
    with open(f_name, 'wb') as file :
        pkl.dump(data, file)
    start = end
    end += 500
    time.sleep(1)

data = []

for file in files: 
    with open(file,'rb') as f:
        info = pkl.load(f)
    tickers = list(info)
    points = ["symbol", "netProfitMarginMRQ", "peRatio", "pegRatio", "high52"]
    for ticker in tickers:
        tick = []
        for point in points:
            tick.append(info[ticker]['fundamental'][point])
        data.append(tick)
    os.remove(file)

points = ["symbol", "Margin", "PE", "PEG", "high52"]

df_results = pd.DataFrame(data, columns=points)
df_peg =df_results[df_results['PEG'] > 1]

def view(size):
    start = 0
    stop = size
    while stop < len(df_peg):
        print(df_peg[start:stop])
        start = stop
        stop += size
    print(df_peg[start:stop])